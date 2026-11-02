# NEXT_STEPS (in order; each step is bounded)
1. **Phase 3, remaining style details.** Use targeted views only, about 10 frames in total.
   - **Typography:** heading font, weight, colour hex, size as a fraction of frame height, y position; the red emphasis word; caption size and position. Use 2 full-res frames each from R07 and R09.
   - **Word-pop timing:** heading words vs SRT cue times. Script: diff spikes inside the heading box vs `srt.json`.
   - **Sfx classes:** classify the onsets at cut / rise-in times (whoosh vs pop vs hit) by spectral centroid. Small script.
   - **Palette:** k-means on the backgrounds of all 10 videos. Script.
2. **Phase 4.** Write a scene spec JSON for 3 scenes: R07 0–3 s (hook), R07 9.4–11 s (rise-in + word pop), R09 13–18 s (equation icons).
3. **Phase 6–7.** Write `CHANNEL_STYLE_RULEBOOK.md` (verified / estimated / hypothesis sections) and a 1-page tech decision.
4. **Phase 8.** Patch the Reel Engine:
   - a `rise` entrance (ease-out between sine and quad, ~0.25–0.3 s, travel ≥0.3 H, fade-in over 2 frames)
   - a word-pop heading
   - a white theme (owner, 2 Nov)
   Then rebuild ~8 s of R07's structure with H and our own words. Stills first, then the preview.
5. **Phase 9.** Compare reference vs ours with the same `analyze.py` metrics (event durations, velocity curves, holds, cut rate).
6. ~~Owner decisions~~ Done 2 Nov: white background, channel = Zenox (complete coverage).
7. **Measure in R05:** is the push-up a pose swap or a sprite animation? Count distinct drawings over 21–28 s using a frame-diff + perceptual-hash script.
