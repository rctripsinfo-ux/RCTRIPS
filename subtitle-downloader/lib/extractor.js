// Thin wrapper around yt-dlp for metadata and subtitle retrieval.
import { spawn } from 'node:child_process';
import { mkdtemp, readdir, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import { fileURLToPath } from 'node:url';

const YTDLP = process.env.YTDLP_PATH || 'yt-dlp';
const GALLERYDL = process.env.GALLERYDL_PATH || 'gallery-dl';
const PYTHON = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
const COOKIES = process.env.COOKIES_FROM_BROWSER || '';
const EXTRA = [
  ...(COOKIES ? ['--cookies-from-browser', COOKIES] : []),
  ...(process.env.YTDLP_EXTRA_ARGS || '').split(/\s+/).filter(Boolean),
];
const TRANSCRIBE_PY = fileURLToPath(new URL('./transcribe.py', import.meta.url));
const TRANSCRIBE_TIMEOUT_MS = Number(process.env.TRANSCRIBE_TIMEOUT_MS || 60 * 60 * 1000);
export const AI_MODELS = ['large-v3-turbo', 'large-v3', 'medium', 'small'];
const isInstagram = (url) => /(^|\.)instagram\.com$/i.test(new URL(url).hostname);
const TIMEOUT_MS = Number(process.env.YTDLP_TIMEOUT_MS || 90000);
const CACHE_MS = 10 * 60 * 1000;
const PREFERRED = ['vtt', 'srt'];

let baseArgs = null;
const cache = new Map();

const NOT_FOUND = {
  [YTDLP]: 'yt-dlp is not installed. Run: python -m pip install --user -U yt-dlp',
  [GALLERYDL]: 'gallery-dl is not installed (needed for Instagram profiles). Run: python -m pip install --user -U gallery-dl',
  [PYTHON]: 'Python is not installed. Get it from https://www.python.org',
};
const PY_MODULE = { [YTDLP]: 'yt_dlp', [GALLERYDL]: 'gallery_dl' };
const useModule = new Set();

/** Run a CLI tool; falls back to "python -m module" when the executable isn't on PATH. */
async function run(args, timeoutMs = TIMEOUT_MS, tool = YTDLP) {
  if (useModule.has(tool)) return exec(PYTHON, ['-m', PY_MODULE[tool], ...args], timeoutMs, NOT_FOUND[tool]);
  try {
    return await exec(tool, args, timeoutMs, NOT_FOUND[tool]);
  } catch (e) {
    if (!e.notFound || !PY_MODULE[tool]) throw e;
    useModule.add(tool);
    return exec(PYTHON, ['-m', PY_MODULE[tool], ...args], timeoutMs, NOT_FOUND[tool]);
  }
}

function exec(cmd, args, timeoutMs, notFoundMsg) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'], env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
    let out = '';
    let err = '';
    const timer = setTimeout(() => child.kill('SIGKILL'), timeoutMs);
    child.stdout.on('data', (d) => (out += d));
    child.stderr.on('data', (d) => (err += d));
    child.on('error', (e) => {
      clearTimeout(timer);
      reject(e.code === 'ENOENT'
        ? Object.assign(new Error(notFoundMsg || `${cmd} not found`), { notFound: true })
        : e);
    });
    child.on('close', (code, signal) => {
      clearTimeout(timer);
      if (signal) return reject(new Error('Extractor timed out'));
      if (code !== 0) {
        if (/No module named/.test(err) && notFoundMsg) return reject(Object.assign(new Error(notFoundMsg), { notFound: true }));
        const msg = (err.match(/(?:ERROR|\[error\]):? (.*)/gi) || []).pop() || err.trim().split('\n').pop() || `${cmd} exited with ${code}`;
        return reject(new Error(msg.replace(/^(ERROR|\[error\]):?\s*/i, '')));
      }
      resolve(out);
    });
  });
}

async function getBaseArgs({ playlist = false } = {}) {
  if (!baseArgs) baseArgs = await buildBaseArgs();
  return playlist ? baseArgs.filter((a) => a !== '--no-playlist') : baseArgs;
}

async function buildBaseArgs() {
  const args = ['--no-warnings', '--no-playlist'];
  try {
    const help = await run(['--help']);
    if (help.includes('--js-runtimes')) args.push('--js-runtimes', 'node');
  } catch { /* surfaced on the real call */ }
  return [...args, ...EXTRA];
}

const LOGIN_RE = /login|log in|cookies|rate.?limit|not available|private|empty media response|401|403/i;

/** yt-dlp call; for Instagram, retries with Firefox cookies when a login is needed. */
async function ytdlp(args, url, timeoutMs) {
  try {
    return await run(args, timeoutMs);
  } catch (e) {
    if (COOKIES || !isInstagram(url) || !LOGIN_RE.test(e.message)) throw e;
    try {
      return await run(['--cookies-from-browser', 'firefox', ...args], timeoutMs);
    } catch {
      throw new Error(`${e.message} — Instagram needs you to be logged in: log in to instagram.com in Firefox, then try again.`);
    }
  }
}

export async function checkExtractor() {
  return (await run(['--version'])).trim();
}

function pickFormat(formats = []) {
  for (const ext of PREFERRED) {
    const f = formats.find((x) => x.ext === ext && x.url);
    if (f) return f;
  }
  return formats.find((x) => x.url) || formats[0];
}

function buildTracks(info) {
  const tracks = [];
  const add = (kind, lang, formats) => {
    if (!formats?.length || lang === 'live_chat') return;
    const f = pickFormat(formats);
    tracks.push({
      id: `${kind}:${lang}`,
      kind,
      lang,
      name: formats.find((x) => x.name)?.name || lang,
      sourceExt: f?.ext,
      _format: f,
    });
  };
  for (const [lang, formats] of Object.entries(info.subtitles || {})) add('manual', lang, formats);
  const origLang = info.language;
  for (const [lang, formats] of Object.entries(info.automatic_captions || {})) {
    const isOrig = lang.endsWith('-orig') || lang === origLang;
    add(isOrig ? 'auto' : 'translated', lang, formats);
  }
  // If YouTube marks the source as "xx-orig", don't duplicate it as a translation of itself.
  const origs = new Set(tracks.filter((t) => t.lang.endsWith('-orig')).map((t) => t.lang.slice(0, -5)));
  return tracks
    .filter((t) => !(t.kind !== 'manual' && origs.has(t.lang) && !t.lang.endsWith('-orig')))
    .map((t) => (t.kind === 'translated' && origs.has(t.lang) ? { ...t, kind: 'auto' } : t))
    .sort((a, b) => a.name.localeCompare(b.name));
}

export async function getInfo(url) {
  const hit = cache.get(url);
  if (hit && hit.expires > Date.now()) return hit.value;
  const json = await ytdlp([...(await getBaseArgs()), '-J', '--skip-download', '--', url], url);
  const info = JSON.parse(json);
  if (info._type === 'playlist') throw new Error('Playlists are not supported. Paste a single video link.');
  const value = {
    url,
    title: info.title || 'video',
    uploader: info.uploader || info.channel || '',
    duration: info.duration || null,
    thumbnail: info.thumbnail || null,
    site: info.extractor_key || info.extractor || '',
    webpage: info.webpage_url || url,
    tracks: [...buildTracks(info), { id: 'ai:auto', kind: 'ai', lang: 'auto', name: 'AI transcription (from audio)' }],
  };
  cache.set(url, { value, expires: Date.now() + CACHE_MS });
  if (cache.size > 200) cache.delete(cache.keys().next().value);
  return value;
}

/** Return the raw subtitle text (VTT or SRT) for a track. */
export async function getSubtitleSource(url, trackId, { model = AI_MODELS[0] } = {}) {
  const info = await getInfo(url);
  if (trackId === 'ai:auto') {
    const r = await transcribeCached(url, model);
    return { info, track: { id: trackId, kind: 'ai', lang: r.language }, text: r.vtt };
  }
  const track = info.tracks.find((t) => t.id === trackId);
  if (!track) throw Object.assign(new Error('Subtitle track not found'), { status: 404 });
  const f = track._format;

  if (f?.url && PREFERRED.includes(f.ext)) {
    try {
      const res = await fetch(f.url, { headers: f.http_headers || {}, signal: AbortSignal.timeout(30000) });
      if (res.ok) {
        const text = await res.text();
        if (text.includes('-->')) return { info, track, text };
      }
    } catch { /* fall back to yt-dlp below */ }
  }
  return { info, track, text: await downloadWithYtdlp(url, track) };
}

async function downloadWithYtdlp(url, track) {
  const dir = await mkdtemp(join(tmpdir(), 'subgrab-'));
  try {
    const args = [
      ...(await getBaseArgs()),
      '--skip-download',
      track.kind === 'manual' ? '--write-subs' : '--write-auto-subs',
      '--sub-langs', track.lang,
      '--sub-format', 'vtt/srt/best',
      '--convert-subs', 'vtt',
      '-o', join(dir, 'sub.%(ext)s'),
      '--', url,
    ];
    await ytdlp(args, url);
    const file = (await readdir(dir)).find((n) => /\.(vtt|srt)$/.test(n));
    if (!file) throw new Error('No subtitle file was produced for this language');
    return await readFile(join(dir, file), 'utf8');
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

export function publicInfo(info) {
  return { ...info, tracks: info.tracks.map(({ _format, ...t }) => t) };
}

const LIST_TIMEOUT_MS = Number(process.env.YTDLP_LIST_TIMEOUT_MS || 15 * 60 * 1000);
const TAB_RE = /\/(videos|shorts|streams|live|podcasts|releases)\/?$/;

function videoUrl(e) {
  if (e.url && /^https?:/.test(e.url)) return e.url;
  if (e.id && /youtube/i.test(e.ie_key || e.extractor_key || '')) return `https://www.youtube.com/watch?v=${e.id}`;
  return e.webpage_url || e.url || null;
}

async function listOnce(url, limit) {
  const args = [...(await getBaseArgs({ playlist: true })), '-J', '--flat-playlist'];
  if (limit > 0) args.push('--playlist-end', String(limit));
  return JSON.parse(await run([...args, '--', url], LIST_TIMEOUT_MS));
}

/**
 * List the videos of a channel or playlist (fast, metadata only).
 * sections: which channel tabs to include when given a channel's main page.
 */
export async function listVideos(url, { limit = 0, sections = ['videos'] } = {}) {
  const igUser = instagramProfile(url);
  if (igUser) return listInstagram(igUser, limit);
  const top = await listOnce(url, limit);
  if (top._type !== 'playlist') {
    return { title: top.title || url, uploader: top.uploader || top.channel || '', videos: [{ url: top.webpage_url || url, title: top.title, duration: top.duration, section: 'video' }] };
  }
  const entries = top.entries || [];
  const tabs = entries.filter((e) => e.url && TAB_RE.test(e.url) && (e._type === 'url' || e._type === 'playlist'));
  const videos = [];
  const push = (list, section) => {
    for (const e of list || []) {
      const u = videoUrl(e);
      if (u && !videos.some((v) => v.url === u)) videos.push({ url: u, title: e.title || u, duration: e.duration || null, section });
    }
  };
  if (tabs.length && tabs.length === entries.length) {
    // A channel's main page: entries are its tabs (Videos, Shorts, Live...).
    for (const tab of tabs) {
      const section = tab.url.match(TAB_RE)[1];
      if (!sections.includes(section)) continue;
      try {
        push((await listOnce(tab.url, limit)).entries, section);
      } catch { /* tab may be empty or unavailable */ }
    }
  } else {
    push(entries, (url.match(TAB_RE) || [])[1] || 'playlist');
  }
  return { title: top.title || url, uploader: top.uploader || top.channel || '', videos: limit > 0 ? videos.slice(0, limit) : videos };
}

// ---------- AI transcription (faster-whisper) ----------
const aiCache = new Map();
let aiQueue = Promise.resolve();

function vttTime(sec) {
  const ms = Math.round(sec * 1000);
  const p = (n, w = 2) => String(n).padStart(w, '0');
  return `${p(Math.floor(ms / 3600000))}:${p(Math.floor((ms % 3600000) / 60000))}:${p(Math.floor((ms % 60000) / 1000))}.${p(ms % 1000, 3)}`;
}

const MAX_CHARS = 42;
const MAX_GAP = 0.6; // seconds of silence that starts a new caption

/**
 * Whisper JSON -> WebVTT with inline per-word timestamps (understood by convert()).
 * Long segments are split into readable captions (~42 chars, or at pauses / sentence ends).
 */
export function whisperToVtt(result) {
  const cues = [];
  for (const seg of result.segments) {
    const words = seg.words?.length ? seg.words : seg.text ? [{ start: seg.start, end: seg.end, word: seg.text }] : [];
    let cur = [];
    const flush = () => {
      if (!cur.length) return;
      const line = cur.map((w, i) => (i === 0 ? w.word : `<${vttTime(w.start)}>${w.word}`)).join(' ');
      cues.push(`${vttTime(cur[0].start)} --> ${vttTime(cur.at(-1).end)}\n${line}`);
      cur = [];
    };
    for (const w of words) {
      const prev = cur.at(-1);
      const len = cur.reduce((n, x) => n + x.word.length + 1, 0) + w.word.length;
      if (prev && (len > MAX_CHARS || w.start - prev.end > MAX_GAP || /[.!?]$/.test(prev.word))) flush();
      cur.push(w);
    }
    flush();
  }
  return 'WEBVTT\n\n' + cues.join('\n\n') + '\n';
}

async function transcribe(url, model) {
  const dir = await mkdtemp(join(tmpdir(), 'subgrab-ai-'));
  try {
    await ytdlp([...(await getBaseArgs()), '-f', 'bestaudio/best', '-o', join(dir, 'audio.%(ext)s', ), '--', url], url, TRANSCRIBE_TIMEOUT_MS);
    const file = (await readdir(dir)).find((n) => n.startsWith('audio.') && !n.endsWith('.part'));
    if (!file) throw new Error('Could not download the audio for transcription');
    const out = await exec(PYTHON, [TRANSCRIBE_PY, join(dir, file), '--model', model], TRANSCRIBE_TIMEOUT_MS,
      'Python is not installed. Get it from https://www.python.org');
    const result = JSON.parse(out);
    if (!result.segments.length) throw new Error('No speech was detected in this video');
    return { language: result.language, vtt: whisperToVtt(result) };
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

/** One transcription at a time (it is CPU/GPU heavy); results cached per URL and model. */
function transcribeCached(url, model) {
  const key = `${model}|${url}`;
  if (aiCache.has(key)) return aiCache.get(key);
  const job = aiQueue.then(() => transcribe(url, model));
  aiQueue = job.catch(() => {});
  aiCache.set(key, job);
  job.catch(() => aiCache.delete(key));
  if (aiCache.size > 300) aiCache.delete(aiCache.keys().next().value);
  return job;
}

// ---------- Instagram profiles (gallery-dl) ----------
const IG_RESERVED = new Set(['p', 'reel', 'reels', 'tv', 'stories', 'explore', 'accounts', 'direct']);

export function instagramProfile(url) {
  const u = new URL(url);
  if (!isInstagram(url)) return null;
  const [user] = u.pathname.split('/').filter(Boolean);
  return user && !IG_RESERVED.has(user.toLowerCase()) ? user : null;
}

async function listInstagram(user, limit) {
  const target = `https://www.instagram.com/${user}/reels/`;
  const args = ['-j', ...(limit > 0 ? ['--range', `1-${limit}`] : []), target];
  let out;
  const cookies = COOKIES || 'firefox';
  try {
    out = await run(['--cookies-from-browser', cookies, ...args], LIST_TIMEOUT_MS, GALLERYDL);
  } catch (e) {
    if (e.notFound) throw e;
    try {
      out = await run(args, LIST_TIMEOUT_MS, GALLERYDL);
    } catch {
      throw new Error(`${e.message} — log in to instagram.com in ${cookies === 'firefox' ? 'Firefox' : cookies}, then try again.`);
    }
  }
  const messages = JSON.parse(out || '[]');
  const videos = [];
  const seen = new Set();
  for (const m of messages) {
    if (!Array.isArray(m)) continue;
    const meta = m[0] === 3 ? m[2] : m[0] === 2 ? m[1] : null;
    const code = meta && (meta.post_shortcode || meta.shortcode);
    if (!code || seen.has(code)) continue;
    seen.add(code);
    const text = (meta.description || '').replace(/\s+/g, ' ').trim();
    videos.push({
      url: `https://www.instagram.com/reel/${code}/`,
      title: text ? (text.length > 90 ? text.slice(0, 90) + '…' : text) : `Reel ${code}`,
      duration: meta.video_duration || null,
      section: 'reels',
    });
  }
  return { title: `@${user}`, uploader: `@${user}`, videos: limit > 0 ? videos.slice(0, limit) : videos };
}
