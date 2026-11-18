// Subtitle parsing and conversion (WebVTT / SRT -> SRT, VTT, TXT).

const TS = /(\d{1,2}:)?\d{1,2}:\d{2}[.,]\d{1,3}/;

function toMs(ts) {
  const [hms, frac = '0'] = ts.replace(',', '.').split('.');
  const parts = hms.split(':').map(Number);
  while (parts.length < 3) parts.unshift(0);
  const [h, m, s] = parts;
  return ((h * 60 + m) * 60 + s) * 1000 + Number(frac.padEnd(3, '0').slice(0, 3));
}

function fmt(ms, sep) {
  const pad = (n, w = 2) => String(n).padStart(w, '0');
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  return `${pad(h)}:${pad(m)}:${pad(s)}${sep}${pad(ms % 1000, 3)}`;
}

const ENTITIES = { '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&nbsp;': ' ' };

function cleanLine(line) {
  return line
    .replace(/<\d{1,2}:\d{2}[:.\d]*>/g, '') // inline karaoke timestamps
    .replace(/<\/?[a-z][^>]*>/gi, '') // <c>, <i>, <b>, <v Name>, <font ...>
    .replace(/&(amp|lt|gt|quot|#39|nbsp);/g, (e) => ENTITIES[e])
    .replace(/\s+/g, ' ')
    .trim();
}

/** Parse WebVTT or SRT text into cues: [{start, end, lines}] (ms). */
export function parseCues(text) {
  const blocks = text.replace(/^﻿/, '').replace(/\r\n?/g, '\n').split(/\n{2,}/);
  const cues = [];
  for (const block of blocks) {
    const rows = block.split('\n');
    const i = rows.findIndex((r) => r.includes('-->'));
    if (i === -1) continue;
    const [a, b] = rows[i].split('-->');
    const sa = a.match(TS);
    const sb = b.match(TS);
    if (!sa || !sb) continue;
    const lines = rows.slice(i + 1).map(cleanLine).filter(Boolean);
    cues.push({ start: toMs(sa[0]), end: toMs(sb[0]), lines });
  }
  return cues;
}

/**
 * Remove the "rolling" duplication found in auto-generated captions,
 * where each cue repeats the previous cue's line before adding a new one.
 */
export function dedupeCues(cues) {
  const out = [];
  let prev = [];
  for (const cue of cues) {
    const fresh = cue.lines.filter((l) => !prev.includes(l));
    if (cue.lines.length) prev = cue.lines;
    if (!fresh.length || cue.end - cue.start <= 20) continue;
    const last = out[out.length - 1];
    if (last && last.lines.join('\n') === fresh.join('\n')) {
      last.end = Math.max(last.end, cue.end);
      continue;
    }
    out.push({ start: cue.start, end: cue.end, lines: fresh });
  }
  // Prevent overlaps created by rolling captions.
  for (let i = 0; i < out.length - 1; i++) {
    if (out[i].end > out[i + 1].start) out[i].end = out[i + 1].start;
  }
  return out;
}

export function toSrt(cues) {
  return cues
    .map((c, i) => `${i + 1}\n${fmt(c.start, ',')} --> ${fmt(c.end, ',')}\n${c.lines.join('\n')}\n`)
    .join('\n');
}

export function toVtt(cues) {
  return 'WEBVTT\n\n' + cues
    .map((c) => `${fmt(c.start, '.')} --> ${fmt(c.end, '.')}\n${c.lines.join('\n')}\n`)
    .join('\n');
}

export function toTxt(cues) {
  return cues.map((c) => c.lines.join(' ')).join('\n') + '\n';
}

const INLINE_TS = /<(\d{1,2}:\d{2}(?::\d{2})?[.,]\d{1,3})>/;

function splitWords(text) {
  return text.split(' ').filter(Boolean);
}

/** Spread words across [start, end], weighted by word length. */
function spread(words, start, end) {
  const weights = words.map((w) => w.length + 1);
  const total = weights.reduce((a, b) => a + b, 0);
  let t = start;
  return words.map((w, i) => {
    const s = t;
    t = i === words.length - 1 ? end : Math.round(t + ((end - start) * weights[i]) / total);
    return { start: s, end: t, lines: [w] };
  });
}

/**
 * One cue per word. Uses the exact per-word timestamps embedded in
 * auto-generated captions when present; otherwise estimates each word's
 * timing from its share of the line's duration.
 * Returns { cues, exact }.
 */
export function wordCues(raw) {
  const blocks = raw.replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n').split(/\n{2,}/);
  const segs = [];
  for (const block of blocks) {
    const rows = block.split('\n');
    const i = rows.findIndex((r) => r.includes('-->'));
    if (i === -1) continue;
    const [a, b] = rows[i].split('-->');
    const sa = a.match(TS);
    const sb = b.match(TS);
    if (!sa || !sb) continue;
    const cueStart = toMs(sa[0]);
    const cueEnd = toMs(sb[0]);
    for (const line of rows.slice(i + 1)) {
      if (!INLINE_TS.test(line)) continue;
      const parts = line.split(INLINE_TS); // text, ts, text, ts, text...
      let start = cueStart;
      for (let k = 0; k < parts.length; k += 2) {
        if (k > 0) start = toMs(parts[k - 1]);
        const text = cleanLine(parts[k]);
        if (text) segs.push({ start, cueEnd, text });
      }
    }
  }

  if (!segs.length) {
    const cues = dedupeCues(parseCues(raw)).flatMap((c) => spread(splitWords(c.lines.join(' ')), c.start, c.end));
    return { cues, exact: false };
  }

  segs.sort((x, y) => x.start - y.start);
  const cues = [];
  segs.forEach((seg, i) => {
    const next = segs[i + 1];
    const end = next ? Math.min(seg.cueEnd, next.start) : seg.cueEnd;
    cues.push(...spread(splitWords(seg.text), seg.start, Math.max(end, seg.start + 1)));
  });
  return { cues, exact: true };
}

/** Convert raw subtitle text into the requested format. */
export function convert(raw, format) {
  if (format === 'words') {
    const { cues } = wordCues(raw);
    if (!cues.length) throw new Error('No subtitle cues found in source file');
    return toSrt(cues);
  }
  const cues = dedupeCues(parseCues(raw));
  if (!cues.length) throw new Error('No subtitle cues found in source file');
  if (format === 'srt') return toSrt(cues);
  if (format === 'vtt') return toVtt(cues);
  if (format === 'txt') return toTxt(cues);
  throw new Error(`Unsupported format: ${format}`);
}
