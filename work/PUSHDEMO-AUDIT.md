# Audit: `final/pushdemo.mp4` vs reference V06 "How Many Push-Ups Do You Really Need?" (31 Oct 2026)

## Evidence used (nothing re-downloaded, nothing rendered)
- **Side-by-side frames:**
  - 12 pairs in the hook (0.0–3.8 s).
  - 24 pairs from 4.5 s to 50 s, every 2 s.
  - Both sheets are in `/tmp/ref/an/` (`cmp_hook.jpg`, `cmp_full.jpg`). Earlier sheets: V06 at 1 fps and 10 fps, V06 frames 0–7, and our QA sheets.
- **Reference SRT:** V06.
- **Our word timings:** `words.json` from the render.
- **Audio measures:** loudness (EBU R128), the quiet-floor ratio (music-bed indicator), and the V06 onset/cut data in `ref-analysis/measure.json`.

**Limits:**
- I cannot listen. Voice quality, pronunciation and SFX character are **not judged by ear**. Only measurable audio facts are reported.
- Between sampled frames, motion is inferred from the earlier measurements, not watched.
- Our cut count from `scdet` (4) is unreliable on a flat beige background, so our scene changes are taken from the plan instead.
- **Intentional differences that are not errors:** H instead of their character, beige instead of pale blue, our own narration wording, our TTS voice, and no third-party clips.

## 1. Timestamp-by-timestamp table
Times are in seconds. "Ref" = V06, "Ours" = pushdemo.mp4.

| Timestamp | Reference Video | Our Rendered Video | Exact Difference / Mistake | Severity | Required Fix |
|---|---|---|---|---|---|
| 0.00 | Cover: char with **hands behind head**, crying, red ring on the chest, "NO CHEST?" huge black condensed text filling the top 20 % | Cover: H crying with **arms at his sides**, red ring on the chest, "NO CHEST?" in Inter Black (not the heading font), smaller (~60 % of the width) | Pose differs (no hands-behind-head); font is not Anton; the text is smaller | MINOR | Use an Anton TTF for the cover. A hands-behind-head sad H pose would match (needs an asset). |
| 0.03–0.40 | Smash zoom-out from an extreme chest close-up **with motion blur** to waist-up crossed-arms "X" | Zoom-out 2.8 → 1.0 over 0.4 s, no motion blur. At 0.1 s already a medium shot. Our X pose = folded arms (`hero_arms_crossed`), not an X. | No motion blur; the zoom starts less tight; the "stop" gesture is weaker (folded arms ≠ X) | MINOR | Start the zoom at 3.5, add blur/smear on the first 0.2 s (`enter: smear`), use `hero_stop_palm` or an X-arms asset |
| 0.0–1.6 | No heading at all during the hook; only tiny captions | Red "NO CHEST?" heading the whole time (owner request) | Extra heading (intentional, owner's rule) | — | Keep (owner rule) |
| 0.5–1.6 | A **rectangular video inset at the top centre** showing real push-ups (moving reps), char below | A small **circle bubble at the top right** with a still push-up image (no reps) | Inset is static (no rep motion), different shape and position | MINOR | Show the push-up loop inside the inset (poses top/mid every 0.4 s); a rectangle at the top centre, above the head |
| 1.6–2.9 | **Full background swap**: orange/brown anime speed-line gym; char waist-up, large, **sunglasses + hands behind head**, small **shiver** jitter | Beige background, faint thin white speed lines, full-body double biceps, punch zoom 1.1; no shiver | The impact background is missing; no shiver; the char is smaller; different pose | **MAJOR** | Add a speed-line/impact backdrop layer (full-screen radial lines in warm colours), `shiver()`, a waist-up crop (width 1.2, y 0.75), and a sunglasses flex pose |
| 2.9–3.6 | **Black screen**, char small in the centre, **spins/turns** and **shrinks back** (sad/aura beat) | Beige, facepalm + red pain circle on the chest, "STILL FLAT" in red (2.1–4.3), then crying | **Black beat missing**; no turn/shrink; our frustration beat is longer (2.2 s vs 0.7 s) | **MAJOR** | Insert `sad_beat()` (black, zoom 1 → 0.8) for ~0.8 s on "still looks flat", with `flip` turn |
| 3.6–4.5 / ours 4.35–5.9 | **"LET ME FIX THAT" kinetic text**: mixed sizes (LET ME small dark, FIX big, THAT big red), placed **around the char's head**, char pointing a finger up, pale-blue background | Dark card #1E2228, white "HERE'S THE FIX" typed, punch-in, no char | Different technique (kinetic text with char vs flat card); our bumper starts **0.75 s later** (4.35 vs 3.6) | **MAJOR** (technique) / brand text intentional | Keep our words, but build it as kinetic text over beige with H pointing up (`hero_count_1`), mixed sizes, "FIX" in red; start right after the hook line |
| 4.5–8.9 / ours 5.9–10.7 | Hand-only close-up **3 fingers** (big, mid-screen) with "ONLY" white text typing above (4.5–7), then sunglasses arms crossed waist-up "you'll look stronger instantly" (7–8.9) | Full-body `count_3` with heading "ONLY 3 FIXES" (5.9–8.4), then the sunglasses gag "CHEST: GROWING" (8.4–10.7) | No hand close-up (scale change missing); our section is 0.4 s longer and **starts 1.4 s later** | MINOR | Hand-close-up "3 fingers" asset (or zoom 2.2 on the hand of `count_3`), white "ONLY" kinetic word |
| 8.9–10.4 | **"#1" huge faded/ghost number** + "HAND PLACEMENT" centred mid-screen on a blank background (text-only card), then the title **moves up** as the exercise appears | "#1 HAND PLACEMENT" typed at the top at once, push-up already showing | Missing the text-only section card and the title move-up transition | **MAJOR** | Section card: ghost "#1" (opacity 0.25, size 300) + title centred for ~1.2 s, then the title slides to y 0.15 and the exercise rises in |
| 10.4–21 / ours 10.7–22.8 | **Front-view** push-up, char small in the centre; **red glow on both shoulders** ("too wide / too close"), then a **green dashed line** between the hands (correct width); char animates (several poses) | **Side view** only, one still pose the whole 12 s; white dashed shoulder→wrist line + red wrist ring; subs change 3 times | The width cue cannot be shown in side view; wrong/right comparison missing; **12 s with one unchanged pose** | **CRITICAL** | Needs front-view push-up assets: correct, too wide, too close. Show wrong (red joint glow on shoulders) → right (dashed width line, white not green per owner rule). Change the pose every ~2 s. |
| 21–22.3 | "#2" ghost + "RANGE OF MOTION" text card | Title typed at the top with the exercise | Missing section card | MAJOR | Same card as #1 |
| 22.3–29 / ours 22.8–31.5 | Side push-up going **all the way down** (chest near the floor, R26), smooth motion with a **ghost trail**, red dashed vertical depth line under the chest | Loop `pushup_top_v3` ↔ `pushup_mid` every 0.6 s; **mid is not the bottom**; red dashed arrow to the floor | The bottom position is never shown, so the cue "chest almost touches the floor" is **not demonstrated** (inaccurate demo) | **CRITICAL** | Asset: side push-up bottom (chest 3 cm above the floor). Loop top → mid → bottom → mid. |
| 29–30.7 / ours 31.5–35.2 | X-arms "don't flare your elbows like a chicken", no heading | Folded arms, heading "ELBOWS IN" | Joke visual missing (no chicken/flared-elbow image); weaker "stop" pose | MINOR | Show a wrong-form frame (elbows flared, top view or front) with a red ring on the elbows, then folded arms |
| 30.7–32 | "#3" ghost + "CORE CONTROL" card | Title typed at the top | Missing section card | MAJOR | As #1 |
| 32–35 / ours 35.2–41.3 | Straight-arm push-up with **hips sagging/popping**, red dot on the hips | **Forearm plank** (`hero_plank`) with a red ring on the hips | Wrong exercise position (forearm plank ≠ push-up); no sag/pike shown, only a normal plank | **CRITICAL** (fitness accuracy) | Assets: straight-arm push-up with sagging hips and with piked hips. Red ring on the hips. |
| 35–37 / ours ~39–41 | Finger up "bad yoga, not push-ups" | `count_1` + sub "NOT YOGA" | Similar | — | — |
| 37–41 / ours 41.3–45.5 | Push-up with a **white dashed straight line + arrow** from the neck to the heels | Forearm plank with a white dashed line from the ankle to the shoulder | Wrong base pose again (forearm plank) | MAJOR | Use the straight-arm top push-up; the line runs from the ankle to the shoulder |
| 41–43 | **"LIKE SOLID PLANK" big 3D metallic kinetic text** stacked over the push-up | Small brown sub "LIKE A MOVING PLANK" | Kinetic hero text missing | MAJOR | Big stacked text (tool look `giant`/`echo`), 2 lines, over the exercise |
| 43–45 / ours 45.5–48.9 | Thumbs up waist-up with **3 mini push-up icons** popping above the head | Thumbs up full body, heading "3 FIXES = BIG DIFFERENCE" | Mini icons (a recap of the 3 fixes) missing | MINOR | 3 small images (hand placement, depth, plank line) popping in a row above the heading |
| 45–47 | Finger up "massive difference" | Finger up "NO GYM. NO GEAR." | Similar | — | — |
| 47–50.9 / ours 50.6–53.2 | Sunglasses hands behind head, waist-up, **subscribe-button animation (like → subscribe → bell)** over the chest | Sunglasses thumbs-up gag, "CLEAN REPS = REAL CHEST" | Subscribe animation missing; different ending | MAJOR (CTA) | Add a subscribe-button layer (or our comment CTA, an owner choice); waist-up crop |
| Whole video | 50.9 s | 53.2 s | Ours is **2.3 s longer**; section starts drift +1.4 s to +4.2 s | MAJOR | Remove the "CHEST: GROWING" beat (2.3 s, not in the ref) and use voice speed 1.12 |
| Whole video, captions | Tiny white captions (≈2 % height), soft shadow, on the char's waist or under the exercise; 1–2 words | Larger white bold outlined captions (≈3 % height) at y ≈ 0.72, **over H's thighs** | Ours is bigger and covers the body | MINOR (approved template) | Keep or shrink (`size` 44) and move under the figure (y 0.86) on exercise screens |
| Whole video, headings | Small black condensed headings (≈3 % height), no "#N" prefix in the title (the number is a separate ghost) | Anton 105–150 with the "#N" prefix, plus brown subs | Ours is larger and denser (heading + sub + caption = 3 text lines) | MINOR | Drop the subs where the caption says the same; move the number to a ghost card |
| Whole video, character scale | Many shots are waist-up or close-up (0.1, 1.6–2.9, 4.5 hand, 8, 30, 36, 44–50) | Always full body (except the zoom-out start) | No scale variety | MAJOR | Add waist-up crops (width 1.3, y 0.78) on attitude beats; a hand close-up on counts |

## 2. Audio (measured)
| Item | Reference | Ours | Difference | Severity | Fix |
|---|---|---|---|---|---|
| Background music | Present the whole time: quiet floor = 0.20 of median loudness, steady tonal lines in the spectrogram | **None**: floor 0.14 (voice and room only) | Music bed missing | **CRITICAL** | Need `music_bed.mp3` (asset requested), at volume 0.025 under the voice |
| Loudness | −11.8 LUFS | −16.0 LUFS | Ours is 4.2 LU quieter; YouTube normalises to about −14, so the ref will play about 2 dB louder than ours | MINOR | Master at −14 LUFS |
| Voice | Human male, energetic | TTS, 1.08x, ~174 words/min (154 words / 53 s) vs ref ~166 | Slightly faster per word but longer overall (more words: 154 vs 141) | MINOR | Trim to ~140 words |
| SFX density | 36 onsets detected | 22 planned cues | Fewer accents | MINOR | Add whoosh on every section card, a pop on the kinetic words, a shiver sound on the flex |
| Sad/aura sound at the black beat | Present (pitched sweep / tonal, Likely) | No black beat, no sound | Missing | MAJOR | `sad_beat()` + `sad_sting.mp3` (asset requested) |
| Pronunciation / pauses | Not judged by ear | Not judged by ear | Can't be verified by me | — | Owner listens |

## 3. Transcript differences (ref SRT time → ours)
Our wording was written to be original, so each line differs in words but keeps the meaning. Exact differences:

| Ref time | Reference line | Our time | Our line | Difference |
|---|---|---|---|---|
| 0.16 | "Stop doing hundreds of push-ups that look tough but build nothing." | 0.05 | "Doing hundreds of push-ups that look tough, but your chest still looks flat?" | "Stop" is missing (the command hook becomes a question); "build nothing" → "still looks flat" |
| 2.9 | "Let me fix that." | 4.35 | "Here's the fix." | Brand phrase (intentional); **+1.45 s late** |
| 4.24 | "You only need three simple form fixes and you'll look stronger instantly." | 5.88 | "You only need three small form fixes, and your chest finally starts to grow." | Different payoff; +1.6 s |
| 8.2 | "First hand placement. Most guys go too wide or too close." | 10.70 | "Number one: hand placement. Most people put their hands too wide or too close." | "First" → "Number one"; +2.5 s |
| 12.1 | "Go shoulder width apart, fingers slightly out." | 15.44 | "Keep your hands just outside your shoulders, right under your chest." | The **"fingers slightly out"** cue is missing; "right under your chest" contradicts "just outside your shoulders" slightly. **Fitness wording to fix:** "hands a bit wider than your shoulders, under your chest line". |
| 15.8 | "That's where your chest, shoulders and triceps actually work together." | 19.33 | "Now your chest, shoulders and triceps all work together." | Same meaning |
| 19.7 | "Second range of motion. Half reps equals half results." | 22.78 | "Number two: range of motion. Half reps give you half results." | +3.1 s |
| 24.9 | "Go all the way down until your chest nearly touches the floor. Then push up with power." | 26.75 | "Go down until your chest almost touches the floor, then push back up with power." | Same |
| 28.4 | "Don't flare your elbows like a chicken." | 31.46 | "And keep your elbows in. Don't flap them out like chicken wings." | Ours is longer (+5 words) |
| 30.4 | "Third, core control. If your hips are sagging or popping up, you're basically doing bad yoga, not push-ups." | 35.24 | "Number three: core control. If your hips sag or pop up, that's not a push-up, that's bad yoga." | +4.8 s |
| 37.1 | "Keep your body straight from neck to heels. Like a solid plank that moves." | 41.31 | "Keep one straight line from your head to your heels, like a plank that moves." | "neck" → "head" |
| 42.5 | "That's it. Three small fixes, massive difference." | 45.54 | "That's it. Three small fixes, one big difference." | +3.0 s |
| 45.0 | "No fancy gym, no equipment, just clean push-ups equals clean gains." | 48.95 | "No gym, no equipment. Just clean reps and a real chest." | Different punchline |

**Missing dialogue:** the "Stop" command opener and the "fingers slightly out" cue. **Extra dialogue:** "and your chest finally starts to grow", "And keep your elbows in".

## 4. Missing scenes, animations and effects (complete list)
1. Motion blur on the hook zoom-out.
2. X-arms "stop" pose.
3. Moving push-up inset during the hook (ours is a still image).
4. Full-screen anime speed-line background, plus shiver on the flex.
5. Black aura beat with turn and shrink.
6. Kinetic "LET ME FIX THAT"-style bumper with the char.
7. Hand close-up "3 fingers" with a kinetic "ONLY".
8. Section cards with a ghost "#N" and the title moving up (×3).
9. Front-view push-up: wrong-width poses with red shoulder glow, then the correct width line.
10. Push-up bottom position, a motion/ghost trail, and a pose change every ~2 s in #1.
11. Flared-elbow wrong form for the chicken joke.
12. Straight-arm push-up with sagging or piked hips (ours uses a forearm plank).
13. "LIKE SOLID PLANK" big kinetic text.
14. 3 mini push-up recap icons.
15. Subscribe-button animation at the end.
16. Waist-up and close-up character crops.
17. Music bed.
18. Sad/aura sound.

## 5. Top 10 most serious mistakes
1. **No background music** (CRITICAL).
2. **#1 hand placement shown in side view with one still pose for 12 s.** The width cue is impossible to see, and there is no wrong-vs-right (CRITICAL).
3. **Push-up bottom never shown**, so "chest almost touches the floor" is not demonstrated (CRITICAL).
4. **#3 uses a forearm plank instead of a straight-arm push-up** with sagging or piked hips (CRITICAL, fitness accuracy).
5. Black aura/sad beat with shrink is missing (MAJOR).
6. Section cards with the ghost "#N" and the title move-up are missing (×3) (MAJOR).
7. Kinetic text moments are missing ("LET ME FIX THAT"-style bumper, "ONLY", "LIKE SOLID PLANK") (MAJOR).
8. Timing drift: ours runs 1.4–4.8 s behind the ref per section and is 2.3 s longer overall, because of the extra "CHEST: GROWING" beat and more words (MAJOR).
9. No character scale variety (always full body) (MAJOR).
10. No impact background or shiver on "look tough", and the ending has no subscribe animation (MAJOR).

## 6. How to fix each one (in order of the top 10)
1. **Music:** get `music_bed.mp3` from the owner, then add it to the plan as a music track (volume 0.025, ducked under the voice) and master at −14 LUFS.
2. **#1 hand placement:**
   - **New assets:** `hero_pushup_front_correct`, `hero_pushup_front_wide`, `hero_pushup_front_close` (front view, head toward the camera).
   - **Sequence:** wide, with a red joint ring on both shoulders, sub "TOO WIDE" (2 s) → push to close, red rings, "TOO CLOSE" (2 s) → push to correct, white dashed line between the hands (2.5 s) → side view top/mid loop for "all work together".
3. **Bottom position:**
   - **New asset:** `hero_pushup_bottom` (side view, chest 3 cm above the floor, elbows about 45°).
   - **Loop:** top → mid → bottom → mid at 0.35 s each. Red depth line from the chest to the floor only on the bottom frame.
4. **#3:**
   - **New assets:** `hero_pushup_hips_sag`, `hero_pushup_hips_pike` (straight arms, side view).
   - **Sequence:** sag + red ring on the hips → pike + red ring → correct `pushup_top_v3` + white dashed line from the ankle to the shoulder.
5. **Black beat:** `sad_beat()` on "still looks flat" (0.8 s), H crying with a `flip` entrance, zoom 1 → 0.8, `sad_sting`.
6. **Section cards:** a `section_card(n, title, at)` helper. Ghost number (size 320, opacity 0.2) + title at y 0.45 for 1.2 s. The title then moves to y 0.15 (two text layers: centre exits `up`, top enters `up`) and the exercise enters `up`.
7. **Kinetic text:** use the tool's text looks (`giant`, `echo`, `outline`, `animation: letters`):
   - **Bumper:** "HERE'S" small dark, "THE FIX" big red, around H pointing up.
   - **"ONLY":** in white over the hand close-up.
   - **"LIKE A SOLID PLANK":** 3 stacked lines over the push-up.
8. **Timing:** cut the "and your chest finally starts to grow" beat and "And keep your elbows in" (−2.5 s), and use voice speed 1.12 to land at ≈51 s.
9. **Scale:** waist-up crop preset `WAIST = {"autoAlign": False, "width": 1.3, "y": 0.8}` on attitude beats (X arms, finger up, sunglasses); a hand close-up via zoom on `count_3`.
10. **Flex beat:** a full-screen radial speed-line background layer (an image or a `burst` rays layer in orange/brown), `shiver()` on a waist-up flex, and `teeth_chatter`/whoosh. **Ending:** a subscribe-button graphic (asset or tool layer) on the chest, or keep the owner's comment CTA.

## 7. Overall similarity (subjective assessment, not a measured fact)
**Approximately 55 / 100.**
- **Matches:** the section order, the topic, the overall length within 5 %, the main beats, the cover, the zoom-out hook, the bumper position in the structure, and the push-up guide-line idea.
- **Does not match:** music, the fitness demos for #1 and #3, the push-up bottom, the kinetic typography, section cards, the black beat, and scale variety.

## 8. Verdict: **FAIL**
As a "reference-faithful" demo it fails, for three reasons:
1. Three CRITICAL demo problems: the side view for hand width, no bottom position, and a forearm plank for push-up core control. They make two of the three teaching points visually incorrect or unproven.
2. There is no music bed, which all 10 references have.
3. The signature reference techniques (section cards, kinetic text, black beat, scale changes) are missing.

The character, background, structure and timing are close enough that the fixes are additive. Most need **6 new H images** (front push-up ×3, push-up bottom, hips sag, hips pike) plus **music**.
