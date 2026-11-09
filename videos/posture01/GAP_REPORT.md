# posture01 vs green.faction: gap report

Compared against the **top 10** green.faction reels (by plays), with the same measuring pipeline,
same Whisper model, and side-by-side frames (`gap_compare.jpg`: ref #3, ref #1, ours at the same beats).

## Measured
| Metric | Top-10 ref | Ours | Gap |
|---|---|---|---|
| Speech pace (Whisper words/sec) | **3.60** | **2.63** | ours 27% slower |
| Length | 48 s | 47 s | OK |
| Frames with motion | 46% | 38% | less motion |
| p95 motion speed | 0.068 | 0.028 | movements 2.4× smaller/slower |
| Scene changes / min (detected) | 7.4 | 2.5 | our scene changes are soft fades the detector barely sees |
| First scene change | 2.5 s | 4.8 s | hook changes too late |
| Brightness variation over time | 10.6 | 1.8 | ours visually monotone |
| Colour variation over time | 11.6 | 5.2 | ours monotone |
| Ease-in / settle frames | 3 / 7.5 | 2 / 6 | OK |
| Loudness | -14.1 LUFS, LRA 2.2 | -13 LUFS, LRA 2.9 | OK (slightly more dynamic) |

## Seen in the frames (largest gaps first)
1. **Character too small.** Ref: the mascot fills 70–95% of the frame height, often cropped at the waist or
   thigh (medium shots and close-ups). Ours: a small full-body figure at about 45% height in every scene, with empty space around it.
2. **No shot variety.** Ref mixes close-up, medium, side view, full-screen stat card ("47%"),
   diagram and exercise-on-mat. Ours uses the same framing in all 12 scenes.
3. **No diagrams or motion arrows.** Ref overlays anatomy (spine, pelvis, highlighted muscles) and curved
   red arrows that show the movement direction. Ours has only red circles.
4. **Too much text.** Ref uses little text: mostly none, or one huge word/number filling the
   screen. Ours puts two caption lines at the top of every scene, which reads like subtitles.
5. **Messy transitions.** Our fade-out of the old pose overlaps the new pose sliding up, so it shows as a
   double exposure at 16 s and 26 s. Ref swaps cleanly, with the old pose gone before the new one rises.
6. **Exercises lack context.** Ref shows equipment (mat, bench, dumbbell) and the movement path.
   Ours shows plain poses floating on the background.
7. **No brand mark.** Ref has a small logo watermark in the top-right in every reel.
8. **Pace.** Our voice has more pauses (3.6 vs 2.6 words/sec): tighten the gaps and/or raise TTS speed.

## Fix list for v2 (in order of impact)
1. Scale the hero to 75–90% of frame height and crop to medium/close-up shots. Vary the framing per scene
   (close-up on the problem, full-body for exercises).
2. Hard-swap transitions (old pose out in 2–3 frames, then the new one slides up). No overlapping ghosts.
3. Cut the text to 1 huge word/number per beat (e.g. a full-screen "12 KG" stat card), and none on many scenes.
4. Add motion arrows on the exercises, and a simple drawn spine/neck line on the posture scenes.
5. Speed the voice up about 25% (to about 3.5 words/sec): smaller gaps, and atempo, or TTS speed 1.4.
6. Add a mat under the floor exercises and a small brand watermark.
7. First visual change by about 2 s. Add a punch-in on the hook.
