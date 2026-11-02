# Test segment rebuild summary

**Segment:** the first 16.9 s of the video (new frames 0-505): the hook, arrival, whale close-up, "it stinks", the
burial and tow ideas, and the engineer. It was chosen because it contains the worst gaps in a small render budget:
3 hard cuts inside one place, 2 place changes, the biggest bright sand areas, and the opening the user cares about.

**Files**
| File | What |
|---|---|
| `out/test_seg/test_segment_v6.mp4` (copy: `whale_short_test_segment_v6.mp4` in the repo root, git-ignored) | corrected segment with sound |
| `out/test_seg/v4_seg.mp4` | the same 506 frames of v4 (baseline) |
| `analysis/sbs_test.jpg` | reference still / v4 / v6 side by side |
| `analysis/data/m_v4seg.json`, `m_v6seg.json` | picture metrics (`analysis/measure.py`) |
| `analysis/v4_seg.mp4.cam.json`, `seg_v6.mp4.cam.json` | per-frame camera speed (`analysis/camfit.py`) |

## What changed (implementation)
| Fix | Where | What |
|---|---|---|
| F8 pacing | `scripts/voice_tight.py`, `src/videos/whale/timewarp.ts`, `Whale.tsx` | Narration re-voiced back to back (am_fenrir, 1.2x): **3.71 words/s**, 63.1 s (was 65.8 s). Breath gaps are 0.06-0.16 s, with one held beat for the blast. `timewarp.ts` maps old line starts to new ones. Every component evaluates the old timeline at `oldFrame(newFrame)`, so the whole picture follows the new voice without re-authoring. |
| F8 audio | `scripts/sound.py` | Every SFX/music time goes through the same warp (`wp()`). Music stays well under the voice (user decision). |
| F7 editing | `story.ts` shots 2-4 | The 3 hard changes inside the beach scene (aerial -> whale, whale -> man, man -> worker) are replaced by camera travel. Place changes 4 (tow) and 5 (engineer) use 6-frame dissolves (`XFADE`). Shots joined by travel share one world sun (`world.ts` `shotSun` link), so the light doesn't jump mid-move. |
| F7 speed | `story.ts` | First try: 30/22/16-frame travels peaked at 75-113 px/f (reference strong moves: ≤ ~38). Re-done as 56/66/34/30-frame glides. The aerial now ends on the land side so the camera never crosses the snout. |
| F12 sharpness | `story.ts` DOF | Lens blur on medium shots reduced from 10-14 px to 6-8 px. |
| G1 brightness | `grade.ts` GRADE_GOLDEN2 | Mid-tones pressed (0.54 -> 0.45 knot), darks deeper, saturation 1.08/1.22/1.15, vignette 0.32. |
| Asset | `world.ts` whaleGeo | Flat snout cap: the lathe pole made a star-shaped shading artefact when seen head-on. |
| Kept from the earlier session | `lights.ts`, `world.ts`, `cast.ts` | Late-afternoon "golden" light for the beach, denser sand texture (footprints, ripples), head sway. |

## Results (medians; reference = 38 approved stills, caption band masked)
| Metric | Reference | v4 segment | v6 segment | Moved toward reference? |
|---|---|---|---|---|
| Mean luminance | 0.366 | 0.658 | **0.522** | yes, gap -47 % (still too bright) |
| Darkest 2 % (p2) | 0.085 | 0.205 | **0.116** | yes, gap -74 % |
| Dark mass (< 0.12) | 0.075 | 0.012 | 0.022 | yes, a little (still 3.4x short) |
| Saturation | 0.467 | 0.393 | **0.482** | **closed** (+3 % over the reference) |
| Colourfulness | 0.272 | 0.320 | 0.298 | yes |
| Edge density | 0.099 | 0.061 | 0.066 | barely (still 0.67x) |
| Fine detail | 0.017 | 0.014 | 0.012 | **no** (worse) |
| Sharpness (Laplacian var.) | 0.009 | 0.005 | 0.003 | **no** (worse) |
| Narration speed | 3.5-4.1 w/s (UNVERIFIED) | ~3.5 with 8.6 s of pauses over the full video | **3.71 w/s, < 1 s of pauses** | yes |
| Hard changes inside a place | 0-1 per video (UNVERIFIED) | 3 (+2 place cuts) | **0** (+2 dissolves, 2 flashes) | yes |
| Camera hold / drift / move | 10 / 24 / 65 % (UNVERIFIED) | 0 / 40 / 60 % | 0 / 32 / 68 % | move share yes; we still never hold |
| Median camera speed | 3.6 px/f (UNVERIFIED) | 2.29 | 3.77 | yes |
| p90 camera speed | 16.9 px/f (UNVERIFIED) | 12.7 | 26.8 | **overshoot**: travel too fast near the whale |

## Verdict on the segment
- **Better:** pacing (no dead air), continuity (no cuts inside the beach scene), saturation, darks, warmth, mood.
- **Not better or worse:** sharpness and fine detail went down, because the darker grade and the warm haze soften
  edges. The whale's shaded side turns a flat saturated blue that reads worse than v4 (see `sbs_test.jpg`, column 3).
  Two travel moves still peak at 56-100 px/f (frames 202-222 and 284-304), so they are still too fast.
- **Not touched in this pass:** world detail density (the reference frames are full of buildings, signs and props),
  character idle acting beyond head sway, the explanation section, the ending.
