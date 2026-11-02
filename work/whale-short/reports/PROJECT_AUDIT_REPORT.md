# Project audit report

Date: 2026-11-02. Scope: the `cartoon-3d-short` skill (`.claude/skills/cartoon-3d-short/`) and our whale project
(`work/whale-short/`).

## 1. What exists

### Reference material (in the skill)
| Item | Count | What it actually is | Usable for |
|---|---|---|---|
| `references/frames/*.jpg` | 38 | 540x960 JPEG stills, frames 60 and 180 of 20 shorts (2 missing) | colour, contrast, edges, detail, framing |
| `references/sheets/*_sheet.jpg` | 20 | 1800x1920, 10x6 tiles of 180x320. **One whole video per sheet, tiles ~1 s apart** | pacing (how often the picture changes), shot variety |
| `references/reports/*.md` | 8 | earlier agent reports (characters, depth, grade, lighting, motion, outlines, textures, CONTEXT) | numbers measured on the full videos by the skill author |
| `references/STYLE_BIBLE.md` | 1 | summary: format, script formula, voice, captions, camera | rules |

### Not present (claimed by the skill docs)
| Item named in SKILL/CONTEXT/STYLE_BIBLE | Status |
|---|---|
| `references/vids/*.mp4` (the 20 reference videos, 720p) | **missing**: not shipped in the repo |
| `references/measure/*_sheets/sNN.jpg` (2 s = 60 consecutive frames) | **missing** |
| `references/tx/` transcripts, `measure/summary.json` | **missing** |
| Kenney CC0 models (`bridge/kenney/*.glb`) | **missing**; kenney.nl returns 403 from this container |

**Consequence:** frame-by-frame motion analysis (optical flow, phase correlation, cut detection, text timing, audio cue
timing) **cannot be redone on the reference** with what we have. Every motion/timing number about the reference in
this audit comes from the skill author's earlier reports and is marked *unverified (prior report)*. The user should
supply the 20 videos (or their URLs) to close this.

### Transcripts / SRT
- `/root/.claude/uploads/.../bd6e918e-download_6.txt`: transcript of the *tutorial* video (how the skill was made).
  It is not a reference-short transcript.
- No transcripts of the 20 reference shorts are available.

### Our project (`work/whale-short/`)
| Area | Files |
|---|---|
| Script + facts | `SCRIPT.md` (fact-checked; one unverified detail, "whale of a deal", left out) |
| Voice | `scripts/voice.py` (v1, am_michael 1.3x), `scripts/voice_fit.py` (am_fenrir fitted to the v1 line slots; writes `voice/words.json` and `src/videos/whale/words.ts`) |
| Sound | `scripts/sound.py` (synth SFX + original march, ducked) -> `public/whale/mix.wav` |
| Scene code | `src/videos/whale/`: `story.ts` (timeline, 18 shots, 34 framings, DOF, kicks, foreground props), `world.ts` (beach world, whale, cars, props, sea, sky, lamps, stars), `cast.ts` (staging, crowd, effects), `toon.ts` (character drawing, from the skill), `fx70.ts` (our effect cards), `Whale.tsx` (composer + captions), `ink/lensblur/grade/shade/cardshade/lights/paint/build.ts` (from the skill, light edits) |
| Render | `scripts/render.mjs`, `scripts/render_all.sh` (chunks of 250 f), `scripts/stills.mjs`, `scripts/env.sh` (Playwright headless shell + SwiftShader) |
| QA | `scripts/sheet.py` (contact sheets), **new** `analysis/measure.py` (metrics, this audit) |

### Generated outputs
| File | What |
|---|---|
| `out/final/whale_short_final.mp4` | v1: 810x1440 upscaled, am_michael voice |
| `out/final2/video.mp4` | picture of v2-v4 (1080x1920 native) |
| `out/final2/whale_short_v2.mp4` | v2: recognisable whale/gulls, framing pass |
| `out/final2/whale_short_v3.mp4` | v3: am_fenrir voice |
| `out/final2/whale_short_v4.mp4` | v4: music lowered, new hook (current) |
| `out/test_seg/seg_v_new.mp4` | corrected test segment (this task, frames 0-269) |

## 2. What was analysed before, and how well
| Earlier claim | Evidence quality |
|---|---|
| Colour/edge/detail targets in reports | measured by the skill author on full videos; **re-checked here on 38 stills** (Section 2 of the gap report) |
| "Camera holds ~80 % of frames" (STYLE_BIBLE) vs "camera moving 65 % of frames, slow push-ins" (motion.md) | **contradictory** prior reports; cannot be re-measured without the videos |
| "Hard cuts almost never: 0-1 per video in 12/20" (STYLE_BIBLE) vs "big reframes are cuts" (motion.md recipe) | **contradictory**; the STYLE_BIBLE statement is a direct measurement, the motion.md line is a recipe for the bridge |
| Captions: one word at a time, white bold, black outline, 60-74 % height | visible in all 38 skill stills (verified per file). The user's 88-frame set reportedly has none and was not available; captions are not used. |
| Voice 3.5-4.1 w/s, < 1 s of pauses per video; music 5-10 dB under speech | prior report, unverified |

## 3. Assumptions we made (and status)
| Assumption | Status |
|---|---|
| Skill author's rule "no captions" applies to us | **kept.** The user didn't ask for captions; the test-segment captions were added without permission and are now disabled |
| Bright midday beach is fine | **refuted** by measurement: our mean luminance 0.63 vs reference 0.37 |
| Billboard 2D characters are acceptable | consistent with the reference (it also uses flat cards) |
| Word timings for captions | **estimate**: syllable-weighted inside each measured speech span; no forced aligner available |
| Our music level (user asked: much lower) vs reference (5-10 dB under speech) | **conscious deviation**: user preference wins |

## 4. Unverified items that block "exact match" claims
1. Reference camera motion curves, move/hold ratio, transition types (needs the videos).
2. Reference caption timing relative to word onsets (needs the videos + audio).
3. Reference audio mix levels (needs the audio).
4. Exact word timing of our captions (needs a forced aligner, e.g. whisperX; not installable offline here).
