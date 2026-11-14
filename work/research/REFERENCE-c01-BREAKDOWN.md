# REFERENCE BREAKDOWN — "Why Your Arms Still Look Small" (Captain Workout Short, 4.2M views)

File: owner's Drive copy (`Why Your Arms Still Look Small.mp4`). All numbers measured on that file on 14 Nov 2026 unless
marked ESTIMATE. Transcript timing = owner's word-level SRT (TurboScribe). Frames: every frame at 30 fps (1,874 frames)
tracked against the flat set colour, plus 1 fps keyframes and 0.1 s / 30 fps strips around changes.

## 1. Status
| Sec | Before this request | Now |
|---|---|---|
| A Basics | PARTLY (duration, size, fps, words) | DONE |
| B Structure / script | PARTLY (SRT words, hook lines) | DONE |
| C Camera | PARTLY (30 fps events classified) | DONE (2D: "camera" = layer scale / position) |
| D Cuts & transitions | PARTLY (6 cuts counted) | DONE |
| E Look / render | NOT DONE | DONE (tool = ESTIMATE) |
| F Light & colour | NOT DONE | DONE (no lighting changes exist) |
| G Characters | NOT DONE | DONE (proportions ESTIMATE) |
| H Captions & text | NOT DONE | DONE |
| I Audio | PARTLY (LUFS, music bed, pauses) | DONE except SFX list + music genre: NOT POSSIBLE here (speech-overlapped SFX need an audio classifier; Gemini audio API returned 503) |
| J Pacing map | NOT DONE | DONE |
| K Retention tricks | PARTLY | DONE |
| L Weaknesses | NOT DONE | DONE |

## A. Basics
- Duration 62.53 s · 720 x 1280 · 9:16 · 30 fps (constant) · MP4 (H.264 video, AAC 44.1 kHz stereo, plus a mov_text subtitle track) · 633 kb/s.
- 137 spoken words · first word at 0.00 s, last word ends 62.1 s · 2.19 words/s (132 wpm) · 15 pauses >= 0.35 s.

## B. Structure / script (timestamps = SRT)
| Part | Time | Text |
|---|---|---|
| Hook (roast + question) | 0.00-4.75 | "You're curling every session, but your arms still look like coat hangers?" |
| Comedy pause | 4.75-6.49 | 1.74 s silence, character sips a shaker in close-up |
| Bumper | ~6.5-7.9 | "Let me fix that." (grey title card, empty set) |
| Mechanism (myth flip) | 8.1-12.6 | "Here's the truth. Biceps don't make your arms look huge. Triceps do." |
| Escalation | 13.2-17.8 | "And if you want that sleeve-busting size, you need to hit all heads of the triceps." |
| Promise | 18.2-20.7 | "Here are three moves that get it done." |
| Fix 1 | 21.2-31.9 | "First, overhead extensions. Dumbbells, ropes, cables, it doesn't matter. But keep your arms behind your head, and elbows up for a full stretch." |
| Fix 2 (+ twist: alternative) | 32.4-47.9 | "Second, dips machine. Perfect for loading heavy without turning into a flailing mess. Elbows tucked, chest up, keep it in tricep zone. No machine? Bench dips with plates. Old school and super effective." |
| Fix 3 | 48.2-57.2 | "Third, dumbbell triceps extensions. This one nails full range stimulation. Shoulders locked, elbows steady, move like you mean it." |
| Ending (recap, no question) | 57.3-62.1 | "These three triceps exercises will give you maximum gains." |
- First frame: the character is already mid-curl (action already happening), seen in a ~2x blurred close-up that zooms out in 12 frames. First line = statement that turns into a question ("...coat hangers?").
- Ending: a recap collage of all three exercises + a thinking close-up; it does NOT hand a question back (no CTA).

## C. Camera (2D: moves are layer / set scale and position; 37 non-trivial motion events)
| Start-end (s) | Type (measured) | Frames | Curve | On word |
|---|---|---|---|---|
| 0.03-0.43 | pull-out zoom (size 0.58x) + blur | 12 | - | You're |
| 2.10-2.53 | layer slides down out | 13 | - | but |
| 2.70-3.10 | new pose slides up in | 12 | - | arms |
| 3.80-4.20 | push-in (1.41x) | 12 | - | like |
| 6.70 | hard cut | 1 | - | Let |
| 8.07-8.57 | layer enter (grow) | 15 | - | Here's |
| 9.13-9.56 | push-in 1.57x + move right | 13 | ease-out | truth. |
| 13.23-17.10 | long drift / pan (0.56x) | 116 | ease-in-out + overshoot | And |
| 21.10-21.23 | punch zoom (0.77x) | 4 | - | First, |
| 22.27-22.67 | push-in 1.19x | 12 | - | overhead |
| 23.93-24.70 | props enter one by one | 23 | - | (pause) |
| 25.00-25.70 | push-in 1.72x + move | 21 | ease-out | Dumbbells, |
| 26.70-27.30 | idle shiver | 18 | - | doesn't |
| 27.77 | hard swap (corner peek) | 1 | - | But |
| 28.33-28.80 | ghost layer grows | 14 | - | arms |
| 32.43-32.56 | small move | 4 | ease-out | (pause) |
| 33.20-33.60 | layer fade/grow | 12 | - | dips |
| 34.63-35.06 | cameo rises from corner | 13 | ease-out | Perfect |
| 37.77-38.20 | pull-out 0.62x | 13 | ease-in | flailing |
| 38.30-39.03 | push-in 1.46x | 22 | ease-out | mess. |
| 42.70-43.23 | push-in 1.41x | 16 | - | (pause) |
| 43.90-44.30 | pull-out 0.63x | 12 | - | Bench |
| 45.57 | punch 0.75x | 1 | - | plates. |
| 45.83-46.33 | cameo rises, 1.4x | 15 | ease-out + overshoot | Old |
| 46.50-47.97 | idle shiver x2 | 13+20 | - | school / effective |
| 48.17-48.30 | quick move | 4 | - | Third, |
| 49.17-49.53 | swap + ghost grows | 1+9 | - | dumbbell |
| 50.23 / 51.20 | punch zooms 0.77x / 0.51x | 1 / 1 | - | triceps / This |
| 52.00-52.80 | ghost grows | 24 | - | one |
| 57.23-58.13 | collage piece slides in 1.38x | 27 | ease-out + overshoot | you |
| 58.37-58.97 | slides in | 18 | ease-out + overshoot | three |
| 59.07-61.77 | slow drift 1.26x | 81 | ease-out + overshoot | triceps |
- Totals: 37 motion events = 35.5 per minute; new framing every 1.6 s on average; 63.9 % of frames completely still; 8.6 % of frames in fast motion (frame difference > 6).
- Slides: median 15 frames (0.5 s); measured curves ease-out 10 of 16 with overshoot in 5.
- Shot sizes by second (foreground box height): full / medium 28 s, close-up 21 s, wide or empty / text-only 14 s.
- Camera height: frontal eye level throughout (2D) — ESTIMATE.

## D. Cuts & transitions
- 6 hard cuts (scene detector): 13.23, 22.27, 33.20, 42.70, 43.90, 48.17 s, plus 4 one-frame pose swaps (6.70, 23.77, 27.77, 49.17 s).
- Every other change happens WITHOUT a cut: layer exits/enters on the same set (2.1-3.1 s: out down, 0.17 s empty set,
  new pose up), corner cameo rises (34.6, 45.8 s), props appear one by one (23.9-26.7 s), ghost limbs grow (28.3, 49.2, 52.0 s).
- No dissolves, no whips, no morphs measured. Section changes use a giant grey number on the empty set (21, 32, 48 s).

## E. Look / render style
- 2D flat cut-out illustration (no 3D). Tool: ESTIMATE — layered PNG cut-outs animated in a 2D editor (After Effects / CapCut class).
- Outlines: dark, ~3 px at 1080 width (ESTIMATE, n = 8 edge samples, IQR 3-3.25 px).
- Shading: smooth airbrushed grey muscle shading on a near-black / grey character; anatomy diagrams use a different, painted style.
- Set: one flat colour #BAC8D0 (RGB 186,200,208) for the whole video; no texture, no props in the set.
- Depth / fog / DOF / sun rays / bloom: none. Vignette: none (corner luminance 196.6 vs top-centre 196.4).
- Grain: none (flat-patch noise std 0.46). Motion blur: yes, only on fast moves (strong on the 0.0 s zoom-out, frames 0-6).

## F. Light & colour (per scene between cuts; 5 frames each)
| Scene (s) | Brightness 0-255 | Contrast (luma std) | Saturation | Dominant colours (share) | Shadow |
|---|---|---|---|---|---|
| 0.0-13.2 | 165.3 | 56.2 | 9.7 % | #B4CCCC 73 %, #3C3C3C 6 %, #6C6C6C 5 %, #545454 4 %, #242424 3 %, #0C0C0C 2 % | #272727 |
| 13.2-22.3 | 178.1 | 41.4 | 11.8 % | #B4CCCC 74 %, #849C9C 4 %, #6C6C6C 3 %, #9C9C9C 3 %, #3C3C3C 3 %, #E4E4CC 1 % | #2C2020 |
| 22.3-33.2 | 184.1 | 36.2 | 10.3 % | #B4CCCC 88 %, #545454 3 %, #849C9C 2 %, #3C3C3C 2 % | #272829 |
| 33.2-42.7 | 164.3 | 58.3 | 9.3 % | #B4CCCC 74 %, #242424 7 %, #3C3C3C 7 %, #545454 4 % | #28292A |
| 42.7-43.9 | 151.2 | 63.2 | 9.0 % | #B4CCCC 63 %, #545454 16 %, #3C3C3C 7 % | #262628 |
| 43.9-48.2 | 168.3 | 52.0 | 9.7 % | #B4CCCC 73 %, #6C6C6C 6 %, #3C3C3C 5 % | #26262A |
| 48.2-62.5 | 175.9 | 46.6 | 10.1 % | #B4CCCC 80 %, #3C3C3C 4 %, #545454 3 % | #27282A |
(Colours quantised to 24-level bins; exact set colour #BAC8D0.) Accent colours appear only as small marks: red biceps highlight, green triceps highlight, red shaker cup, anatomy reds.
- No lighting design: no key/rim changes, no time of day. Brightness stays 151-184 and saturation 9-12 % for the whole video; mood comes from voice and pose, not light.

## G. Characters
- 1 recurring character (several copies on screen at once: main + commentator cameo), plus anatomy diagrams.
- Design: dark grey / near-black full-body suit, light grey muscle shading, round head with a white "W" mask and two round white eyes, no mouth (no lip-sync), muscular proportions ~7.5 heads tall (ESTIMATE).
- Size in frame (foreground box height): full / medium 46-68 %, close-ups 75-84 %, wide 30-45 %; head top sits 9-25 % from the top in full/medium shots, 11-16 % in close-ups.
- Acting = pose swaps + props: curling with ghost arms and shake lines, sipping a shaker (thin "coat hanger" body), double-biceps flex, arms crossed, thumbs up, thinking chin-hold, peeking from the bottom-left corner.

## H. Captions & on-screen text
- Bottom captions: white, bold rounded sans-serif (Poppins / Montserrat ExtraBold class, ESTIMATE), lowercase, thin dark stroke, no shadow box, no keyword colour.
- 2-3 words visible, built up word by word: 101 caption changes for 137 words (1.36 words per change); a change lands within 0.18 s of the word start for 80 % of words (median -0.017 s). No caption in 15 % of frames.
- Position: text line at 76.6-79.2 % from the top; letter height ~2.6 % of screen height; line width 27-55 % of screen, centred.
- In-world text: "LET ME FIX THAT" (6.5-7.9 s, big grey condensed caps on the empty set), "1/3" and "2/3" labels on the arm (10-12 s), anatomy labels "long head / lateral head / medial head" popping one at a time (17-20 s), giant grey "1" (21 s), "2" (32 s), "3" (48 s) behind the exercise.

## I. Audio
- Voice: adult male, median pitch 112 Hz (95-140 Hz), 132 wpm, word-loudness spread 3.6 dB (calm, even; loudest words: You're, curling, arms, your, dumbbell). Longest-held words: maximum 0.78 s, exercises 0.74 s, extensions. 0.72 s.
- Pauses >= 0.35 s (15): 4.75 s (1.74 s, after the joke), 17.79, 20.69, 21.71, 23.35 (0.88 s), 25.41, 31.87 (0.72 s), 34.05 ... (full list in the SRT).
- Music: tempo ESTIMATE 63 BPM (or 126 BPM, autocorrelation of the onset envelope); bed 11.0 dB under the voice (RMS between words vs inside words). Genre: NOT MEASURED.
- SFX: only 2 transients outside speech (24.08 s, 55.29 s); SFX under the voice could not be separated. SFX are sparse.
- Loudness: -20.2 LUFS integrated, true peak -4.0 dBTP, LRA 4.5 LU.

## J. Pacing map (1 row per second; visual from 1 fps keyframes, camera from the 30 fps events)
| Time | Spoken | Visual | Camera | Caption | SFX | Light |
|---|---|---|---|---|---|---|
| 0 | You're curling every | character mid-curl, ghost dumbbells, shake lines | 2x->1x pull-out 12 f + blur | you're curling every | music in | flat #BAC8D0 |
| 1 | session, | same, curling | still / shake | session, | - | same |
| 2 | but your arms still | character drops out down; empty set 0.17 s | layer out 13 f | but your arms | - | same |
| 3 | look like coat | thin pose sipping shaker rises in | layer in 12 f | still look like | - | same |
| 4 | hangers? | same pose | push-in 1.41x 12 f | coat hangers | - | same |
| 5 | (pause) | close-up, sipping | still | - | - | same |
| 6 | Let | same; cut | hard cut | let | - | same |
| 7 | me fix that. | "LET ME FIX THAT" on empty set | still | me fix that | - | same |
| 8 | Here's the truth. | double-biceps flex enters | grow in 15 f | here's the truth | - | same |
| 9 | Biceps don't | chest close-up flex | push-in 1.57x 13 f | biceps don't | - | same |
| 10 | make your arms look | biceps red + "1/3" | still | make your arms | - | same |
| 11 | huge. | hold | still | huge | - | same |
| 12 | Triceps do. | triceps green + "2/3" | still | triceps do | - | same |
| 13 | And if you want | cut: sipping pose, ghost copy, drift | hard cut + drift starts | and if you want | - | same |
| 14 | that sleeve-busting | sipping close-up | drift | sleeve-busting | - | same |
| 15 | size, you need to | same | drift | size you need to | - | same |
| 16 | hit all heads of | close-up, lower body | drift ends | hit all heads | - | same |
| 17 | the triceps. | anatomy diagram (arm) | still | the triceps | - | same |
| 18 | Here are three | labels pop: long head | still | here are three | - | same |
| 19 | moves that get | + medial head | still | moves that get | - | same |
| 20 | it done. | + lateral head | still | it done | - | same |
| 21 | First, | giant grey "1", empty set | punch 4 f | first | - | same |
| 22 | overhead extensions. | cut: cable overhead extension in front of "1" | push-in 1.19x | first overhead extensions | - | same |
| 23 | (pause) | same | still / swap | - | - | same |
| 24 | Dumbbells, | props: dumbbells appear | props enter | dumbbells | transient 24.08 | same |
| 25 | ropes, cables, | + rope, + cable | push-in 1.72x 21 f | ropes cables | - | same |
| 26 | it doesn't matter. | three props | shake 18 f | it doesn't matter | - | same |
| 27 | But keep your | head peeks from bottom-left | swap 1 f | but keep your | - | same |
| 28 | arms behind your head, | extension + ghost arms grow | grow 14 f | arms behind your head | - | same |
| 29 | and elbows | hold, dashed arc | still | and elbows | - | same |
| 30 | up for a full | hold | still | up for a full | - | same |
| 31 | stretch. | hold | still | stretch | - | same |
| 32 | Second, | giant grey "2" | small move 4 f | second | - | same |
| 33 | dips machine. | cut: dip machine, "2" behind | grow 12 f | dips machine | - | same |
| 34 | Perfect for | commentator rises bottom-right | cameo 13 f | perfect for | - | same |
| 35 | loading heavy without | arms-crossed cameo over machine | still | loading heavy | - | same |
| 36 | turning into | hold | still | without turning into | - | same |
| 37 | a flailing mess. | hold | pull-out 0.62x | a flailing mess | - | same |
| 38 | (pause) | machine from behind | push-in 1.46x 22 f | - | - | same |
| 39 | Elbows tucked, | dip with ghost | still | elbows tucked | - | same |
| 40 | chest up, keep | hold | still | chest up keep | - | same |
| 41 | it in tricep | hold | still | it in tricep | - | same |
| 42 | zone. No | cut: thinking close-up | hard cut | zone no | - | same |
| 43 | machine? | thinking, finger on chin | push-in 1.41x | machine | - | same |
| 44 | Bench dips with plates. | cut: bench dips with plates | pull-out 0.63x | bench dips with plates | - | same |
| 45 | Old school | thumbs-up cameo rises bottom-left | cameo 15 f + overshoot | old school | - | same |
| 46 | and super | hold, shake | shake 13 f | and super | - | same |
| 47 | effective. | hold, shake | shake 20 f | effective | - | same |
| 48 | Third, | cut: giant grey "3" | quick move 4 f | third | - | same |
| 49 | dumbbell triceps | lying extension in front of "3" | swap + ghost 9 f | dumbbell triceps | - | same |
| 50 | extensions. | hold | punch 0.77x | extensions | - | same |
| 51 | This one nails | lying extension | punch 0.51x | this one nails | - | same |
| 52 | full range | ghost arms grow | grow 24 f | full range | - | same |
| 53 | stimulation. | hold, dashed arc | still | stimulation | - | same |
| 54 | Shoulders locked, | hold | still | shoulders locked | - | same |
| 55 | elbows steady, | hold | still | elbows steady | transient 55.29 | same |
| 56 | move like you | hold | still | move like you | - | same |
| 57 | mean it. These | recap: piece 1 slides in | slide 27 f + overshoot | mean it these | - | same |
| 58 | three triceps | piece 2 slides in | slide 18 f + overshoot | three triceps | - | same |
| 59 | exercises will | thinking close-up enters, collage | drift 81 f | exercises will | - | same |
| 60 | give you maximum | collage + thinking | drift | give you maximum | - | same |
| 61 | gains. | hold | drift | gains | - | same |
| 62 | (end) | hold | still | - | music out | same |

## K. Retention tricks (timestamps)
- 0.0 s: action already happening + blurred 2x zoom-out (motion on frame 1).
- 0.0-4.75 s: a roast with a funny image ("coat hangers") phrased as a question.
- 2.1-3.1 s: pattern interrupt: character drops out, empty set, a thin version rises in.
- 4.75-6.5 s: 1.74 s comedy pause on a sipping close-up.
- 6.5 s: brand bumper "Let me fix that." on an empty set.
- 9-12.6 s: myth flip with on-screen numbers "1/3" vs "2/3".
- 18.2 s: promise of a count ("three moves") -> open loop paid at 21, 32, 48 s by giant numbers.
- 23.9-26.7 s: props appear one per word (dumbbells, ropes, cables).
- 27.8 s: corner peek gag; 34.6 s and 45.8 s: commentator cameo rising from a corner.
- 42.7 s: question to self "No machine?" -> instant answer.
- 57-62 s: recap collage of all three moves.

## L. Weaknesses (measured or directly visible; what NOT to copy)
- Captions are small (letter height ~2.6 % of screen) and white on a light set (#BAC8D0, luma ~196) — low contrast.
- Saturation 9-12 % for the whole video: almost monochrome.
- Anatomy diagrams are drawn in a different (painted) style than the character.
- Frame 0 is a heavy blur (the hook's first frame is soft).
- No lip-sync / no mouth: acting relies only on poses.
- 15 % of frames have no caption at all; no keyword highlighting.
- Ending has no question / CTA back to the viewer.

## 2. STYLE RULEBOOK (measured; copy the numbers)
1. Format 9:16, 30 fps, 55-65 s, first word at 0.00 s.
2. Narration 130-135 wpm (2.2 words/s); never cut every pause.
3. Keep 12-15 pauses >= 0.35 s per minute of video; one 1.5-1.8 s pause right after the hook joke.
4. Voice male, low-mid pitch (~110 Hz median), calm: word loudness spread <= 4 dB.
5. One flat set colour for the whole video (reference: #BAC8D0); no texture, no gradient, no vignette, no grain.
6. Saturation of the frame <= 12 %; colour only on highlights and props.
7. 2D cut-out character, dark body, ~3 px dark outline at 1080 width, no lighting changes.
8. 6 hard cuts per minute max; all other changes happen on the same set without a cut.
9. 35 motion events per minute; a new framing every ~1.6 s.
10. 60-65 % of frames completely still; <= 9 % in fast motion.
11. Slides 15 frames (0.5 s), ease-out, 1 in 3 with a small overshoot.
12. Push-ins 1.2-1.7x over 12-22 frames; punch zooms 0.5-0.8x in 1-4 frames.
13. Frame 1: the action is already happening, ~2x close, zooms out to full body in 12 frames with motion blur.
14. Full/medium shots ~45 % of seconds, close-ups ~33 %, wide/empty/text ~22 %.
15. Character height 46-68 % of the screen in full/medium, 75-84 % in close-up; head top 9-25 % from the top.
16. Pose swaps happen in place (1 frame); never replace the whole set to change a pose.
17. A second copy of the character appears as a commentator rising from a bottom corner in 13-15 frames.
18. Show reps with ghost / onion-skin copies that grow in over 9-24 frames, plus a dashed motion arc.
19. Shake lines + 13-20 frame shake for effort or emphasis.
20. Props enter one per spoken noun.
21. Section markers: giant grey number (1/2/3) on the empty set, then the exercise in front of it.
22. Bumper: big grey condensed caps ("LET ME FIX THAT" style, our own words) on the empty set for ~1.4 s.
23. Numbers on screen when a ratio is spoken ("1/3" vs "2/3"), labels pop one per beat.
24. Bottom captions only: white bold rounded sans, lowercase, thin dark stroke, 2-3 words, built word by word.
25. Caption text line at 77-79 % from the top, letter height ~2.6 % of the screen, width 27-55 % (we should go bigger / higher contrast, see L).
26. Caption change within 0.18 s of the spoken word.
27. Music bed 11 dB under the voice; tempo ~63 BPM (ESTIMATE); calm, continuous, no drops.
28. SFX sparse: <= 2-3 audible hits outside speech per minute.
29. Master at -20 LUFS, true peak -4 dBTP, LRA ~4.5 LU (the reference is quiet; YouTube plays it as is).
30. Structure: roast question -> pause -> bumper -> myth flip with numbers -> escalation -> "three moves" -> 1/2/3 -> recap collage.
31. Each fix = name (1 line) + why/benefit (1 line) + 2-3 form cues ("elbows up", "chest up").
32. Offer a no-equipment alternative inside one fix ("No machine? ...").
33. End on a recap collage of every move shown (5 s).

## 3. SCRIPT TEMPLATE
```
[0.0 s, HOOK — action already on screen]
"You're [doing common habit] every [time], but your [body part] still look like [funny object]?"
[1.5-1.8 s pause — reaction pose / prop gag]
[BUMPER — our own words] "Here's the fix."
[MYTH FLIP] "Here's the truth. [Thing everyone trains] doesn't make your [result]. [Overlooked thing] does."
[ESCALATION] "And if you want that [vivid result]-size, you need to [specific requirement]."
[PROMISE] "Here are [3] moves that get it done."
[FIX 1] "First, [move]. [Equipment options], it doesn't matter. But keep your [cue 1], and [cue 2] for [benefit]."
[FIX 2] "Second, [move]. Perfect for [benefit] without [funny failure image]. [Cue], [cue], keep it in [target] zone.
         No [equipment]? [Alternative]. [Short punchy praise]."
[FIX 3] "Third, [move]. This one nails [benefit]. [Cue], [cue], move like you mean it."
[ENDING] "These [3] [target] exercises will give you [result]."   (+ optional: "Which one do you skip?")
```

## 4. OPEN QUESTIONS
1. Music genre / exact track and the SFX under the voice: need either a working Gemini audio call or a stem-separation tool (e.g. Demucs) in this environment.
2. Retention graph (YouTube Studio) for this Short is not public; views (4.2M) are not retention.
3. Font name: needs the creator's font or an OCR/font-match tool; above is a class ESTIMATE.
4. Character proportions in heads: measured only as box heights; an exact head-count needs a pose model run on the competitor frames.
