# Initial assessment: reference channel ("Z"-mask character), 2 Nov 2026

## 1. Reference inventory (details: `analysis/REFERENCE_INVENTORY.csv`)
- **Source:** Drive folder "fitness video" (owner harshkmr.official), downloaded with `gdown --folder` into `ref/raw/`.
- **Contents:** 10 Shorts plus 10 auto-generated SRTs. One SRT is a duplicate for R10. R01 has no SRT.
- **Format:**
  - All are 608x1080, except R09 and R10, which are 608x1064.
  - 30 fps, AV1 at 125–194 kbps, AAC stereo audio.
  - 34–56 s long (median ~48 s).
- **Quality limits:**
  - These are low-bitrate re-encodes, so fine texture, outline width and exact colours are approximate.
  - R09 and R10 have a grey horizontal bar burned in (a capture artifact, not the channel's style). It slightly biases those two videos toward "static".
- **No other assets:** there are no project files, fonts, music stems or assets from the channel. Everything visual must be measured from the video.
- **Coverage:** two formats are covered: "Let me fix that" problem/fix (R02, R05–R10) and age tier lists (R03, R04). R01 is a mixed listicle.
  - No long-form video, no comparison/myth format, no story format. Fine for Shorts.
  - The channel URL was not given, so it is unknown whether other styles exist. Ask the owner for the URL if needed.

## 2. What was measured (all local and deterministic, cached by sha1 + tool version)
- **Tools:**
  - `tools/inventory.py`: ffprobe metadata.
  - `tools/analyze.py`: per-frame measurements at native 30 fps on a 270x480 grid:
    - brightness, contrast, saturation and edges
    - frame diff and HSV-histogram cuts
    - LK + RANSAC similarity model (translation, scale, rotation) and object residual
    - audio RMS, silences, onsets and LUFS
    - SRT parse and words per minute
    - 6 s contact sheets at 2 fps
  - `tools/motion_events.py`: groups the frames into motion events (slide / zoom), with duration, travel and velocity profile.
  - `tools/overview.py`: one 1 fps sheet per video.
- **Run time:** about 14 s per video, 10 videos in total. Per-video results are in `analysis/R*/{frames.csv, shots.csv, audio.json, srt.json, summary.json}`.

## 3. First verified findings (provisional; full rulebook comes in Phase 6)
| Area | Finding | Evidence |
|---|---|---|
| Character | One 2D illustrated character: dark slate-grey body, white mask with a "Z", thin dark outline, soft cel shading. These are still images (a new drawing per pose), not rigged or 3D. | Overview sheets for all 10 videos; poses change by cut or slide, never by in-between frames |
| Background | Flat pastel (cyan #C0F5F8-ish, light lavender, light blue). Occasionally a yellow/cyan sunburst or a black spotlight for "reveal" beats. No scene geometry or depth. | Brightness 192–215 and saturation 29–105 per video; overviews |
| Motion language | Mostly still holds. Moving content in only 9–37% of frames. Movement comes from entrances: the subject **rises in from below with a fade-in and ease-out**. | 58 slide_up events in all 10 videos, median 0.23 s, travel ≥0.29 of frame height. The R07 9.37 s strip confirms it visually. |
| Zoom | Short punch zooms, median 0.2 s and ~4% scale. Most frequent in R09 and R10. | 50 zoom events |
| Horizontal slides | Used in the age tier lists (R03/R04: 8 each), when moving to the next item. | slide_left events |
| Cuts | 10–16 cuts per video (R03 has 54 in its rapid age list). Shots average 2.3–4.1 s. | shots.csv |
| Script | Hook (problem, 1 sentence) → "Let me fix that" at 2.6–7.6 s → "You only need N simple …" → #1/#2/#3 → "That's it." payoff, or "How old are you…?" comment bait. 162–214 wpm (median ~177). | srt.json for 9 videos |
| Text | Bold black sans headings at the top ("#1 Calorie Deficit", "FOREARMS ARE WEAK"), red emphasis word, words pop in one by one. Tiny white captions in the middle of the body. | Contact sheets R07/R09/R10 |
| Audio | Voice + music with almost no silence (0–0.39 s total per video). Loud master: -11 to -14 LUFS integrated. 30–53 sharp onsets per video (sfx and hits, not yet classified). | audio.json |

## 4. Proposed production architecture (decision doc comes in Phase 7)
The reference is **2D image compositing**: still character drawings, flat backgrounds, layer entrances and punch zooms. 3D is not needed.
| Option | Fit | Cost / complexity |
|---|---|---|
| **A. Our existing Reel Engine (Remotion), plus small patches (recommended)** | Already has image/pose layers, `up` entrance, punch camera, `rays` backdrop, typed text, captions and sfx. Needs an exact "rise-in" preset (ease-out curve + fade from measurements), word-pop headings and a flat pastel theme. | Lowest: already installed, scripted and validated on 4 of our videos |
| B. FFmpeg/Python compositor from scratch | Possible, but rebuilds what Remotion already does | Medium-high |
| C. Blender / Three.js | Real 3D camera and lighting, which this style does not use | High, no benefit |

Character: we keep **H** (our own character). We copy the production language, never the "Z" character or its drawings.

## 5. Estimated Claude usage by phase (relative)
- Phase 1–2: **done** (low; local scripts).
- Phase 3, style reverse engineering: **medium**. Needs about 10–15 targeted frame views plus text-only script analysis.
- Phase 4, frame blueprint for 3–4 representative scenes: **low-medium** (numbers come from the CSVs).
- Phase 6–7, rulebook and decision doc: **low**.
- Phase 8–9, 5–10 s reconstruction test and audit: **medium-high**. This is the most valuable phase: stills first, then a short preview.
- Phase 10–12, skill, full video, state files: **low-medium**.

## 6. Subagent plan
**None for now.** The measurements are deterministic scripts, and the remaining visual review is small. Splitting it would mean re-reading the same context several times.

One independent "verifier" agent may be worth it in Phase 9, to compare reference and reconstruction blind. That will be decided then.

## 7. Missing inputs / dependencies
- The channel URL, to check for styles missing from the 10 samples. Optional.
- An owner decision: keep **H** with our beige look, or switch to a flat pastel background like the reference? H stays either way.
- New H poses for the "rise-in" subjects the reference uses often: a hand showing 2/3 fingers, a fist, arms crossed with glasses, thumbs up, close-ups. Most already exist in the hero library. Check this per script.
- No paid tools or APIs are needed. Licensed music is still open (an owner item since October).
