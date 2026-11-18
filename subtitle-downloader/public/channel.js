const $ = (id) => document.getElementById(id);
const els = {
  url: $('ch-url'), load: $('ch-load'), limit: $('ch-limit'), status: $('ch-status'),
  picker: $('ch-picker'), filter: $('ch-filter'), all: $('ch-all'), none: $('ch-none'),
  count: $('ch-count'), add: $('ch-add'), list: $('ch-list'), urls: $('bulk-urls'),
};
let videos = [];

function fmtDuration(s) {
  if (!s) return '';
  s = Math.round(s);
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
  return (h ? `${h}:${String(m).padStart(2, '0')}` : m) + ':' + String(sec).padStart(2, '0');
}

function status(msg) {
  els.status.textContent = msg;
  els.status.hidden = !msg;
}

function visible() {
  const q = els.filter.value.trim().toLowerCase();
  return videos.filter((v) => !q || v.title.toLowerCase().includes(q));
}

function updateCount() {
  const n = videos.filter((v) => v.checked).length;
  els.count.textContent = `${n} of ${videos.length} selected`;
  els.add.disabled = n === 0;
}

function render() {
  els.list.replaceChildren(...visible().map((v) => {
    const box = Object.assign(document.createElement('input'), { type: 'checkbox', checked: v.checked });
    box.onchange = () => { v.checked = box.checked; updateCount(); };
    const label = document.createElement('label');
    label.append(box,
      Object.assign(document.createElement('span'), { className: 't', textContent: v.title, title: v.url }),
      Object.assign(document.createElement('small'), { textContent: [v.section !== 'videos' && v.section !== 'playlist' ? v.section : '', fmtDuration(v.duration)].filter(Boolean).join(' · ') }));
    const li = document.createElement('li');
    li.append(label);
    return li;
  }));
  updateCount();
}

async function load() {
  const url = els.url.value.trim();
  if (!url) return els.url.focus();
  const sections = ['videos', 'shorts', 'streams'].filter((s) => $(`ch-${s}`).checked);
  els.load.disabled = true;
  els.picker.hidden = true;
  status('Loading video list… large channels can take a minute or two.');
  try {
    const res = await fetch('/api/list', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, limit: Number(els.limit.value) || 0, sections }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Could not load the channel');
    videos = data.videos.map((v) => ({ ...v, checked: true }));
    status(videos.length ? `${data.uploader || data.title}: found ${videos.length} video${videos.length === 1 ? '' : 's'}.` : 'No videos found. Try ticking Shorts or Live streams.');
    els.filter.value = '';
    els.picker.hidden = !videos.length;
    render();
  } catch (e) {
    status(`Error: ${e.message}`);
  } finally {
    els.load.disabled = false;
  }
}

els.load.addEventListener('click', load);
els.url.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); load(); } });
els.filter.addEventListener('input', render);
els.all.addEventListener('click', () => { visible().forEach((v) => (v.checked = true)); render(); });
els.none.addEventListener('click', () => { visible().forEach((v) => (v.checked = false)); render(); });
els.add.addEventListener('click', () => {
  const picked = videos.filter((v) => v.checked).map((v) => v.url);
  const existing = els.urls.value.trim();
  els.urls.value = [existing, ...picked].filter(Boolean).join('\n');
  els.urls.dispatchEvent(new Event('input'));
  status(`Added ${picked.length} video${picked.length === 1 ? '' : 's'} to the list below. Now press "Start bulk download".`);
  els.picker.hidden = true;
  els.urls.scrollIntoView({ behavior: 'smooth', block: 'center' });
});
