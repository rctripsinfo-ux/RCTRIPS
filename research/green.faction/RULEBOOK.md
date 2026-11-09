# green.faction (Gym Faction) — Reel Style Rule Book

Source: all **54 reels** on @green.faction (7 Jul – 8 Nov 2026), analysed with the
`reference-video-analysis` skill: every frame at 30 fps, contact sheets, motion and colour
metrics, loudness, and transcripts (Hindi, medium Whisper + Apify).
Raw numbers: `REFERENCE_SET.json` and `reels_metadata.csv` in this folder.

## 1. Performance snapshot
| Metric | Value |
|---|---|
| Reels | 54 in ~4 months (≈3/week, often 2 posts on the same day) |
| Plays | median **882K**, mean 2.6M, max **28.4M** |
| Likes / plays | median 4.5% |
| Comments | median 99 |
| Length | median **52 s** (21–108 s) |
| Audio | 100% original voice-over, no trending music |
| Purpose | Every reel sells the Gym Faction home-workout app |

**Twin-post A/B testing:** in 11 pairs the same video (same day, same length) was posted twice
with a different caption or cover. One version gets millions of plays, the other only thousands
(e.g. 7.8M vs 4.9K, 5.0M vs 3.0K). This is most likely Instagram "trial reels" or a test of
caption, cover or hook. **Copy this tactic:** post 2 variants and keep pushing the winner.

Top 5: forearms "T-shirt test" (28.4M) · 30-day abs (17.4M) · "big belly is pelvic tilt" (14.0M) ·
500K thank-you + beginner routine (7.8M) · triceps circuit (7.6M).

## 2. Visual style (what it looks like)
- **One mascot, always.** A faceless, olive/yellow-green (#B5B35A-ish), hyper-muscular 2D comic
  character with white glowing eyes, black joggers and wristbands. No human presenter, no real
  footage. A drawn character can be reused endlessly without filming.
- **Flat solid background:** dark teal-green **#2C5C4C** (rgb 44,92,76) covers **53% of all pixels**.
  No gradients or scenery. The brand colour *is* the background.
- **Anatomy overlays:** each target muscle is colour-coded (green / red / blue) on a separate
  arm or torso illustration with a small coloured label (EXTENSORS, FLEXORS, BRACHIORADIALIS).
  Labels appear one by one, synced to the voice.
- **Annotations:** a red circle is hand-drawn around the muscle, a "3D" sticker pops in rotated,
  and before/after splits are shown side by side ("shirt" vs "t shirt").
- **Danger beat:** the whole frame tints **red/black for ~8 frames** on the pain point
  ("mistake", "fat"), then returns to green.
- **Text:** bold white sans-serif, short (1–3 words), typewriter or letter-drop reveal.
  Small brand watermark at top-right (logo) or bottom ("Gym Faction").
- **End card:** the mascot holds a phone showing the app UI, and "Gym Faction / Download karo"
  is typed in letter by letter.

Measured look (median of 54): luma 89/255 (dark-ish), contrast σ 34, saturation 116/255,
warmth R−B = −15 (cool/green), crushed blacks almost absent (p1 luma 19), 0.7% clipped whites.
Very sharp, clean vector art (sharpness ≈ 670, edge density 4.9%).

## 3. Motion and editing (how it moves)
This is **2D motion graphics, not camera work.** The motion numbers describe how the graphics
animate:
- **Slide-up entrance:** elements rise from the bottom edge. 73% of all motion is vertical,
  only 8% horizontal and 18% scale. A move eases in over **3 frames** and eases out over **~7 frames**,
  so it starts fast and settles slowly.
- **Something is always moving:** about 51% of frames have motion. Nothing is static for long.
- **Scene change** about every **3.2 s** (median; p25 1.3 s, p75 8.1 s), ≈ **9 scene changes/min**.
- **First scene change at ~2 s.** The hook image changes almost immediately.
- **~25 "pop" events per minute:** labels, stickers, circles and flashes appearing on single
  frames. Fade-to-background transitions take ~5 frames.
- Top-10 reels move slightly *less* than bottom-10 (46% vs 52% of frames moving, 22 vs 27
  pops/min). The winners are cleaner and less busy.

## 4. Script formula (what it says)
Hindi/Hinglish voice-over, second person ("tum"), **3.5 words/sec** (p25 3.2, p75 3.6), no music.
1. **Hook (0–3 s), relatable "if / when" situation**, used in 15/37 (6 of the top 10):
   "Jab bhi tum shirt ya t-shirt pehnoge… sirf tumhare forearms visible honge."
   "Agar roz crunches ke baad bhi six-pack missing hai…"
   or a **myth-bust**: "Tumhara pet utna bada nahi hai… asli wajah anterior pelvic tilt hai."
2. **Stakes:** "Agar wo patle hain, toh poori physique bekaar lagegi."
3. **Promise with low effort:** "Sirf do dumbbell se…", "bina gym, bina equipment"
   (8/37). "3D" muscles (9/37). A stat/percentage ("90% log…", "60 pratishat") appears in 12/37.
4. **Challenge line:** "Ab faisla tumhara: scroll karoge ya 3D shoulder banaoge?"
5. **Anatomy lesson:** the target muscles, each named and colour-highlighted on screen.
6. **Numbered exercises (2–5):** name → which muscle → one form cue (14/37 use explicit numbering).
7. **CTA, almost always:** "Next workout ke liye save kar lo" + "Gym Faction download karo,
   link bio mein hai." The app CTA appears in **36/37** transcripts.

Captions are short and curiosity-driven ("30 Days Abs Challenge 💀", "Giga Biceps 💪"),
with few hashtags (mostly #gymfaction).

## 5. Sound
- Integrated loudness **−14.2 LUFS** (exactly Instagram/YouTube target), true peak −0.5 dBFS.
- Loudness range only **2.3 LU**. The mix is heavily compressed, so the voice is constantly up front.
- Voice-over is the only audio identity (100% "original audio").

## 6. Recreate it in our style (checklist)
1. Design **one ownable mascot** and **one flat brand colour** background. Reuse them in every reel.
2. Script with the formula in section 4 at ~3.5 words/sec, 45–60 s, Hindi/Hinglish, "tum".
3. Animate in 2D (After Effects / Rive / Remotion / Canva): slide-up entrances (3-frame ease-in,
   ~7-frame settle), scene change every ~3 s, labels/circles synced to words, red flash on the pain
   point, typewriter end-card CTA.
4. Mix the voice to −14 LUFS, true peak ≤ −1 dBFS, light compression (LRA ≈ 2–3 LU).
5. Post every reel twice (trial/variant). Change the hook line, cover or caption and keep the winner.
6. Measure each render with the skill:
   `python3 .claude/skills/reference-video-analysis/scripts/analyze_video.py our.mp4 --out work/analysis/our`
   then `compare.py research/green.faction/REFERENCE_SET.json work/analysis/our/summary.json`.

## Notes and limits
- Transcripts are machine-generated (Hindi ASR), so spellings are approximate. Pattern counts are
  keyword matches over 37 of 54 transcripts (all of the top 10 except #7).
- "Hard cut" counts from the analyzer over-trigger on motion graphics, because single-frame
  pop-ins count as cuts. Section 3 uses merged scenes (pops < 0.25 s folded into the scene).
