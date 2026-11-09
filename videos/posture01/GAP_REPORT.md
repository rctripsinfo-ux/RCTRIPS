# posture01 vs green.faction: full gap report (58 gaps)

Reference: green.faction's top-10 reels (by plays), especially #3 "pelvic tilt" (14M, same topic family).
Evidence tags: **[M]** measured with the same pipeline · **[S]** seen in side-by-side frames
(`gap_compare.jpg`, 15 fps strips) · **[B]** bug in our render · **[L]** likely (inferred, not measured).

## A. Character and framing
1. [S] Mascot too small: about 45% of frame height vs 70–95% in the reference.
2. [S] Always full-body. The reference uses medium shots and close-ups cropped at the waist or thigh.
3. [S] Always front view. The reference uses the view that explains the topic (side view for posture/belly).
4. [S] Identical framing in all 12 scenes, with no shot variety.
5. [S] Entrance is a slide only. The reference character *grows* from small to full size while rising (scale + rise).
6. [S] Character is frozen after the entrance (only 0.6% breathing). The reference animates every frame (glow wisps, sparkles on the problem area).
7. [S] The problem is not shown on the body. The reference shows the big belly or a glowing problem zone, while we show the text "9 GHANTE".
8. [S] The flat drawn bench does not match the painted mascot art (style mismatch).
9. [B] The bench appears at full opacity before the hero rises (visible in frames 0–3).
10. [B] Transitions double-expose: the old pose is still fading while the new one rises (visible at 16 s and 26 s).

## B. Explanation visuals
11. [S] No anatomy overlay. The reference draws an X-ray spine/pelvis inside the body to explain the mechanism.
12. [S] No animated arrows. The reference has a rotating yellow arrow for pelvis tilt and red arrows pushing the belly out.
13. [S] No colour-coded muscle highlights (the reference uses green/red/blue muscles with labels).
14. [S] No "bad state vs good state" on the same character. The reference flips a warm/red "bad" grade to a green "good" grade.
15. [S] Floor exercises float in space. The reference puts them on a mat or bench.
16. [S] No motion-path arrows on exercises (the reference uses a curved red arrow for leg raises).
17. [S] The glute-bridge rep loop is a hard 2-image swap, so it looks choppy.
18. [S] The red circle is generic. The reference marks the problem with animated glow/energy lines on the body.
19. [S] "12 KG" is a small caption. The reference gives key stats a full-screen card (huge "47%", nothing else).
20. [S] No English anatomy labels (the reference uses FLEXORS / EXTENSORS style tags).

## C. Text and typography
21. [S] Two text lines in almost every scene. The reference shows no text most of the time.
22. [S] Text is static after its pop-in. The reference types or letter-drops words in and keeps them moving.
23. [S] The exercise label stack (number + name + sub-line) is heavy. The reference shows one short label or none.
24. [S] The yellow accent colour is not in the reference palette (white + muscle colours + red).
25. [S] The font (Inter ExtraBold, square) differs from the reference's rounded bold display font.

## D. Motion and editing
26. [M] Frames with motion: 38% vs 46%.
27. [M] Motion amplitude (p95 speed): 0.028 vs 0.068, so our moves are 2.4× smaller.
28. [M] Detected scene changes: 2.5/min vs 7.4/min, because our changes are soft fades on the same background.
29. [M] First visual change at 4.8 s vs 2.5 s, so the hook holds too long.
30. [M] Brightness variation over time: 1.8 vs 10.6 (visually monotone).
31. [M] Colour variation over time: 5.2 vs 11.6.
32. [S] Only one colour-grade beat (the red flash). The reference uses several (warm "bad" grade, sparkles, highlights).
33. [S] The same push-in on every scene feels mechanical. The reference's moves are motivated by the voice.
34. [S] All props bob in the same loop, which also feels mechanical.
35. [S] Each exercise is a static pose for about 4 s. The reference shows the movement itself (arrows, rep motion).
36. [M] Ease-in is 2 frames vs 3. The entrance is slightly too snappy.

## E. Audio
37. [M] The music/ambience bed between words is 15 dB quieter (-36 dB vs -21 dB), so there are empty gaps.
38. [M] Thin low end: 14% of energy below 150 Hz vs 29%.
39. [M] Too bright and harsh: 3.5% of energy above 4 kHz vs 0.6%; spectral centroid 1673 Hz vs 1277 Hz.
40. [M] Speech pace: 2.6 vs 3.6 words/sec (27% slower).
41. [S] Fixed 0.12 s gaps plus TTS pauses make the delivery stop-start. The reference flows continuously.
42. [L] 12 separate TTS takes reset the intonation every line. The reference is one continuous take.
43. [B] The music file is a 20 s clip looped, so it has audible seams at 20 s and 40 s.
44. [M] Loudness range is 2.9 LU vs 2.2. Ours is slightly less compressed, so the voice punches less.
45. [M] -13 LUFS vs -14 LUFS (minor; Instagram normalises anyway).

## F. Script
46. [S] The hook is an assumption ("9 ghante jhuke hue?"). The reference hooks with a myth-bust ("tumhara pet fat nahi hai").
47. [S] No self-test. The reference makes the viewer do something ("deewar se chipak ke khade ho jao…").
48. [S] No identity line. The reference uses "tum bhi un 60% logon mein ho".
49. [S] Our stat stands alone. The reference ties its stat to the self-test result.
50. [S] Exercise 1 (side neck stretch) does not fix forward-head posture (chin tucks would). Content accuracy.
51. [S] The form cues are thinner. The reference gives cue + duration for every exercise ("20–30 sec hold").
52. [S] The CTA "save + follow" gives no reason. The reference adds a reason ("bina plan ke train karna band karo") and an offer.
53. [S] No "next workout ke liye save karo" style save trigger.
54. [M] About 150 words in 47 s vs about 170 in the reference, so the script carries less information.

## G. Branding and publishing
55. [S] No logo watermark (the reference has one top-right in every reel).
56. [S] No product end card (the reference shows the mascot holding a phone with the app plus a typewriter CTA).
57. [S] No Instagram caption drafted. The reference uses a short curiosity line + emoji + one hashtag.
58. [S] No cover frame or twin variant prepared. The reference posts A/B twins (e.g. 7.8M vs 4.9K plays).

## Priority fixes for v2
1. Framing: hero at 75–90% height, close-ups and medium shots, side view for posture (gaps 1–5, 7).
2. Clean transitions and the bench bug (9, 10).
3. Rewrite the hook as a myth-bust + self-test + identity line, with chin tucks as exercise 1 (46–50).
4. Explanation layer: drawn spine line, arrows, bad/good colour grade (11–14, 16).
5. Text diet: no captions on most scenes, one full-screen stat card (19, 21–23).
6. Audio: one continuous TTS take at a faster speed, louder bass-ier bed, de-ess/low-pass the voice, no loop seams (37–43).
7. Logo, end card, caption, cover, twin variant (55–58).
