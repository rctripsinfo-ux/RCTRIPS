// Thin wrapper around yt-dlp for metadata and subtitle retrieval.
import { spawn } from 'node:child_process';
import { mkdtemp, readdir, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const YTDLP = process.env.YTDLP_PATH || 'yt-dlp';
const EXTRA = (process.env.YTDLP_EXTRA_ARGS || '').split(/\s+/).filter(Boolean);
const TIMEOUT_MS = Number(process.env.YTDLP_TIMEOUT_MS || 90000);
const CACHE_MS = 10 * 60 * 1000;
const PREFERRED = ['vtt', 'srt'];

let baseArgs = null;
const cache = new Map();

function run(args) {
  return new Promise((resolve, reject) => {
    const child = spawn(YTDLP, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '';
    let err = '';
    const timer = setTimeout(() => child.kill('SIGKILL'), TIMEOUT_MS);
    child.stdout.on('data', (d) => (out += d));
    child.stderr.on('data', (d) => (err += d));
    child.on('error', (e) => {
      clearTimeout(timer);
      reject(e.code === 'ENOENT'
        ? new Error('yt-dlp is not installed or not on PATH. Install it: https://github.com/yt-dlp/yt-dlp#installation')
        : e);
    });
    child.on('close', (code, signal) => {
      clearTimeout(timer);
      if (signal) return reject(new Error('Extractor timed out'));
      if (code !== 0) {
        const msg = (err.match(/ERROR: (.*)/g) || []).pop() || err.trim().split('\n').pop() || `yt-dlp exited with ${code}`;
        return reject(new Error(msg.replace(/^ERROR:\s*/, '')));
      }
      resolve(out);
    });
  });
}

async function getBaseArgs() {
  if (baseArgs) return baseArgs;
  const args = ['--no-warnings', '--no-playlist'];
  try {
    const help = await run(['--help']);
    if (help.includes('--js-runtimes')) args.push('--js-runtimes', 'node');
  } catch { /* surfaced on the real call */ }
  return (baseArgs = [...args, ...EXTRA]);
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
  const json = await run([...(await getBaseArgs()), '-J', '--skip-download', '--', url]);
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
    tracks: buildTracks(info),
  };
  cache.set(url, { value, expires: Date.now() + CACHE_MS });
  if (cache.size > 200) cache.delete(cache.keys().next().value);
  return value;
}

/** Return the raw subtitle text (VTT or SRT) for a track. */
export async function getSubtitleSource(url, trackId) {
  const info = await getInfo(url);
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
    await run(args);
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
