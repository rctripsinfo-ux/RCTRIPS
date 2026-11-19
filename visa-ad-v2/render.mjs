// node render.mjs [--stills=1,2,3]  -> out/visa-ad-final.mp4 (or out/stills/*.jpg)
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('/opt/node22/lib/node_modules/playwright');
import { execFileSync } from 'node:child_process';
import { mkdirSync, rmSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const stills = process.argv.find(a => a.startsWith('--stills='));
const dir = path.join(here, 'out', stills ? 'stills' : 'frames');
rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
const browser = await chromium.launch();
const M = process.argv.includes('--music');
const url = pathToFileURL(path.join(here, 'index.html')).href;
const open = async () => { const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } }); p.on('pageerror', e => console.error('PAGE', e.message)); await p.goto(url); await p.evaluate(() => window.READY); return p; };
const warpArg = process.argv.find(a => a.startsWith('--warp='));
const WARP = warpArg ? JSON.parse((await import('node:fs')).readFileSync(warpArg.slice(7), 'utf8')) : null;
const toOrig = t => { if (!WARP) return t; const [o, v] = [WARP.orig, WARP.out]; if (t <= v[0]) return o[0]; for (let i = 1; i < v.length; i++) if (t <= v[i]) return o[i - 1] + (o[i] - o[i - 1]) * (t - v[i - 1]) / (v[i] - v[i - 1]); return o[o.length - 1]; };
const p0 = await open(); const total = WARP ? Math.round(WARP.total * 30) : await p0.evaluate(() => Math.round(TL.total * 30));
const list = stills ? stills.slice(9).split(',').map(Number) : [...Array(total).keys()];
const pages = [p0, ...await Promise.all([...Array(Math.min(5, list.length - 1))].map(open))];
let next = 0, done = 0;
await Promise.all(pages.map(async pg => { while (next < list.length) { const f = list[next++]; await pg.evaluate(([n, g]) => window.seek(n, g), [toOrig(f / 30) * 30, f]);
  await pg.screenshot({ path: path.join(dir, String(f).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 93 }); if (++done % 150 === 0) console.log('frames', done, '/', list.length); } }));
await browser.close();
if (!stills) {
  const od = WARP ? path.join(here, 'eleven') : path.join(here, 'out'); const out = path.join(od, WARP ? 'visa-ad-eleven-final.mp4' : 'visa-ad-v2-final.mp4');
  const args = ['-y', '-v', 'error', '-framerate', '30', '-i', path.join(dir, '%05d.jpg')];
  if (existsSync(path.join(od, 'audio.wav'))) args.push('-i', path.join(od, 'audio.wav'), '-c:a', 'aac', '-b:a', '192k', '-shortest');
  args.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out);
  execFileSync('ffmpeg', args, { stdio: 'inherit' }); console.log('done', out);
}
