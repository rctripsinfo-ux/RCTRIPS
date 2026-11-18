import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkExtractor, getInfo, getSubtitleSource, listVideos, publicInfo } from './lib/extractor.js';
import { convert } from './lib/subtitles.js';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), 'public');
const HOST = process.env.HOST || '127.0.0.1';
const PORT = Number(process.env.PORT || 3000);
const FORMATS = new Set(['srt', 'vtt', 'txt', 'words']);
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

function validUrl(raw) {
  try {
    const u = new URL(String(raw || '').trim());
    return ['http:', 'https:'].includes(u.protocol) ? u.href : null;
  } catch {
    return null;
  }
}

function sendJson(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(body));
}

function safeName(s) {
  return s.replace(/[\\/:*?"<>|\x00-\x1f]+/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 120) || 'subtitles';
}

async function readBody(req) {
  let data = '';
  for await (const chunk of req) {
    data += chunk;
    if (data.length > 10000) throw Object.assign(new Error('Request too large'), { status: 413 });
  }
  return JSON.parse(data || '{}');
}

async function serveStatic(req, res, pathname) {
  const rel = normalize(pathname === '/' ? '/index.html' : pathname).replace(/^(\.\.[/\\])+/, '');
  const file = join(ROOT, rel);
  if (!file.startsWith(ROOT)) return sendJson(res, 403, { error: 'Forbidden' });
  try {
    const body = await readFile(file);
    res.writeHead(200, { 'Content-Type': MIME[extname(file)] || 'application/octet-stream' });
    res.end(body);
  } catch {
    sendJson(res, 404, { error: 'Not found' });
  }
}

const server = createServer(async (req, res) => {
  const { pathname, searchParams } = new URL(req.url, 'http://localhost');
  try {
    if (pathname === '/api/info' && req.method === 'POST') {
      const url = validUrl((await readBody(req)).url);
      if (!url) return sendJson(res, 400, { error: 'Please enter a valid http(s) video link.' });
      return sendJson(res, 200, publicInfo(await getInfo(url)));
    }

    if (pathname === '/api/list' && req.method === 'POST') {
      const body = await readBody(req);
      const url = validUrl(body.url);
      if (!url) return sendJson(res, 400, { error: 'Please enter a valid channel or playlist link.' });
      const limit = Math.max(0, Math.min(5000, Number(body.limit) || 0));
      const allowed = ['videos', 'shorts', 'streams'];
      const sections = (Array.isArray(body.sections) ? body.sections : ['videos']).filter((x) => allowed.includes(x));
      return sendJson(res, 200, await listVideos(url, { limit, sections: sections.length ? sections : ['videos'] }));
    }

    if (pathname === '/api/subtitle' && req.method === 'GET') {
      const url = validUrl(searchParams.get('url'));
      const track = searchParams.get('track') || '';
      const format = searchParams.get('format') || 'srt';
      if (!url || !/^(manual|auto|translated):[\w.@-]{1,40}$/.test(track) || !FORMATS.has(format)) {
        return sendJson(res, 400, { error: 'Invalid request parameters.' });
      }
      const { info, track: t, text } = await getSubtitleSource(url, track);
      const out = convert(text, format);
      const inline = searchParams.get('inline') === '1';
      const ext = format === 'words' ? 'words.srt' : format;
      const name = `${safeName(info.title)}.${t.lang}${t.kind === 'manual' ? '' : `.${t.kind}`}.${ext}`;
      res.writeHead(200, {
        'Content-Type': `${format === 'vtt' ? 'text/vtt' : 'text/plain'}; charset=utf-8`,
        'Content-Disposition': `${inline ? 'inline' : 'attachment'}; filename="${name.replace(/[^\x20-\x7e]/g, '_')}"; filename*=UTF-8''${encodeURIComponent(name)}`,
        'Cache-Control': 'no-store',
      });
      return res.end('﻿' + out);
    }

    if (pathname === '/api/health') {
      try {
        return sendJson(res, 200, { ok: true, ytdlp: await checkExtractor() });
      } catch (e) {
        return sendJson(res, 500, { ok: false, error: e.message });
      }
    }

    if (req.method === 'GET') return serveStatic(req, res, pathname);
    sendJson(res, 405, { error: 'Method not allowed' });
  } catch (e) {
    const status = e.status || (e instanceof SyntaxError ? 400 : 502);
    sendJson(res, status, { error: e.message || 'Something went wrong' });
  }
});

server.listen(PORT, HOST, async () => {
  console.log(`SubGrab running at http://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT}`);
  try {
    console.log(`Using yt-dlp ${await checkExtractor()}`);
  } catch (e) {
    console.warn(`WARNING: ${e.message}`);
  }
});
