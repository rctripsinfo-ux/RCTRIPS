# posture03 (v3) — review vs green.faction: mistakes + what the reference does that we don't

Evidence: reference frames at 15–30 fps around their tilt/zoom/transition moments (found from roll/zoom spikes in
frames.csv of the top 6 reels), full-res reference frames of arrows / X-ray / muscle highlights, and full-res v3 frames.
Images: `review_ref_motion.jpg`, `review_ref_detail.jpg`, `review_v3_arrows.jpg`.

## 1. Character motion (owner's point: entrances, flips, tilts, new characters)
What the reference does:
- **Card-flip pose changes:** the character turns edge-on to a thin vertical sliver (~5 frames), then the next pose turns back out (~5 frames). That is a 3D Y-axis flip of about 0.33 s. They use it for most pose changes (#5 3.8 s, #6 9.3 s, #4 2.8 s).
- **Tilt/lean:** the character rotates a few degrees and settles on emphasis words. This shows up as roll spikes every 1–3 s in the first 10 s of every top reel.
- **Grow + rise entrance** with a slight overshoot, full opacity, never a translucent ghost.
- **Second character / split panels:** light-green panels rise from the bottom like bars, carrying a second character or a comparison (bad vs good side by side, #2 abs 1.5–3.5 s).
- **Pop-out props:** round icon badges pop out of the hand in an arc (#5 triceps 4–6 s).

What we do (mistakes):
1. Pose changes are a rise from the bottom or a hard cut. **No flip, no tilt, no settle.**
2. The rise starts as a translucent shrunken ghost (40% opacity).
3. Never two characters or panels on screen; bad and good are 35 s apart instead of side by side.
4. The character is frozen between changes apart from the push-in, with no reaction to emphasis words.
5. The chin-tuck red "ghost head" reads as a blurry double image, not an animation.
6. Glute-bridge reps still crossfade (a muddy double image for 2–3 frames per rep).

## 2. Muscle highlights (owner's point)
The reference fills **the whole muscle** with a flat colour (green / red / blue), following its exact shape, often with a label
(EXTENSORS / FLEXORS / BRACHIORADIALIS), and circles the area (red ring around the abs).
We have:
7. **No muscle highlight at all.** The red "glow" is a round blur that ignores the muscle shape.
8. No muscle labels.
9. The spine is a row of dots on the *skin edge*. The reference overlays an X-ray spine and pelvis *inside* the body with a soft glow.

## 3. Arrows (owner's point)
The reference uses broad flat block arrows (red, or yellow with a gradient), with wide triangular heads and no black outline.
They sit **in empty space next to the body** (e.g. 2 parallel red arrows beside the belly, a curved yellow arrow behind the pelvis),
slide in, and **never touch the face**.
We have:
10. **Arrow on the face:** at 6.5 s the red forward-head arrow pokes out of the forehead and eye.
11. **Arrow over the face/neck:** the cobra arrow (34.5 s) runs over the neck and face.
12. Arrows **on the body**: hip flexor (thigh), glute bridge (hips), chin tuck (at the jaw).
13. Thin neon-green lines with a black outline, so they look like a drawing tool, not part of the art.
14. Too small (about 18 px stroke at 1080 wide; the reference arrows are about 60–90 px tall).
15. Arrows draw on like a pen stroke; the reference arrows slide/pop in as finished shapes.

## 4. Other mistakes found
16. The wall in the wall test is a flat light-green stripe with lines, so it reads as a door or panel. The "GAP" marker is tiny.
17. The wall-test full-body shot is narrow, with about 60% empty frame on the right for 3.5 s.
18. The pain glow (red blur) looks like a rash. The reference uses crisp glow lines or a highlighted muscle.
19. The stat card has a thin red ring. The reference uses just huge white text ("47%") with a punchy scale-in.
20. No logo watermark (the reference has one in every reel).
21. No word-by-word captions on the hook. Reference #2/#4 type the hook line word by word, top-left, with red keywords.
22. Exercise beats are a single static image for 3–4 s. The reference shows the movement (two key poses with a flip or a smooth slide).
23. The sparkles are generic. The reference uses meaningful pop-outs (icons, badges, inset diagrams).
24. Loudness range is still 0.7 LU vs 2.2 in the reference (audio too dense).

## 5. Plan for v4
- **Motion:** a 3D card-flip between poses (scale-x 1→0→1 with a slight skew/brightness change, about 10 frames), a ±4° tilt + settle on emphasis words,
  grow + rise with overshoot at full opacity, and side-by-side split panels for bad vs good posture.
- **Muscle highlights:** hand-traced muscle shapes on each pose (neck/traps, chest, hip flexor, glutes), filled with a flat
  colour (multiply blend so the shading shows through), clipped to the body, plus a short label. The repo's anatomy circles
  (`anat_muscle_neck`, `anat_pain_neck`, `anat_muscle_hip_flexors`, `anat_muscle_glutes`, `anat_bone_spine_bad/good`) pop out
  as inset badges next to the character, like the reference's arm diagrams.
- **Arrows:** flat block arrows (red / yellow, wide heads, soft shadow, no outline), placed only in empty space beside
  the body (never on the face), sliding in.
- **Exercises:** each one as 2 key poses with a flip or a smooth slide between them.
- **Branding:** add the logo watermark once you send the file.
