# HANDOFF: Effortless Exercise Shorts (last updated 31 Oct 2026)

**Repo:** `rctripsinfo-ux/RCTRIPS` · **Branch:** `claude/intelligent-euler-6jm4o0` · everything lives in `work/`.

## 1. The job
- **Channel:** YouTube Shorts channel **Effortless Exercise**.
- **Character:** **H**, a bald, muscular, tan cartoon man with a white "H" on his forehead.
- **Goal:** every Short above 10K views. One topic a day from `TOPICS-30-DAYS.md`.
- **Language:** talk to the owner in **Hinglish**. Scripts, titles, descriptions and prompts are in **English**.
- **Limits:** keep weekly and session usage low. No extra renders or long explanations, and don't spawn agents.
- **Git:** commit and push every finished video to the branch above. Don't open a PR unless asked.

## 2. Current approved format: "Day 1 V1, no clips"
| Day | Build file | Plan / script | Final video |
|---|---|---|---|
| 1 Forearms | `build_forearms3.py` | `forearms3.json`, `forearms3.txt` | `final/forearms3.mp4` (23.1 s) |
| 2 Lower belly | `build_day2b.py` | `day2b.json`, `day2b.txt`, `day2b.pauses.json` | `final/day2b.mp4` (18.7 s, cover) |

**Latest owner rule (29 Oct): no exercise clip videos.** Every exercise is shown with H pose images swapped in a loop:
- `poses(...)` layer, clean cuts.
- `loop(a, b, anchor, n, step)` helper: down/up frames every 0.4 s (0.6 s for slow moves).
- `flipX=True` for "each side".

Older builds (`build_forearms.py`, `build_day2.py`) used clips. Do not copy their clip scenes.

**Format, in order:**
1. **Optional cover:** the owner's thumbnail shows for 0.1 s at the start (5th argument to `fast_render.py`).
2. **Hook (0–3 s):** H image, heading shown in full from frame 1, a spinning dashed red "pain" circle on the problem area, and a camera punch on the key word.
3. **Why:** one gag image (`gag_*`) or 1–2 anatomy bubbles (`anat_*`).
4. **Bumper:** "HERE'S THE FIX" on a dark card (#1E2228), with a loud typing sound and a punch-in. Captions are hidden during it.
5. **Moves:** "#1 …" heading at the top plus a small sub (e.g. "30 SEC EACH SIDE"), the H pose loop, and a red rep counter where reps are spoken.
6. **Result:** H stands, then `gag_sunglasses_thumbs` with a heading like "ARMS: COMPLETE".
7. **CTA:** `hero_point_viewer`, the heading `COMMENT "WORD"`, a pop-up comment bubble with a notification sound, and a punch-in on the face.

**Look and sound:**
- **Look:** sand-beige background (#E2D3B9) with a spotlight. Headings in Bebas-style dark ink at the top (y 0.15). Small white clean captions at the bottom (y 0.82), with keywords in yellow.
- **Voice:** 1.3x. `fast_render.py` cuts silences. `<plan>.pauses.json` = `{"_gap": 0.05}` cuts every gap.
- **Audio:** whoosh on every entrance and transition. Loudness -16 LUFS.

## 3. Owner rules (never break)
- **Layout:**
  - No overlaps: text, bars, labels and bubbles must never touch H or each other.
  - Nothing on H's face or bald head. Anatomy circles go in the lower half, beside the legs (x 0.77–0.8, y 0.61–0.66).
  - No empty gap between the heading and H.
- **Text and sound:**
  - Typing must be in sync with the voice, and text must never shake or vibrate.
  - No green ticks or glows, no small icons on the character, no meme sounds.
- **Content:**
  - Simple words a 5-year-old understands.
  - Calm, systematic flow: one idea per beat, every picture stays at least ~1.5 s.
- **Don't change unless asked:** cards and caption style (style D cards are approved).
- More detail is in `CAPTAIN-WORKOUT-STYLE.md` (style guide plus all owner rules by date).

## 4. How to make the next video (fresh container)
```bash
cd /home/user/RCTRIPS/work
./restore_tool.sh            # installs Reel Engine from the reel-video-maker skill, applies tool-patches, copies
                             # anat/gag/card images, clips and sfx, starts the server on :3011
cp build_day2b.py build_day3.py   # edit: script anchors, scenes, poses, output file name
# write day3.txt (the voiceover script), echo '{"_gap": 0.05}' > day3.pauses.json
python3 build_day3.py
python3 fast_render.py day3 day3.txt day3.json 1.3 [thumbnails/day3.jpg]
# check frames: final/day3-frames.jpg, or ffmpeg -nostdin ... tile sheet; fix overlaps; re-render
git add -A && git commit -m "Day 3 ..." && git push -u origin claude/intelligent-euler-6jm4o0
```

**Plan anchors:**
- Anchors are phrases from the script, with at most one offset: `"Hang from"`, `"fix.+0.15"`.
- Repeated words need `Word#2`.
- Start each scene at `"<first words>-0.05"`, so no empty frame shows between scenes.

**Poses:**
- Find poses with `ls ~/reel-engine-tool/public/library/hero | grep -i <move>`, then look at them in a contact sheet before using them.
- Floor poses need a smaller width and a lower y.
- Use `autoAlign=False` for bar or hang images, so the bar stays under the heading.

**Delivery:** send the mp4 to the owner, plus a title, description and tags. Past ones are in `UPLOAD-TEXT.md` and in chat.

## 5. Where things are
- **Plans and analysis:** `TOPICS-30-DAYS.md` (next is **Day 3: "Can You Hold a Dead Hang for 60 Seconds?"**), `OLD-VIRAL-ANALYSIS.md`, `GROWTH-PLAN.md`.
- **Image prompts and images:**
  - `anatomy/` holds 60 anatomy circles (`anat_*`).
  - `gags/` holds 30 gag images (`gag_*`). These are weak: skinny_legs, sweating_bucket, knees_creak, glutes_vacation.
  - `character/` holds the H base images.
- **Clips:** `clips/` holds 77 exercise clips. They are no longer used (owner rule), but are kept.
- **Renders:**
  - `fast_render.py`: TTS, silence cut, holds, typed-card sync, cover, render, loudnorm, frames sheet.
  - `make_cards.py`: exact style-D typed cards.
- **Tool and output:**
  - `tool-patches/` holds our Reel Engine changes: pain circle, bubble connector and face-avoid, viral/high captions, dash layer, no-pop cards, and the library snapshots. `restore_tool.sh` applies them.
  - `final/` holds every rendered video. `thumbnails/` holds the thumbnails.

## 6. Open items
1. **Day 3 onward:** in the no-clip format, one per day from `TOPICS-30-DAYS.md`.
2. **Missing poses:** there are no real **dead bug** poses. Day 2 uses `hero_reverse_crunch` / `_v2` as the closest match. The owner can generate 2 images (dead bug: right arm and left leg straight, then left arm and right leg straight). Check each topic's moves against the hero library before writing the script, and ask for missing poses early.
3. **Day 1:** in farmer's hold, the `hero_pick_dumbbell` frame looks a bit bigger than the others. The owner may ask for a fix.
4. **Later:** better voice and music (needs the owner), remake the weak gags, thumbnail prompts per video (skill `effortless-exercise-thumbnail-prompts`).
