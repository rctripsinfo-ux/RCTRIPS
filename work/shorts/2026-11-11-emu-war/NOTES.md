# The Day Oregon Blew Up a Whale (cartoon-3d-short skill)

Original 66 s short, built from the `cartoon-3d-short` skill's bridge template (three.js + Remotion).

- Script and facts: `SCRIPT.md`. Voice: `scripts/voice.py` (Kokoro am_michael, 1.3x) -> `voice/voice.wav`, `voice/lines.json`.
- Shots, camera, timing: `src/videos/whale/story.ts`. World: `world.ts`. Cast and effects: `cast.ts`, `fx70.ts`.
- Sound: `scripts/sound.py` -> `public/whale/mix.wav` (synthesised SFX + original march, ducked under the voice).
- Stills: `. scripts/env.sh; PROPS='{"post":{"dpr":0.5}}' node scripts/stills.mjs WhaleShort out/x_ 100,400 0.5`
- Render: `scripts/render_all.sh` (810x1440 chunks), then concat, mux the mix, upscale to 1080x1920.

Cloud-container lessons (no GPU):
- Use the Playwright headless shell with `gl: "swangle"` (`scripts/env.sh`); Remotion's own browser had no WebGL.
- The `@react-three/postprocessing` `<EffectComposer>` renders nothing there: Whale.tsx builds the postprocessing
  composer by hand (RenderPass -> InkPass -> lens pre -> lens main -> bloom + tone map + grade).
- R3F clamps dpr to >= 1, so pass `inputProps.post.dpr` with the same value as `--scale` to really render smaller.
  Scale must give integer sizes (0.75 -> 810x1440). ~3 s/frame at 0.75 on 4 CPUs.
