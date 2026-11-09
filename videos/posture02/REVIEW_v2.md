# posture02 (v2) — detailed review: mistakes + remaining gaps

Method: the whole video at 6 fps (286 frames) as contact strips, suspicious moments at full resolution,
the voice re-transcribed and diffed against the script, and blank-frame / motion / colour / audio metrics
vs green.faction's top reels.

## A. Mistakes in our video (things that look wrong)
| # | Time | Mistake | Fix |
|---|---|---|---|
| 1 | 0.0–0.1 s | First 3 frames are an empty green screen, so the autoplay first frame and thumbnail are blank | Start on the hook image at frame 0 |
| 2 | 1.7 s, 14.0 s | The same pose "re-enters" (shrinks and rises again) when only the framing changes, which looks like a glitch | Use a hard cut / punch-in for the same pose; the rise animation only for a new pose |
| 3 | 0.2–3 s, 14–17 s | The neck "pain" wisps read as a red doodle/cloud on the skin | Replace with a pulsing red glow on the neck (soft radial) |
| 4 | 3.5–6.8 s | Spine dots run over the scalp up to the forehead | End the spine at the skull base |
| 5 | 4.5–6.8 s | The forward-head arrow sits across the head and looks like a red headband | Put the arrow in front of the face, pointing forward |
| 6 | 9.1–9.3 s | The red flash turns the whole frame and the character solid red for 6 frames, which looks like an error | Lighter flash (≤35%), 4 frames, background only |
| 7 | 9.3–10.4 s | The sore-back close-up crops the head at the right edge | Reframe with the head inside the safe area |
| 8 | 10.5–14 s | Wall test is unclear: the wall is a flat stripe, the figure is small, the head-to-wall gap isn't visible, and the right half is empty | Bigger figure, real wall (with baseboard), dashed line from wall to head + "GAP" callout |
| 9 | 14–16.6 s | The red arrow behind the head reads as another headband | Short arrow in the gap only, plus a dashed ideal line |
| 10 | 18.8–23.5 s | The stat card holds for 4.7 s with no change | 2 beats: "EVERY 15°" then "12 KG" punch on the word "twelve" |
| 11 | 18.8–19.6 s | "12 KG" counts up 3.5 s *before* the voice says "twelve kilos" | Sync the count to the word |
| 12 | 25.5–27.6 s | "15 DAYS" text overlaps the top of the head | Move the text up or frame the hero lower |
| 13 | 24–27 s, 41–47 s | Sparkles render as white "+" scratches over the chest and face | Sparkles only outside the silhouette, softer 4-point glints |
| 14 | 27.8–31.4 s | The chin-tuck arrow points into the nose/eye, not the chin, and nothing shows the tuck | Arrow at chin level; before/after nudge of the head (small backward shift) |
| 15 | 31.4–34.7 s, 38.4–41.4 s | Cobra and glute-bridge figures are tiny (about 35% of the width) with big empty space | Frame the floor poses 90% wide, centred vertically |
| 16 | 38.4–41.4 s | The glute-bridge rep loop is a hard swap between 2 images (choppy) | 4-frame crossfade + hip lift motion |
| 17 | 38.3 s | The label slides in from off-screen, so fragments like "…BRIDGE" appear | Pop-in at centre instead of a long slide |
| 18 | 27.8–41.4 s | Exercise labels are small (92 px) while the frame is mostly empty | Bigger label (130 px) + number |
| 19 | 0–3 s | Hook: warm skin on a brown background has low contrast, so the character merges into it | Darker/cooler "bad" background, or a rim light on the character |
| 20 | 0–3 s | The hook close-up hides the phone and hands, so the cause isn't visible | Medium shot that keeps the phone in frame |
| 21 | ~32 s | Possible TTS mispronunciation: Whisper heard "cobra" as "breast" | Check by ear; if wrong, regenerate with "COH-bruh" spelling |
| 22 | 7.5 s | "shoulders" heard as "shoulder" (minor) | — |
| 23 | 47.7 s | The video ends abruptly mid-CTA, with no hold or loop point | 0.8 s hold on the end card |
| 24 | all | Mats (flat grey trapezoids) and the bench look unfinished next to the painted mascot | Shaded mat/bench with highlight + shadow |
| 25 | all | Motion is busier than the reference (68% vs 46% of frames) because wisps and sparkles run constantly | Effects only on their beat |
| 26 | all | Colour swings are too strong (24 vs 11.6) | Milder bad grade, shorter |
| 27 | all | Audio over-squashed: loudness range 0.6 LU vs 2.2 | Lighter compression / bed ducking deeper in speech |

## B. Remaining gaps vs the reference (style level)
1. The reference draws **X-ray anatomy inside the body** (bones/spine); we draw dots on the skin.
2. The reference **colour-codes muscles with labels**; we have none.
3. The reference keeps **one pose for several beats and animates overlays**; we swap poses 16 times.
4. The reference uses **thick curved motion arrows** (rotation, path); ours are straight.
5. The reference shows a **before/after state on the character**; we only change the background.
6. **Logo watermark** missing (needs your logo file).
7. **Product/app end card** missing (needs a decision on what to promote).
8. The reference mascot is flat cel-shaded and ours is painted. This is inherent to your character, so it isn't a fix item.

## C. Checked and OK
- Blank "blink" frames between scenes: ours 1.8%, reference 1.9–3.4%. The reference does this too, so it's in style (except #1, the very first frame).
- Voice: 167/167 words present, no clipped words from the pause-tightening; pace 3.54 words/sec (ref 3.6).
- Loudness -14.1 LUFS, music bed, bass and highs are close to the reference.
