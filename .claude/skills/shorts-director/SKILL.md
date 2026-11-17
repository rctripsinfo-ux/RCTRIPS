---
name: shorts-director
description: Make an Effortless Exercise YouTube Short (9:16, 30 fps, character H) with the in-repo PIL+ffmpeg compositor work/director.py, using the stage+layers system and the effects library (circle inset badges, blinking muscle colour, discs + whole-frame dim, focus blur, label boxes, dashed arcs, particles, typewriter cursor, squash / brush / iris transitions), then run the full-frame QA check. Use when the owner asks for a new Short or demo "like Demo 03", wants an effect added to the engine, or asks to check every frame of a rendered video for clipping.
---

# Shorts director (Effortless Exercise)

Repo `rctripsinfo-ux/RCTRIPS`, work in `work/`. Reference plan to copy from: `work/demo03_plan.py`.
Research behind it: `work/research/EFFECTS-LIBRARY-36-VIDEOS.md` (36 competitor Shorts, measured) and
`work/research/REFERENCE-c01-BREAKDOWN.md`. The house style (not the competitor's look) is in
`work/research/CREATIVE-SYSTEM-PLAN.md`; follow it once the owner approves it.

## THE METHOD (owner, 15 Nov 2026: "all videos totally amazing, always make them this way")
Reference: `work/week1/day02_plan.py` … `day07_plan.py`, with the shared helpers in `work/week1/w1.py`. Day 1 = `work/pilot3_plan.py`.
Owner feedback that shaped it:
- poses must ANIMATE in every scene (2–4 poses per scene, from frame 1)
- labels never on a face, never over another label, never left over a new picture
- 3+ labels at once: blur the picture behind them
- white set, Mini-H commentator, small captions, punchy hook in the first second

Steps for a new day N (one video ≈ 25–40 min):
1. **Script.** Take Day N from `work/content/30-DAY-SHORTS-PLAN.md` and write it to `work/weekX/dayNN.txt`, one line per speaker (`H: …` / `M: …`).
2. **Voices.** `python3 tools/dialogue_voice.py dayNN weekX/dayNN.txt '{"line": gap}'`. H = Fenrir deep/calm, Mini-H = Puck high/fast. Output: `voice/dayNN_cut.wav` + words.json. It starts the Reel Engine server itself.
3. **Images (Codex, see CLAUDE.md):** `weekX/img/run.sh` + `launch.py jobs.tsv` (3 jobs in parallel, ~1 min each).
   - **Gesture library, reuse it:** `week1/img2/g_*_al.png` has 12 talking poses on ONE canvas (point, cross, shrug, think, thumbs, one, two, palm, facepalm, shock, hips, flex). They swap in place.
   - **Topic poses:** make the base with H as reference, then variants with "The exact same image as the reference … The ONLY change: …".
   - Align with `tools/align_to.py base.png outdir var1.png var2.png` (`--height` for walking).
   - Cut-outs: `tools/cutout_white.py`. Mini-H stickers: `tools/sticker_ring.py`.
   - Red-muscle blink: `tools/highlight_merge.py` + layer `highlight=dict(base, asset, at)`.
4. **Plan.** Copy a `week1/dayNN_plan.py`.
   - `act([(pose, word), …])` = one H layer that changes pose on words.
   - `full()` = a single picture (82% size, the top stays free for labels).
   - `body()` = line-ups. `mini()` = cameo with focus blur.
   - `lab()` / `stack()` = labels. `card()` = dark-slate "#N" card.
   - `hook_keys()` = 2x blurred zoom-out on frame 1 + `shake` + whoosh_big.
   - Split a scene whenever the picture changes, so labels never stay over a new picture.
   - Use `until=` on labels that should replace each other.
   - The engine places labels automatically (`place()`: off faces, figures, captions and other labels). 3+ live labels → the picture behind is blurred. `fixed=True` keeps a hand-set spot.
5. **Render.** `LUFS=-20 python3 weekX/dayNN_plan.py` → `final/dayNN.mp4`.
6. **QA.** `python3 tools/label_qa.py weekX/dayNN_plan.py sheet.jpg`.
   - Fix real FACE / LABEL / OUTSIDE flags (look at the sheet; small FACE values near raised fists are usually false alarms).
   - Then look at 10 frames.
7. **Thumbnail.** Brand colours dark red #7A1A1A + teal #0F8B85 + white italic words; the layout varies (thumbnail skill). Codex 1080x1920.
   - `tools/append_thumb.sh final/dayNN.mp4 thumb.png final/dayNN_upload.mp4` puts it in the last frame.
8. **Upload text.** Title, description and tags in the style of `work/content/week1_upload.md`.
9. **Commit EVERYTHING**, Codex images included (the owner asked on 15 Nov, so other clouds can rebuild). Push to the session branch.

## THE LONG METHOD (16:9 long videos; owner approved demo v2.1 on 17 Nov 2026: "good now its better")
Reference: `work/long03/long03_plan.py` (demo). Research and specs: `work/research/LONGFORM-24-ANALYSIS-AND-PLAN.md` (D6 spec) and `LONGFORM-ANALYSIS-PROMPT.md` (QA protocol).

**Owner rules**
- **The CHARACTER explains everything through POSES.**
  - Never a still image that only moves with the camera.
  - Charts are only small support.
- **Rooms are EMPTY backdrops, and H is a set of cut-out poses on top.**
  - Codex cannot redraw "the same room, only H changes".
- **One base per set.** Every pose set comes from one base image ("The exact same image as the reference … ONLY change: …").
  - Standing poses use `week1/img2/g_base.png`.
  - Push-ups use `long03/img/pu_top.png`.
  - The bed uses `long03/img/bed_base.png`.
- **Alignment:**
  - Align with `tools/align_to.py base outdir vars --noscale`.
  - Big props (bed) need edge phase-correlation instead, plus `NOCROP=1 tools/cutout_white.py`.
- **Text:**
  - No burned-in captions (`cap_mode="none"`, upload an SRT instead).
  - Kinetic italic words with no boxes. A word that gets replaced uses `until=` and vanishes at once.
- **Never on screen:** a label on a face, text over text, Mini-H covering anyone, cut heads or feet, two poses at once (no dissolve; use `pose_pop`), frozen H (`puppet=True`), or more than ~1 s of an empty half-frame.
- **Layout and timing:**
  - Mini-H stays in front (z=3). Charts stay visible in Mini's scenes (`at=-5`).
  - Section cards are dark red `#7A1A1A`, at least 1.4 s. Add a voice pause after "Day N." when needed.
- **Pacing:** a pose change every ~0.6–1 s; context montages are quick cuts of 0.5–0.7 s with rep loops.
- **Audio:** `LANDSCAPE=1`, `LUFS=-14`, music 11 dB under the voice.

**Steps**
1. Script plus beat sheet: one visual beat per 3–4 s, and an acting pose for every line.
2. Voice: `tools/long_voice.py` or `dialogue_voice.py` with `TTS_MODEL=gemini-3.8-flash-tts` (the old model's free tier is 10 requests a day).
3. Codex pose sets, then align and cut out.
4. Plan, then stills.
5. Render.
6. QA every frame:
   - flicker and jump scan
   - a 0.25–0.3 s contact sheet
   - exact-frame checks on every fix
7. Thumbnail 1280x720 in brand colours, upload text with chapters, SRT. Commit everything.

## Owner rules (always)
- Reply to the owner in Hinglish. Scripts, titles and prompts are in English.
- Keep usage low: no subagents, no renders that aren't needed.
- Never cut a face or feet. Highlights must sit exactly on the named muscle; check them on a still.
- No 16:9 images, no compressed images, no ring sound. The voice is the loudest stem, then SFX, then music.
- Commit and push only to the session branch. No PR.

## Pipeline
1. **Voice.** Write the script in `work/<name>.txt`, then run `gemini_voice.py` + `voice_prep.py`.
   - `NATURAL=1`, deep calm settings: `H_PITCH=deep H_SPEED=1.0`.
   - If needed, slow with atempo ≈0.88 and divide the word times by the same factor.
   - The Reel Engine server must run on port 3011 for /sync (word timings). Restart:
     `cd ~/reel-engine-tool && PORT=3011 setsid nohup node tools/server.mjs > /tmp/reel-server.log 2>&1 < /dev/null &`
   - Trimming audio later: cut the wav with ffmpeg atrim/concat and shift the words.json the same way (see the git history of demo02).
2. **Plan** `work/<name>_plan.py`: a list of scenes. Scene texts must concatenate to the transcript in order. Anchors are words inside the scene (`"word"`, `"word#2"`, `"word+0.3"`, `"E"`).
   - Stage: `poses=[]`, `set=` (per-scene colour), `layers` (enter/exit, `poses` swaps, `ghost`, `shiver`, `alpha`, `focus=True` blurs what is behind), `bgwords` (`cursor=True` for a typewriter).
   - Effects: `insets` (asset crop, `paint`, `mark="x"|"tick"`, `big_at`), `labels` (drop-in boxes, `leader`), `arcs`, `particles`, `dim`.
   - `marks`: `style="paint"` with `blink=2` / `pulse`, or `style="disc"`.
   - Camera `keys` + `punch(at, z0, z1, focus)`. Transitions `tr=`: cut, squash, brush, `iris:x,y`, push_*, zoom, fade.
3. **Stills first** (max 3 sheets): render `Renderer(PLAN).frame(t)` at the key words. Check:
   - marks sit on the muscle
   - labels are off faces
   - insets are inside the frame
4. **Render:** `LUFS=-20 python3 <name>_plan.py`. Output goes to `work/final/<name>.mp4`.
5. **QA, every frame:** `python3 -I work/tools/edgecheck.py work/final/<name>.mp4`.
   - Expected flags: hook zoom-out, 1–4-frame slide-ins, dim / focus-blur stretches (background colour changes).
   - Any other run = something is cut. Fix it and re-render.
   - Punch zooms: keep the feet. Focus fy ≥ feet_y − 0.5/zoom; for full-body poses use (.5, .53).
6. Commit (with the attribution lines), `git pull --rebase`, push, send the mp4, and give the owner a short Hinglish summary.

## Measured timings to respect (30 fps)
| Effect | Timing |
|---|---|
| Inset pop | from 125% + blur to 100% in ~4 frames |
| Blink | on 3 frames / off 3 frames / on |
| Dim | −27…−44% over 2 frames to 1 s |
| Squash | 4 frames in, 1 empty frame, 6 frames out |
| Brush wipe | 3–4 frames per band |
| Label drop | ~8 frames ease-out with blur |
| Typewriter | ~33 characters/s, plus a 0.45 s cursor blink |
| Slides | ~15 frames, ease-out with overshoot |
| Speech | ~132–140 wpm with real pauses |
| Loudness | −20 LUFS, music 11 dB under the voice |

## Research tools (work/tools)
- `track30.py` / `events30.py`: motion events from a video.
- `fx_detect.py` + `fx_events.py`: dim, blur, highlights, wipes, cuts.
- `overview.py` / `strips.py`: contact sheets. These two read `comp2/<id>_*.mp4` relative to the current folder, so run them from the scratchpad.
