# Remotion playbook (for Claude)

## Scaffold (once per workspace) — use the bundled template, don't write from scratch
```bash
cp -r SKILL_DIR/template work/remotion && cd work/remotion && npm i
```
Template = tested, data-driven edit: `src/Main.tsx` (zooms, captions, hook title, progress bar, SFX), `src/data.json` (the only file that changes per video), `public/` (local fonts + whoosh/pop SFX).

Rules learned from testing:
- **Copy** media into `public/` (symlinks return 404 in the Remotion server).
- Fonts must be **local files** in `public/` loaded with `@font-face` + `staticFile()` (Google Fonts CDN can fail behind proxies/offline). To add a font: download the latin `.woff2` from fonts.googleapis.com CSS, put it in `public/`, add to the `@font-face` block in `Main.tsx`.
- If Remotion can't download its browser, pass `--browser-executable=<path to Chrome/Chromium>`.

## Build (per video)
1. Normalise audio while copying the cut: 
   `ffmpeg -y -i work/<project>/cut.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k work/remotion/public/main.mp4`
2. Write `src/data.json`:
   ```json
   {"fps":30, "duration":<cut seconds>,
    "hook":{"text":"...", "s":0, "e":3.5},
    "zooms":[{"s":..,"e":..,"scale":1.18}],
    "captions":[{"s":..,"e":..,"words":["TWO","WORDS"],"hi":[1]}],
    "sfx":[{"at":..,"src":"whoosh.wav","volume":0.35}]}
   ```
   - **Captions**: write clean text yourself from `cut_words.json` timings — fix misheard words/brand names; script per user (Hinglish = Latin letters). 2–3 words per group, start = first word start, end = next group start (or last word end + 0.6 s). `hi` = indexes of highlight words (keywords, numbers, brands).
   - **Zooms**: 5–8 per minute on the punchiest lines (scale 1.12–1.2, ~1–1.5 s). Add a whoosh at each zoom start.
   - **Hook**: 1-line curiosity title for the first ~3.5 s.
3. Match STYLE.md by editing constants in `Main.tsx` (colours, font, caption `top`, size, stroke, animation). Keep text inside the safe zone.
4. Preview stills (cheap): `npx remotion still src/index.ts Main ../<project>/s_<f>.png --frame=<f>` for 4 frames (hook, a zoom, mid caption, end). Frame must be < duration×fps. Look at them; fix before full render.
5. Full render: `npx remotion render src/index.ts Main ../../exports/<project>_v1.mp4 --codec=h264 --crf=20 --concurrency=<cores>`

## Extending the look (when STYLE.md needs it)
Add small components next to `Main.tsx` and drive them from `data.json` (e.g. `popups:[{at,type,text}]`, `broll:[{s,e,src}]`, `music:{src,volume}` with volume lowered while captions are active). Keep everything data-driven so the next video only changes `data.json`.
