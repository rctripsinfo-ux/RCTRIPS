# Blunderloop nightly short: procedure for the scheduled night session

Goal: one finished vertical short (1080x1920, ~55-65 s) ready to upload by 12:00 IST, in the exact style of
`work/whale-short` (the approved first video, v7). Work alone, without questions. Keep usage low: reuse the engine,
check stills at low resolution, render once.

## 0. Setup (fresh container)
1. Repo `rctripsinfo-ux/RCTRIPS`, branch `claude/intelligent-euler-6jm4o0` (add_repo if it is not attached).
2. `cd work/whale-short && npm ci` (node_modules is not committed).
3. `pip install -q kokoro-onnx soundfile scipy`, then download the voice model into `work/whale-short/models/`:
   `kokoro.onnx` and `voices.bin` from github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/
   (`kokoro-v1.0.onnx`, `voices-v1.0.bin`).
4. Rendering: `scripts/env.sh` points Remotion at the Playwright headless shell with `gl: swangle`. If the path
   differs, `ls -d /opt/pw-browsers/chromium_headless_shell-*/*/` and fix `scripts/env.sh`.
   Read `work/whale-short/NOTES.md` (cloud lessons: hand-built composer, dpr = scale).

## 1. Topic + facts (pick ONE, check it is not in `work/shorts/TOPICS.md`)
- A true story where a plan backfired, absurd and visual, physical cause and effect, nobody (or almost nobody) died.
- Check every fact with web search (2-3 reliable sources). Jokes must be real facts. Write `SCRIPT.md` with sources.

## 2. Script (cartoon-3d-short formula, `.claude/skills/cartoon-3d-short/SKILL.md`)
Hook = absurd fact in line 1. Setting, then 3-4 escalating beats, the break, "Luckily ... / Unluckily ...", "You see,"
plus an everyday analogy, the consequence, and a callback twist as the last line. 190-230 words, English, no emojis.

## 3. Project
- Copy the engine: `cp -r work/whale-short work/shorts/<YYYY-MM-DD>-<slug>` WITHOUT node_modules/out/models
  (symlink `node_modules` and `models` to the whale ones).
- Keep untouched: `ink.ts lensblur.ts grade.ts shade.ts cardshade.ts lights.ts paint.ts toon.ts build.ts Whale.tsx`
  (rename the composition), `timewarp.ts` mechanism, `scripts/*`.
- Rewrite for the story: `story.ts` (shots, cameras, DOF, kicks), `world.ts` (the set; procedural props only, no
  external models), `cast.ts` (staging), `fx70.ts` (effects).
- House rules (user decisions): clean CUTS between angles, only slow push-ins inside a shot (no fast flying camera);
  opening = close-up of the main character's shocked face (it is the thumbnail); pale reference-style heads; front
  views in close-ups; nobody half-cut at the frame edge; golden afternoon or night moods; NO captions; music well
  under the voice.

## 4. Voice + sound
- Voice am_fenrir via `scripts/voice_tight.py` (back-to-back lines, 3.6-3.9 words/s, ~1 s held beat only on the big
  moment). Then `scripts/sound.py` (adapt the SFX event times to the new story).

## 5. Check before rendering
- Stills at dpr 0.5 of every shot (`scripts/stills.mjs`), contact sheet (`scripts/sheet.py`), look at them. Fix framing,
  blocked faces, unreadable subjects. Max 2 still rounds.

## 6. Render + deliver
- `scripts/render_all.sh` (edit paths/frame count), concat, mux the mix, loudnorm -14 LUFS, 1080x1920.
- Quick QA: blackdetect, 12-frame contact sheet.
- Deliver: SendUserFile the mp4 (status proactive) with a plain title (clear, to the point, no emojis) and a description
  (no emojis, ends with "Subscribe to Blunderloop for more true stories that went hilariously wrong." and 5 hashtags).
  If Google Drive tools are available, also upload the mp4 + `UPLOAD.md` to a Drive folder "Blunderloop daily".
- Add the topic to `work/shorts/TOPICS.md`, commit the project source (never the mp4) and push.
- If anything blocks the video, still deliver what exists (script + voice) and say exactly what failed.
