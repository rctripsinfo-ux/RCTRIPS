import { makeZip } from './zip.js';

const $ = (id) => document.getElementById(id);
const els = {
  form: $('bulk-form'), urls: $('bulk-urls'), file: $('bulk-file'), count: $('bulk-count'),
  lang: $('bulk-lang'), format: $('bulk-format'), auto: $('bulk-auto'), trans: $('bulk-trans'),
  ai: $('bulk-ai'), aiOnly: $('bulk-ai-only'), model: $('bulk-model'),
  start: $('bulk-start'), result: $('bulk-result'), progress: $('bulk-progress'), bar: $('bulk-bar'),
  list: $('bulk-list'), zip: $('bulk-zip'), stop: $('bulk-stop'), retry: $('bulk-retry'),
};
const CONCURRENCY = 2;
let jobs = [];
let stopped = false;

function extractUrls(text) {
  const found = text.match(/https?:\/\/[^\s,;"'<>]+/g) || [];
  return [...new Set(found.map((u) => u.replace(/[).\]]+$/, '')))];
}

function updateCount() {
  const n = extractUrls(els.urls.value).length;
  els.count.textContent = `${n} link${n === 1 ? '' : 's'}`;
}

function safeName(s) {
  return s.replace(/[\\/:*?"<>|\x00-\x1f]+/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 100) || 'subtitles';
}

/** Pick the best track for the wanted language and allowed kinds. */
function pickTrack(tracks, { lang, auto: allowAuto, trans: allowTrans, ai, aiOnly }) {
  const aiTrack = tracks.find((t) => t.kind === 'ai');
  if (aiOnly) return aiTrack || null;
  const t = pickSubtitle(tracks, lang, allowAuto, allowTrans);
  return t || (ai ? aiTrack || null : null);
}

function pickSubtitle(tracks, lang, allowAuto, allowTrans) {
  const kinds = ['manual', ...(allowAuto ? ['auto'] : []), ...(allowTrans ? ['translated'] : [])];
  const base = (code) => code.replace(/-orig$/, '').toLowerCase();
  const want = lang.trim().toLowerCase();
  for (const kind of kinds) {
    const pool = tracks.filter((t) => t.kind === kind);
    if (!want) {
      // No language given: the video's own language (original upload, else the "-orig" auto track).
      const t = kind === 'auto' ? pool.find((x) => x.lang.endsWith('-orig')) || pool[0] : pool[0];
      if (t && kind !== 'translated') return t;
      continue;
    }
    const t = pool.find((x) => base(x.lang) === want) || pool.find((x) => base(x.lang).startsWith(want + '-'));
    if (t) return t;
  }
  return null;
}

function setStatus(job, cls, text) {
  job.status = cls;
  job.st.className = `st ${cls}`;
  job.st.textContent = text;
}

function renderProgress() {
  const done = jobs.filter((j) => j.status === 'ok' || j.status === 'err').length;
  const ok = jobs.filter((j) => j.status === 'ok').length;
  const failed = jobs.filter((j) => j.status === 'err').length;
  els.progress.textContent = `${done} / ${jobs.length} done · ${ok} ok${failed ? ` · ${failed} failed` : ''}`;
  els.bar.style.width = `${jobs.length ? (done / jobs.length) * 100 : 0}%`;
  els.zip.disabled = ok === 0;
  els.zip.textContent = ok ? `Download ZIP (${ok})` : 'Download ZIP';
  els.retry.hidden = !failed || jobs.some((j) => j.status === 'run' || j.status === 'wait');
}

async function runJob(job, opts) {
  setStatus(job, 'run', 'Working…');
  try {
    const res = await fetch('/api/info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: job.url }),
    });
    const info = await res.json();
    if (!res.ok) throw new Error(info.error || 'Failed to read video');
    job.nameEl.textContent = info.title;
    const track = pickTrack(info.tracks, opts);
    if (!track) {
      const langs = [...new Set(info.tracks.filter((t) => t.kind === 'manual' || t.kind === 'auto').map((t) => t.lang))];
      throw new Error(info.tracks.length ? `No "${opts.lang || 'original'}" subtitles (available: ${langs.slice(0, 8).join(', ') || 'translations only'})` : 'No subtitles on this video');
    }
    const q = new URLSearchParams({ url: info.url, track: track.id, format: opts.format });
    if (track.kind === 'ai') {
      q.set('model', opts.model);
      setStatus(job, 'run', 'Transcribing audio…');
    }
    const sub = await fetch(`/api/subtitle?${q}`);
    const text = await sub.text();
    if (!sub.ok) throw new Error(JSON.parse(text).error || 'Download failed');
    const cd = sub.headers.get('Content-Disposition') || '';
    const name = decodeURIComponent((cd.match(/filename\*=UTF-8''([^;]+)/) || [])[1] || '') || `${safeName(info.title)}.${opts.format}`;
    job.file = { name, text: text.replace(/^\uFEFF/, '') };
    setStatus(job, 'ok', track.kind === 'ai' ? 'AI transcript' : `${track.lang}${track.kind === 'manual' ? '' : ` (${track.kind})`}`);
    job.msg.textContent = job.file.name;
  } catch (e) {
    setStatus(job, 'err', 'Failed');
    job.msg.textContent = e.message;
  }
  renderProgress();
}

async function runAll(list) {
  stopped = false;
  els.start.disabled = true;
  els.stop.hidden = false;
  const opts = {
    lang: els.lang.value, format: els.format.value, auto: els.auto.checked, trans: els.trans.checked,
    ai: els.ai.checked, aiOnly: els.aiOnly.checked, model: els.model.value,
  };
  localStorage.setItem('subgrab:model', opts.model);
  const queue = [...list];
  list.forEach((j) => { setStatus(j, 'wait', 'Waiting'); j.msg.textContent = ''; });
  renderProgress();
  const worker = async () => {
    while (queue.length && !stopped) await runJob(queue.shift(), opts);
  };
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  list.filter((j) => j.status === 'wait').forEach((j) => setStatus(j, 'err', 'Stopped'));
  els.start.disabled = false;
  els.stop.hidden = true;
  renderProgress();
}

els.form.addEventListener('submit', (e) => {
  e.preventDefault();
  const urls = extractUrls(els.urls.value);
  if (!urls.length) return alert('Add at least one video link.');
  jobs = urls.map((url) => {
    const st = Object.assign(document.createElement('span'), { className: 'st' });
    const nameEl = Object.assign(document.createElement('span'), { className: 'name', textContent: url });
    const msg = document.createElement('small');
    const li = document.createElement('li');
    const row = Object.assign(document.createElement('div'), { className: 'row' });
    row.append(nameEl, st);
    li.append(row, msg);
    return { url, st, nameEl, msg, li, status: 'wait', file: null };
  });
  els.list.replaceChildren(...jobs.map((j) => j.li));
  els.result.hidden = false;
  els.result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  runAll(jobs);
});

els.zip.addEventListener('click', () => {
  const used = new Map();
  const files = jobs.filter((j) => j.file).map(({ file }) => {
    const n = used.get(file.name) || 0;
    used.set(file.name, n + 1);
    return n ? { ...file, name: file.name.replace(/(\.[^.]+)$/, ` (${n + 1})$1`) } : file;
  });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(makeZip(files));
  a.download = `subtitles-${new Date().toISOString().slice(0, 10)}.zip`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 10000);
});

els.stop.addEventListener('click', () => { stopped = true; });
els.retry.addEventListener('click', () => runAll(jobs.filter((j) => j.status === 'err')));
els.urls.addEventListener('input', updateCount);
els.file.addEventListener('change', async () => {
  const f = els.file.files[0];
  if (!f) return;
  const urls = extractUrls(await f.text());
  const existing = els.urls.value.trim();
  els.urls.value = [existing, ...urls].filter(Boolean).join('\n');
  els.file.value = '';
  updateCount();
});

els.model.value = localStorage.getItem('subgrab:model') || els.model.value;

// Single / bulk mode switch
const modeButtons = document.querySelectorAll('.mode');
function setMode(mode) {
  modeButtons.forEach((b) => b.setAttribute('aria-selected', String(b.dataset.mode === mode)));
  const bulk = mode === 'bulk';
  els.form.hidden = !bulk;
  ['form', 'recent', 'result', 'loading', 'error'].forEach((id) => {
    const n = $(id);
    if (bulk) { n.dataset.wasHidden = n.hidden; n.hidden = true; }
    else if (id === 'form') n.hidden = false;
    else if (n.dataset.wasHidden !== undefined) n.hidden = n.dataset.wasHidden === 'true';
  });
  els.result.hidden = !bulk || !jobs.length;
}
modeButtons.forEach((b) => b.addEventListener('click', () => setMode(b.dataset.mode)));
