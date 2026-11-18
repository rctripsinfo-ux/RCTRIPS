# Remotion playbook (for Claude)

## Scaffold (once per workspace)
```bash
npx --yes create-video@latest work/remotion --template blank --no-git   # if flags fail, run interactively and pick "Blank"
cd work/remotion && npm i && npm i @remotion/google-fonts @remotion/media-utils
```
Put media the composition needs in `work/remotion/public/` (copy `cut.mp4`, music, sfx, logo, b-roll there).

## Build (per video)
1. Copy `work/<project>/cut.mp4` → `public/main.mp4`; read `cut_words.json`.
2. Write `src/data.json`: `{ fps, width, height, durationInFrames, words, edits }` where `edits` is your plan:
   - `zooms`: `[{from, to, scale}]` on key lines (per STYLE.md)
   - `popups`: `[{at, type, text|icon|image}]` when numbers/apps/lists are mentioned
   - `broll`: `[{from, to, src}]`
   - `sfx`: `[{at, src, volume}]` aligned to cuts, pop-ups, caption hits
   - `music`: `{src, volume, duckTo}`
3. Components (one file each, small and reusable — later videos reuse them):
   - `Main.tsx` — `<OffthreadVideo src={staticFile('main.mp4')}/>` wrapped in zoom transform (interpolate + spring).
   - `Captions.tsx` — group words per STYLE.md, show active group, highlight rule, entry animation via `spring()`.
   - `Popup.tsx`, `BRoll.tsx`, `Hook.tsx`, `ProgressBar.tsx` as the style needs.
   - Audio: `<Audio>` for music (volume callback lowers it while words are active) and each SFX in a `<Sequence>`.
4. Register composition in `src/Root.tsx` with values from `data.json`.
5. Preview stills first (cheap):
   `npx remotion still src/index.ts Main ../../work/<project>/preview_%d.png --frame=<n>` for 4–6 key frames → look at them, fix layout.
6. Full render:
   `npx remotion render src/index.ts Main ../../exports/<project>_v1.mp4 --codec=h264 --crf=18`
7. Loudness check: `ffmpeg -i exports/<project>_v1.mp4 -af ebur128 -f null -` → target about -14 LUFS; if off, re-render with adjusted volumes or run `loudnorm`.

## Speed tips
- Reuse components from previous projects; only `data.json` changes per video.
- Use `--concurrency` = CPU cores / 2 on slow laptops; `--scale=0.5` for quick full previews.
- Re-render only after reviewing stills.
