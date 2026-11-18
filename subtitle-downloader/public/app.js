const $ = (id) => document.getElementById(id);
const els = {
  form: $('form'), url: $('url'), paste: $('paste'), submit: $('submit'), error: $('error'),
  recent: $('recent'), loading: $('loading'), result: $('result'), thumb: $('thumb'),
  title: $('title'), meta: $('meta'), source: $('source'), tabs: $('tabs'), filter: $('filter'),
  tracks: $('tracks'), empty: $('empty'), preview: $('preview'), pvTitle: $('pv-title'),
  pvBody: $('pv-body'), toast: $('toast'),
};

const KINDS = [
  ['all', 'All'],
  ['manual', 'Original'],
  ['auto', 'Auto-generated'],
  ['translated', 'Translated'],
];
const KIND_LABEL = { manual: 'Original', auto: 'Auto-generated', translated: 'Auto-translated' };
const RECENT_KEY = 'subgrab:recent';
const state = { info: null, kind: 'all' };

let displayNames;
try { displayNames = new Intl.DisplayNames([navigator.language || 'en'], { type: 'language' }); } catch { /* old browsers */ }

function langName(track) {
  const code = track.lang.replace(/-orig$/, '');
  let name = track.name && track.name !== track.lang ? track.name : '';
  if (!name && displayNames) {
    try { name = displayNames.of(code); } catch { /* invalid tag */ }
  }
  return name || code;
}

function fmtDuration(s) {
  if (!s) return '';
  s = Math.round(s);
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
  return (h ? `${h}:${String(m).padStart(2, '0')}` : m) + ':' + String(sec).padStart(2, '0');
}

function showError(msg) {
  els.error.textContent = msg;
  els.error.hidden = !msg;
}

function toast(msg) {
  els.toast.textContent = msg;
  els.toast.hidden = false;
  clearTimeout(toast.t);
  toast.t = setTimeout(() => (els.toast.hidden = true), 2200);
}

function subtitleUrl(track, format, inline = false) {
  const q = new URLSearchParams({ url: state.info.url, track: track.id, format });
  if (inline) q.set('inline', '1');
  return `/api/subtitle?${q}`;
}

function el(tag, props = {}, children = []) {
  const n = Object.assign(document.createElement(tag), props);
  n.append(...children);
  return n;
}

function renderTabs() {
  const tracks = state.info.tracks;
  els.tabs.replaceChildren(...KINDS.map(([kind, label]) => {
    const count = kind === 'all' ? tracks.length : tracks.filter((t) => t.kind === kind).length;
    const b = el('button', { type: 'button', role: 'tab', disabled: !count && kind !== 'all' },
      [label, el('span', { className: 'count', textContent: `(${count})` })]);
    b.setAttribute('aria-selected', String(state.kind === kind));
    b.onclick = () => { state.kind = kind; renderTabs(); renderTracks(); };
    return b;
  }));
}

function renderTracks() {
  const q = els.filter.value.trim().toLowerCase();
  const order = { manual: 0, auto: 1, translated: 2 };
  const list = state.info.tracks
    .filter((t) => state.kind === 'all' || t.kind === state.kind)
    .map((t) => ({ ...t, label: langName(t) }))
    .filter((t) => !q || t.label.toLowerCase().includes(q) || t.lang.toLowerCase().includes(q))
    .sort((a, b) => order[a.kind] - order[b.kind] || a.label.localeCompare(b.label));

  els.empty.hidden = list.length > 0;
  els.empty.textContent = state.info.tracks.length ? 'No languages match your filter.' : 'No subtitles found for this video.';
  els.tracks.replaceChildren(...list.map((t) => {
    const actions = ['srt', 'txt', 'vtt'].map((f) =>
      el('a', { className: f, href: subtitleUrl(t, f), textContent: f.toUpperCase(), download: '' }));
    const view = el('button', { type: 'button', textContent: 'Preview' });
    view.onclick = () => openPreview(t);
    return el('li', {}, [
      el('div', { className: 'lang' }, [el('b', { textContent: t.label }), el('small', { textContent: t.lang })]),
      el('span', { className: 'badge', textContent: KIND_LABEL[t.kind] }),
      el('div', { className: 'actions' }, [view, ...actions]),
    ]);
  }));
}

function render(info) {
  state.info = info;
  state.kind = info.tracks.some((t) => t.kind === 'manual') ? 'manual' : 'all';
  els.filter.value = '';
  els.thumb.src = info.thumbnail || 'favicon.svg';
  els.title.textContent = info.title;
  els.meta.textContent = [info.site, info.uploader, fmtDuration(info.duration)].filter(Boolean).join(' · ');
  els.source.href = info.webpage;
  renderTabs();
  renderTracks();
  els.result.hidden = false;
}

async function openPreview(track) {
  els.pvTitle.textContent = `${langName(track)} — ${KIND_LABEL[track.kind]}`;
  els.pvBody.textContent = 'Loading…';
  els.preview.showModal();
  try {
    const res = await fetch(subtitleUrl(track, 'txt', true));
    const text = await res.text();
    if (!res.ok) throw new Error(JSON.parse(text).error);
    els.pvBody.textContent = text.replace(/^﻿/, '');
  } catch (e) {
    els.pvBody.textContent = `Could not load preview: ${e.message}`;
  }
}

function loadRecent() {
  try { return JSON.parse(localStorage.getItem(RECENT_KEY)) || []; } catch { return []; }
}

function saveRecent(info) {
  const list = [{ url: info.url, title: info.title }, ...loadRecent().filter((r) => r.url !== info.url)].slice(0, 5);
  localStorage.setItem(RECENT_KEY, JSON.stringify(list));
  renderRecent();
}

function renderRecent() {
  const list = loadRecent();
  els.recent.hidden = !list.length;
  els.recent.replaceChildren(el('span', { className: 'muted', textContent: 'Recent:' }), ...list.map((r) => {
    const b = el('button', { type: 'button', className: 'ghost', textContent: r.title, title: r.url });
    b.onclick = () => { els.url.value = r.url; lookup(); };
    return b;
  }));
}

async function lookup() {
  const url = els.url.value.trim();
  if (!url) return;
  showError('');
  els.result.hidden = true;
  els.loading.hidden = false;
  els.submit.disabled = true;
  try {
    const res = await fetch('/api/info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Request failed');
    render(data);
    saveRecent(data);
    history.replaceState(null, '', `?url=${encodeURIComponent(url)}`);
  } catch (e) {
    showError(e.message);
  } finally {
    els.loading.hidden = true;
    els.submit.disabled = false;
  }
}

els.form.addEventListener('submit', (e) => { e.preventDefault(); lookup(); });
els.filter.addEventListener('input', renderTracks);
els.paste.addEventListener('click', async () => {
  try {
    els.url.value = (await navigator.clipboard.readText()).trim();
    els.url.focus();
  } catch {
    toast('Clipboard access blocked — press Ctrl/Cmd+V instead');
  }
});
$('pv-close').onclick = () => els.preview.close();
els.preview.addEventListener('click', (e) => { if (e.target === els.preview) els.preview.close(); });
$('pv-copy').onclick = async () => {
  await navigator.clipboard.writeText(els.pvBody.textContent);
  toast('Copied to clipboard');
};

renderRecent();
const initial = new URLSearchParams(location.search).get('url');
if (initial) { els.url.value = initial; lookup(); }
