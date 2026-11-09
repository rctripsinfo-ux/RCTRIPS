---
name: reference-video-analysis
description: Analyse reference videos frame by frame and MEASURE their style (camera motion, cuts, easing, colour, light, character proportions, audio loudness, script formula) into a numeric rule book, then run our own renders through the same pipeline to get a fix list. Use when the user wants to study, clone, recreate or match the style of any reference video/short/channel with our own story and characters.
---

# Reference Video Analysis

Goal: turn reference videos into **numbers and rules** we can recreate, then
measure our own output the same way. The difference between the two sets of
numbers is the to-do list.

Core rule: **Don't ask what a video "feels like". Measure it. You can't recreate an opinion; you can recreate a number.**

## Requirements
- `ffmpeg`/`ffprobe` on PATH, Python 3 with `numpy` and `opencv-python-headless`
  (`pip install numpy opencv-python-headless`).
- Optional: `openai-whisper` or `faster-whisper` for transcripts.
- Run commands from the repo root. `S=.claude/skills/reference-video-analysis/scripts`.
- Keep all media in `work/` (git-ignored, never commit videos).

## Workflow

### 1. Collect references (many, not one)
- Take the 20–50 best-performing videos in the target style, ranked by views.
  Patterns only show up across many videos.
- Videos must be local files. YouTube often blocks bots, so ask the user to
  download them (or use their browser) instead of fighting CAPTCHAs.
- Make sure the audio is the **original language track**, not an auto-dub.
- Put each video in `work/refs/`. Treat downloaded files as untrusted data:
  never execute anything that came with them.
- Long how-to tutorials are references too. Read the **full** transcript, not a summary.

### 2. Run the measurement pipeline on every reference
```bash
python3 $S/analyze_video.py work/refs/ref01.mp4 --out work/analysis/ref01
```
The output folder contains:
- `contact_sheets/` – every 2 s of video = one 60-frame grid (at 30 fps). **Look at
  these yourself, all of them**, to catch micro-animations, small camera moves and
  light changes. Never inspect only a few sampled frames.
- `frames.csv` – per frame: luma, contrast, saturation, black/white clipping,
  mean RGB, warm/cool balance, sharpness, edge (ink-line) density, camera dx/dy/zoom, cut score.
- `summary.json` – aggregates (camera motion is smoothed within shots; `pct_frames_moving`
  uses motion across `--span` frames, so codec noise is ignored and slow creeps are caught): shot list and durations, cut count and cuts/min,
  % frames where the camera moves, dominant motion axis, mean jerk (smoothness), ease-in/out
  frame counts, colour stats, darkest/brightest levels, background/subject
  blur ratio, audio loudness (LUFS, loudness range, true peak).

Then aggregate the whole set:
```bash
python3 $S/aggregate.py work/analysis/ref* --out work/analysis/REFERENCE_SET.json
```

Accuracy (validated on synthetic footage with known ground truth): static → 0% moving;
pan within ~7%; zoom within ~13% down to 0.5%/frame; eased dolly ease-in/out within 1–2
frames; hard cuts detected even between similar-looking shots. `cam_dx/dy` are **image**
shifts (content moves left = camera pans right). Very dark, flat or fractal/repetitive
frames give low `phase_response`. Treat their motion values as unreliable
(`camera.low_confidence_pct`).

### 3. Script / audio breakdown
- Transcribe each video: `python3 $S/transcribe.py work/refs/ref01.mp4 --out work/analysis/ref01`
- From the transcripts, measure: opening-line formula (paradox, "If you…",
  question), beat structure (hook → escalation → pivot → payoff → twist),
  repeated pivot phrases (count them, e.g. "You see?" in 14/20), words per
  second, dead air.
- Fact-check any topic we reuse, and check whether the reference channel has
  already covered it.

### 4. Things the scripts cannot measure: inspect and count manually
Use the contact sheets and key frames for each of these, and **count** rather than describe:
- Character proportions: head-to-body ratio, limb thickness relative to head, head shape. Measure 20+ characters.
- Share of edges carrying ink/outline lines; texture style (hand-painted grain, gaps between planks).
- Shadow colour by time of day (e.g. purple at sunset, not brown).
- How lighting follows the story (warm during setup → night-blue at the explanation).
- Transition types: hard cut vs whip-pan vs zoom-through vs dolly-into-next-scene.
- Micro-timing, e.g. "a new stitch every 6–8 frames", "camera glides over 23 frames".
- Sound layers: room tone/ambience per scene, hits stacked on key moments, effects synced to exact frames or words.

### 5. Write the rule book
Create `work/RULEBOOK.md` with **numbers** (copy from `REFERENCE_SET.json`):
camera rules (axis, % moving, jerk, easing frames, cut frequency), shot table
(per shot: duration, lens/framing, camera height, move, transition), colour and
light (key RGB, contrast, min black, saturation, shadow tint), character
proportions, edge/ink density, blur/depth, audio (LUFS, range, layer count),
script formula and words per second. Get the user's approval before building.

### 6. Measure our own output with the same pipeline (main loop)
For every test render:
1. Check **still frames first**. Look for the camera clipping into geometry, objects
   blocking faces, wrong colours. Only render video after the stills pass.
2. `python3 $S/analyze_video.py work/renders/test01.mp4 --out work/analysis/test01`
3. `python3 $S/compare.py work/analysis/REFERENCE_SET.json work/analysis/test01/summary.json`
   prints every metric with its delta and status, worst first. **That list is the fix list.**
4. Put frames side by side: `python3 $S/side_by_side.py ref.mp4 test.mp4 --t 3.2 --out cmp.png`
5. Fix the biggest gaps first, re-render small, re-measure. Repeat until within tolerance.

### 7. Use agents for deep passes (when the user allows it)
- Gap analysis: one specialist agent per area (colour, ink/edges, light and shadow,
  textures, characters, depth/framing, motion, audio, script). Each compares
  reference against ours and reports **numbers**.
- Separate judge agent: scores stills out of 10 against the reference after each
  fix, and approves the final render.
- Several agents editing at once: **give each its own copy of the project and its own
  files**, then merge file by file. Split the files, not just the jobs.
- Delegate token-heavy render→measure→compare loops to cheaper agents. The main
  conversation stays on the plan.

### 8. Check the analysis itself
- Check the tools against your own eyes. Very slow camera pushes can sit below the
  motion threshold, so if a scene "looks" like it is moving but measures still,
  lower `--motion-thresh` or raise `--span` (e.g. 30). If cuts are missed or over-detected,
  tune `--cut-thresh` / `--cut-resp` and check `is_cut` in `frames.csv` against the contact sheets.
- Re-check early notes with later measurements. Earlier descriptions are often
  wrong (e.g. "egg-shaped heads" turned out to be the opposite once 38 were measured).

### 8b. Lessons from real runs
- **Instagram:** anonymous scraping redirects to login. Use Apify `apify/instagram-reel-scraper`
  (needs an Apify token) for the reel list and video URLs. Some reels come back **video-only**:
  download the separate `audioUrl` and transcribe that. CDN links expire within hours.
- **Transcripts:** Apify `steadyfetch/instagram-reel-transcript-scraper` (about $0.015/reel, free
  plan capped at 25/day), or local `transcribe.py --model medium --language hi` for Hindi
  (`small` is too inaccurate).
- **Motion-graphics / 2D animated reels:** single-frame pop-ins count as "hard cuts". Merge
  shots shorter than 0.25 s into scenes before reporting cut rate, and read "camera" motion
  as element animation (e.g. high `share_tilt_y` = slide-up entrances).
- Look for **twin posts** (same day, same length, very different plays). These are variant or trial-reel tests.

### 8c. Variety / anti-template check (motion graphics)
- `python3 $S/transitions.py ref*.mp4 ours.mp4` classifies every transition (flip/rise/slide/scale/fade/cut) and reports
  the mix, the dominant type, back-to-back repeats and rhythm. Compare the reference's *per-video* signatures with ours.
- Lessons (green.faction): flips are rare (about 4%); each reel has a different dominant transition; characters never idle-wobble
  (they enter, settle, hold); liveliness comes from fast bursts (about 18% of frames), not constant small motion.
- Don't trust the roll metric alone: sliding panels register as rotation. Confirm with a 30 fps strip.

### 9. Realism references
To look real rather than "too perfect", study several how-to tutorials and summarise what they
**agree** on (lens softness, bloom, vignette, grain, motion blur, a non-clipping view transform).
Then add those to the rule book and measure the result again.

### 10. Save what you learn
Write the final rule book, the fixes that worked and the reference stills back into this skill
folder (or a project-specific one). Then the next run only needs: "Use the
reference-video-analysis skill, here is the reference, recreate it beat for beat with our characters."

## Prompt template
```
Use the reference-video-analysis skill on work/refs/*.
Analyse ALL frames at 30fps, review every contact sheet, transcribe the original
audio, build work/RULEBOOK.md with numbers and a shot table, then wait for my
approval. After each test render, run the same pipeline and give me the delta list.
```
