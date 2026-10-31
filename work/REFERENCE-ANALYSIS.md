# Reference Video Analysis + H Production System (31 Oct 2026)

Source: Drive folder `1_FLBzd0J0zkQn9ux34C4Td20vO0fXb3L` (10 videos and a `script` subfolder with 10 SRTs).
Raw data: `ref-analysis/` holds:
- `measure.json`: motion, static gaps and audio onsets per video
- `cuts.txt`: scene cuts
- `transcripts.txt`: the parsed SRTs
- `measure.py`: the script that produced them

The videos were downloaded once to `/tmp/ref/v` (container only). They were not committed, because they are third-party content.

## 0. Method, limits, checklist
**Method:**
- **Pass A (all 10 videos):**
  - ffprobe metadata.
  - SRT parse.
  - `scdet` scene cuts.
  - A 1 fps contact sheet of the full video.
  - A 10 fps contact sheet of 0–3 s.
  - Per-frame motion: mean pixel change at 30 fps.
  - Audio spectral-flux onsets.
  - One spectrogram of 0–10 s per video.
- **Pass B:** none was needed beyond the sheets.

**Limits (read before trusting numbers):**
- **Visual sampling:** the full video was sampled at 1 frame per second, and the hook at 10 frames per second. Motion between samples was measured numerically, not watched. I did not do a frame-by-frame review.
- **Audio:** I cannot listen. Sound claims come from spectrogram shapes and onset statistics, so every SFX entry below is at most **Likely**. None is **Confirmed**.
- **Performance data:** there are no views, retention or CTR numbers for the references or for our videos. Nothing below proves what drives retention; treat every rule as a hypothesis to test.
- **Character:** the references use another creator's character (a grey/blue masked figure with a "Z"). I studied only the technique. Nothing here copies that character.

| Check | Status |
|---|---|
| 10 videos inventoried | Done |
| SRT matched | 9 of 10. **V08 has no SRT** (the folder holds a duplicate V09 SRT instead). The V08 script was not analysed; its topic was inferred from the title and visuals (Low confidence). |
| SRT alignment | Auto-generated YouTube captions. They match the speech (spot-checked against caption words burned into the frames). Typos: "brachioraiialis" in V01, "tees" (teas) in V10. |
| First 3 s of all 10 | Done (10 fps sheets) |
| Sound | Partly. Categories are Likely or Uncertain; there are no exact identifications. |
| Our own videos compared | Yes, measured: `final/forearms3.mp4` and `final/day2b.mp4` |

## 1. Inventory
All videos are H.264, 30 fps, about 9:16 (608×1080; V09 and V10 are 608×1064, cropped by the downloader). Every one has a 0.1 s cover frame at the start.

| ID | Title (file) | Dur s | Topic | Exercises shown | Hook type | Words | Words/min |
|---|---|---|---|---|---|---|---|
| V01 | How To ACTUALLY Get Thicker Forearms (Fast) | 34.5 | forearms | dead hang, reverse curl (2) | problem statement | 106 | 184 |
| V02 | How To Instantly Grow Big FOREARMS (Fast) | 40.5 | forearms | wrist curl, reverse curl (2) | "Stop…" command | 116 | 172 |
| V03 | How Much Protein Do You Really Need? | 49.1 | nutrition | none (3 rules) | "Stop…" command | 149 | 182 |
| V04 | How Many Pull-Ups … Based on Your AGE? | 48.5 | standards test | pull-up (1) | question/test | 180 | 223 |
| V05 | How Many Push Ups … Based on your AGE? | 47.5 | standards test | push-up (1) | question/test | 157 | 198 |
| V06 | How Many Push-Ups Do You Really Need? | 50.9 | form fixes | push-up (3 fixes) | "Stop…" command | 141 | 166 |
| V07 | How Lean Do You REALLY Need to Look Attractive? | 44.9 | body fat % | none | myth ("Most guys think… Wrong.") | 135 | 180 |
| V08 | 3 Muscle You'll Regret Not Training | 50.5 | 3 muscles (likely forearms, traps, neck; Low) | dead hang, farmer hold, neck work | listicle preview | n/a | n/a |
| V09 | Why You Still Look Skinny (3 Fixes) | 44.6 | skinny look | deadlift (shown in hook only) | relatable problem question | 136 | 183 |
| V10 | The Only Method to Lose Belly Fat Fast | 55.8 | fat loss | none | bold claim and joke | 174 | 187 |

The editing style is shared by all 10:
- A light pastel flat background: mint (V01, V09, V10), pale blue (V02–V07) or sky blue (V08).
- One character, drawn as separate full images.
- Tiny white captions, 1–2 words at a time, placed **on the character's torso**.
- Big black headings in a condensed sans or handwritten font.
- A black-background "emotion beat" before the bumper.
- A "Let me fix that" bumper.
- An ending with sunglasses or glasses, often with a subscribe-button animation.

## 2. First 3 seconds (highest priority)
### 2.1 Hook timelines (observed from 10 fps sheets; times are ±0.1 s)
| ID | 0–0.1 | 0.1–1.0 | 1.0–2.0 | 2.0–3.0 | First spoken line |
|---|---|---|---|---|---|
| V01 | Cover: BEFORE/AFTER forearm | Skinny char flexes one arm (static pose, captions "YOUR ARMS LOOK SMALL") | 1.03 cut: a fist/forearm **grows up from the bottom edge** (scale 0.3→1 in ~0.4 s). "FOREARMS" pops in on top at 1.5. | 2.0: "ARE WEAK" pops in, with "WEAK" rotated 90° in red. 2.53: cut, "CURLS" banner slides in. | "Your arms look small because your forearms are weak." |
| V02 | Cover: DAY 1 / DAY 7 forearm | **Smash zoom-out** from an extreme chest close-up to the full crossed-arms "X" pose (0.1–0.4) | 1.1: a real photo (hand grip trainer) drops in at the top | Same hold; the photo stays. 3.4: black flex beat. | "Stop wasting time on random forearm exercises…" |
| V03 | (no cover) zoom-out from chest | Crossed-arms X. At 0.5 a **real meme video** inset drops in at the top (third-party footage). | The inset keeps playing (crying man) | 2.3: cut to a **black background**, a fat char with blue tears | "Stop eating random amounts of protein…" |
| V04 | Cover: "HOW MANY?" pull-up | Zoom-out from chest to the char **pointing at the viewer** (0.1–0.6) | 0.9–1.1: the pointing char shrinks to the bottom-right corner while a pull-up char appears above. Reps swap every ~0.4 s. | Reps continue | "Did you know how many pull ups you should be able to do based on your age?" |
| V05 | Cover: "YOUR AGE?" push-up | Same as V04 (zoom-out to pointing) | Push-up char appears behind, pointing char at the bottom-right | Reps swap | Same as V04 |
| V06 | Zoom-out from chest | Crossed-arms X, with a real push-up clip inset at the top (0.5–1.6) | 1.6: cut to a sunglasses flex on an **anime speed-line** gym background | 2.9: black background, char spinning/rotating in | "Stop doing hundreds of push-ups that look tough but build nothing." |
| V07 | Rise-in | The char **rises from the bottom edge while scaling up** (0–0.8), thinking pose | 0.9: **Y-axis flip** (the char squeezes to a sliver). Then pointing at a circle bubble of abs. | 2.5: flip again, then a sunburst background with a hands-behind-head flex | "Most guys think you need insane abs to look attractive. Wrong." |
| V08 | Cover: forearm muscles highlighted | Fade plus rise-in of the char holding **3 fanned photo cards** (a preview of the 3 muscles) | Cards settle; 3 fingers up | 1.9: a "SUBSCRIBE" t-shirt pose | (no SRT) |
| V09 | Cover: "STILL SKINNY?" | Zoom-out from chest to the deadlift pose | 1.4: the char slides out left and a new char (hoodie, drinking) slides in | Hold | "You're lifting every day, but still look skinny in clothes?" |
| V10 | Cover: "BELLY FAT?" | The char rises from the bottom edge (phone glowing) | Hold; the caption sits on a grey band | 2.5: tear face, then a black background | "Belly fat is the easiest fat to gain and the hardest to get rid of." |

### 2.2 Measured hook numbers
Motion % is the share of frames with visible pixel change.

| ID | First motion s | Hook motion % (0–3 s) | Cuts in 0–3 s | Spoken words 0–3 s | On-screen heading words |
|---|---|---|---|---|---|
| V01 | 0.13 | 48 | 4 | 9 | 3 |
| V02 | 0.13 | 69 | 1 | 7 | 0 |
| V03 | 0.13 | 91 | 1 | 8 | 0 |
| V04 | 0.13 | 53 | 1 | 13 | 0 |
| V05 | 0.13 | 43 | 1 | 13 | 0 |
| V06 | 0.13 | 83 | 3 | 9 | 0 |
| V07 | 0.13 | 44 | 1 | 9 | 0 |
| V08 | 0.13 | 30 | 2 | n/a | 0 |
| V09 | 0.13 | 39 | 1 | 7 | 0 |
| V10 | 0.13 | 28 | 1 | 10 | 0 |

Character gestures in the hook (meaningful pose changes, not zooms): 1–3 per video. Every video moves by 0.13 s, which means the first non-cover frame is already animating.

### 2.3 Hook conclusions
| Finding | Evidence | Confidence |
|---|---|---|
| Something big moves inside the first 0.2 s, almost always a camera **zoom-out from an extreme close-up of the body** to the full pose (6/10), or a **rise-in from the bottom edge** (3/10). | V02, V03, V04, V05, V06, V09 / V07, V08, V10 | High (seen) |
| A 0.1 s thumbnail/cover frame opens 7/10 videos. | V01, V02, V04, V05, V08, V09, V10 | High |
| The first pose is a **stance that matches the verbal hook**: crossed-arms "X" for "Stop…" (V02, V03, V06), pointing at the viewer for "Did you know…" (V04, V05), thinking for a myth (V07). | sheets | High |
| A second visual idea arrives at 0.5–1.1 s (photo inset, second character, cards). | V02, V03, V04, V05, V06 | High |
| A dark "emotion beat" (black background plus a sad/flex char) comes right before the bumper, at 2.3–4.9 s. | V02, V03, V06, V08, V09, V10 | High |
| Headings on screen in the hook are rare (only V01). The cover frame carries the text. | sheets | High |
| Third-party meme or real-person clips (V02, V03, V06): **do not copy** (copyright, and off-brand). | | |

## 3. Scene timelines (cuts from `scdet`, content from the 1 fps sheets)
Format: start s → scene (pose/visual; text). Exact cut times are in `ref-analysis/cuts.txt`.
- **V01:**
  - 0 cover → 0.1 skinny flex.
  - 1.0 fist grows; "FOREARMS ARE WEAK" (red rotated WEAK).
  - 2.5 three category banners slide in, stacking: CURLS (blue) / PUSH-UPS (pink) / BENCH PRESS (yellow).
  - 5.9 muscular hands-on-hips → hoodie char drinking (grip "fails").
  - 8.5 hand "2", with "Only/Moves" handwritten.
  - 11 text card "DEAD HANGS".
  - 12 front hang. "Sim…ple?" typed above the bar, with a sweat drop.
  - 15 hands on hips. 17 veiny forearm.
  - 19 "2" card. 20 reverse curl (barbell, arrows up).
  - 23 **anatomy close-up**: red muscle on the forearm.
  - 25 glasses, crossed arms. 28 X arms ("no fancy"). 31 flex (ending).
  - Longest static: 3.3 s at 31 s (the end).
- **V02:**
  - 0 cover → X arms plus a grip-trainer photo.
  - 3.4 black flex. 4.7 "LET ME FIX THAT" (kinetic, red FIX).
  - 5.7 hand "2".
  - 7 "WRIST CURLS" card. 9 kneels at a bag (red arrow).
  - 10 **arm-only loop**: curl down/up, curved arrow, "SQUEEZE!!!" red label.
  - 14 points at a skeleton arm with a green muscle. 17 one finger up.
  - 19 "REVERSE CURLS" card. 21 bench reverse curl (3 frames).
  - 24 points at the brachioradialis diagram (label).
  - 27 glasses. 30 veiny fist. 33 "2" card. 34 X arms. 37 sunglasses (ending).
- **V03:**
  - 0 X arms plus a meme inset. 2.3 black, sad fat char.
  - 4.1 "LET ME FIX THAT" (plain text). 5 hand "3" with "ONLY".
  - 7 glasses. 8 "PROTEIN AMOUNT" card.
  - 10 eating at a table, "EAT WAY TOO LITTLE" handwritten plus arrow. 12 finger up.
  - 14 text "0.7g to 1g protein / per pound of bodyweight", with a hand-drawn underline.
  - 18 flex. 20 "PROTEIN TIMING". 21 X arms.
  - 22 eating a giant bowl ("starving bear"). 25 thinking. 26 finger up.
  - 28 table with a "3–4 HIGH PROTEIN MEAL" label. 30 glasses.
  - 33 "PROTEIN QUALITY". 34 "junk protein = (sad char)".
  - 38 the food list types in line by line. 42 neutral stand. 44 4 fingers.
  - 45 sunglasses, hands behind head, with a **subscribe button animating at the top**.
- **V04 / V05 (same template):**
  - 0 cover → zoom-out, pointing.
  - 1 reps loop (pull-up / push-up), with the pointing char in the corner.
  - 3.4 finger up "Let's find out".
  - 4 per age: tag "AGE - 10" top-left plus a small char standing on a step (age = body size) → 6 the exercise with a "1-2 PULL UPS" heading, **2–3 reps at ~0.4 s swaps**.
  - 11 / 12 sunburst flex. 17–22 black background, char spins in.
  - Repeats for ages 20/30/50/60. 39 thumbs up / finger.
  - 44 thinking, with "AGE?" and "PULL UPS?" tags popping in (CTA question).
- **V06:**
  - 0 X arms plus a real clip. 1.6 speed-line flex. 2.9 black spin.
  - 3.6 "LET ME FIX THAT" (kinetic, red THAT). 4.5 "ONLY" + 3 fingers. 7 sunglasses.
  - 8.9–29 **one long push-up section with no hard cut**:
    - "#1 HAND PLACEMENT": front push-up, red glow on the shoulders, green dashed line for hand width.
    - "#2 RANGE OF MOTION": side view, the char lowers and rises (smooth interpolation, ghost trail), with a red dashed depth line.
  - 29 X arms ("don't flare like a chicken"). 30.7 "#3 CORE CONTROL": side plank push-up, red dot on the sagging hips, white dashed body line plus an arrow.
  - 35 finger up. 40 "LIKE SOLID PLANK" (metallic 3D word).
  - 43 thumbs up with 3 mini push-up icons. 46 sunglasses plus a subscribe button (ending).
- **V07:**
  - 0 rise-in, thinking. 0.9 flip → pointing at an abs bubble.
  - 2.5 sunburst flex. 3.5 "let me fix that". 4 X arms.
  - 8 soft-body char. 11 glasses.
  - 12 **3 circle bubbles stack vertically**: face → jaw → waist.
  - 19 small char in a t-shirt, with a "12–15%" red label plus arrow. 22 finger up.
  - 24 sad soft char with "soft" and "lean" labels.
  - 26 glasses. 30 X arms. 32 typed text lines ("Focus on looking ATHLETIC…").
  - 37 sunglasses, hands behind head. 40 thumbs up. 41 X arms. 42 finger (ending).
- **V08:**
  - 0 cover → char holding 3 photo cards. 1.9 SUBSCRIBE t-shirt. 3.7 black.
  - 4.9 "Let Me Fix That" (italic). 6 finger up.
  - 8 neutral → 13 a photo card of the char in a t-shirt.
  - 15 farmer hold (dumbbells, 4 frames). 19 glasses. 20 two fingers.
  - 21–26 white arrows point at the forearms (zoom in and out). 27 close-up dead hang.
  - 33 3 fingers. 35 **mirror comparison**: red arrows on the traps, the char beside a mirror.
  - 40 back view with red lines on the traps. 41 neck/upper-back exercise holding a bar behind the head (4 frames).
  - 46 neutral stands (ending, no SFX-heavy end).
- **V09:**
  - 0 cover → zoom-out deadlift. 1.4 slide transition → skinny hoodie char drinking.
  - 4.3 finger up "let me fix". 5 hand "3". 7 black skinny char.
  - 8 "#1 YOU ONLY TRAIN MIRROR MUSCLES" heading. 11 two circle bubbles (chest, biceps). 12 finger up.
  - 15 traps / shoulders / neck bubbles appear one by one. 20 sunburst flex.
  - 21 "#2 NOT EATING ENOUGH": skinny flex → X arms → eating at a table (a fork char pops in).
  - 30 "#3 BAD POSTURE": side view slouching with a phone → **cross-dissolve** to upright.
  - 40 thumbs up plus a subscribe button.
- **V10:**
  - 0 cover → rise-in, phone glow. 2.5 tear face → black.
  - 4 eating a cookie → belly pops out ("boom") → tear.
  - 7 "LET'S FIX" (red). 8 hand "3".
  - 10 "#1 Calorie Deficit". 13 **icon equation**: eat-circle = burn-circle → fat-loss icon. 18 finger. 19 X arms.
  - 25 "#2 Walk More": step icon "10,000" = calories. 31 finger.
  - 32 **number counts up** 170 → 1700+. 35 hands on hips.
  - 39 "#3 Stop Spot Reducing". 40 finger / X arms. 44 tear belly side view.
  - 48 **top-down view on a scale**. 50 thumbs up plus subscribe.
  - Longest static: 4.9 s at 19.6 s (the X-arms hold).

**Pacing facts (measured):**
- Hard cuts every 2.7–4.0 s (2.5–3.7 per 10 s); V04 is the exception at 10.7 because of the rep swaps.
- Only **17–34 % of frames have any pixel change**. These videos are mostly still drawings that change by cut or swap; they are not continuous animation.
- The longest static hold is 2.8–4.9 s per video.

## 4. How the character is animated (visual inference, not known software)
- **Main method: image replacement.**
  - A library of full-body drawings in many poses, swapped on cuts.
  - Rep loops use 2–4 drawings swapped every 0.37–0.43 s (measured in V04: cuts at 6.20, 6.60, 6.97, 7.33…).
- **Puppet/keyframe motion is rare:**
  - The V06 push-up section moves smoothly. It looks like pose interpolation with a ghost/motion trail (frame 27).
  - V02's curl arm rotates around the elbow.
- **Camera-based motion:**
  - The zoom-out in the hook.
  - Punch-ins on bumpers.
  - The pointing char shrinking to a corner (V04/V05).
- **Entrances:**
  - Rise from the bottom edge with scale (V07, V10, V05 frame 23).
  - Slide in from the left (V09).
  - Pop/scale (cards, bubbles).
  - Y-axis flip (V05 frame 39, V07).
  - A spin on black (V04, V05, V06).
  - Cross-dissolve for before/after (V09).
- **Gesture vocabulary (counted over 10 videos):**
  - Crossed-arms X "stop/no": 8 videos.
  - Index finger up "rule/tip": 9.
  - Hand close-up counting fingers "only 2/3": 6.
  - Glasses or sunglasses "smart/cool": 10.
  - Pointing at the viewer: 3.
  - Pointing at a bubble or diagram: 3.
  - Thinking (hand at head): 3.
  - Thumbs up: 4.
  - Tears / sad: 4.
  - Hands behind head flex: 5.
- **Animation principles:** there is very little anticipation or follow-through, because the poses simply swap. Readability comes from **silhouette contrast between consecutive poses** (X arms → finger up → glasses).

## 5. Exercise demonstrations
| Video | Exercise | How it is shown | Reps visible | Helpers | Credible? |
|---|---|---|---|---|---|
| V01 | Dead hang | Text card, then a static front hang, "Simple?" plus a sweat drop | 0 (static) | none | Yes |
| V01 | Reverse curl | Barbell, 2 frames, small curved arrows | ~1 | arrows | Yes |
| V02 | Wrist curl | **Arm-only close-up**, 4 frames (down, roll, up, squeeze) | 1 | curved arrow, "SQUEEZE!!!" | Yes |
| V02 | Reverse curl | Kneeling at a bench, 3 frames | 1 | none | Yes |
| V04 | Pull-up | Front view, 2 frames at ~0.4 s | 2–3 per age | none | Yes, but the knees are bent and crossed and the heading overlaps the head |
| V05 | Push-up | Front view (head toward camera), 2 frames | 2–3 per age | none | Yes |
| V06 | Push-up (3 form fixes) | Front and side views, smooth lowering | ~3 | red joint glow, green dashed width, red dashed depth, red dot on hips, white dashed body line, ghost trail | Yes; the best demo of the set |
| V08 | Farmer hold, dead hang, neck work | 3–4 frames each, arrows | 1–2 | white arrows, mirror comparison | Neck-with-bar move: unclear form (flag) |
| V09 | Posture | Side view, slouch → upright cross-dissolve | n/a | none | Yes |

None of the 10 uses a red-X / green-tick form comparison. Mistakes are shown as **one wrong pose plus a red marker** (V06).

## 6. Transitions and camera
| Type | Where (examples) | Duration | Sound sync | Use for H |
|---|---|---|---|---|
| Hard cut on a word | all (2.5–3.7 per 10 s) | 0 | usually none | **Essential** (already used) |
| Smash zoom-out from a body close-up | V02, V03, V04, V05, V06, V09 at 0.1 s | 0.2–0.5 s | Likely whoosh (Uncertain) | **Useful: test it** |
| Rise from the bottom edge with scale | V07 0–0.8, V10 0.1–0.9 | 0.5–0.8 s | Likely soft whoosh | **Useful** |
| Y-axis flip (card turn) | V05 39 s, V07 0.9 and 2.5 s | ~0.15 s | Likely swish | Optional |
| Slide out / slide in | V09 1.4 s | ~0.3 s | Likely whoosh | Optional |
| Cross-dissolve before→after | V09 34 s | ~0.5 s | none | **Useful** for posture/fat topics |
| Banner stack slide-in | V01 2.5 s | 0.2 s each | pops | Optional |
| Corner shrink (main char to the corner, a demo appears) | V04, V05 0.9 s | 0.3 s | none | **Useful** for test/level topics |
| Black-background beat | 6/10 before the bumper | 1–1.8 s | sad tonal sting (V03, V10, Likely) | Test it **without** meme sounds |
| Sunburst / speed-line background swap | V04, V05, V06, V07, V09 | 1–1.5 s | Uncertain | Optional (energy beat) |
| Camera shake | not observed | | | Avoid (owner: no shaking) |

## 7. Sound design (all inferred from spectrograms; nothing was listened to)
| Category | Evidence | Where | Confidence |
|---|---|---|---|
| Continuous music bed | The quiet floor stays at 18–25 % of median loudness in every video (`music_floor_ratio`), and steady horizontal tonal lines run through the spectrograms | all 10 | Likely |
| Sad tonal sting (vibrato zigzag) | Zigzag harmonics at V03 2.4–3.0 s and V10 2.6–3.5 s, exactly on the black/tears beat | V03, V10 (V09 3–4.3 dense block) | Likely |
| Pitched sweep (rising-then-falling arc) | Arc shapes at V02 ~3.5, V07 ~3.7, V08 3.7–4.9, V09 ~7.1 s, at the black/flex beat just before the bumper or #1 | 4 videos | Likely |
| Broadband whoosh | Short noise smears at V01 ~1.0 s (forearm grow-in), V04 3.0, V05 3.4 (the cut before "Let's find out") | several | Uncertain (masked by speech) |
| Pops/clicks on text pop-ins | Short transients near heading pop-ins; few of them were separable from consonants | | Uncertain |
| Impacts / bass hits | 1–5 low-band onsets per video; none clearly on the bumper | | Uncertain |

**Asset availability (our library `~/reel-engine-tool/public/library/sfx`, already in use):**
- **Already in our library:**
  - whoosh_soft, whoosh_big, whoosh_short, swoosh_up, swish, whip
  - pop_soft, click_soft, ding, chime, notification, counter
  - typing_loud, riser
- **Not in our library: neutral music bed.** **ASSET REQUIRED — USER TO PROVIDE OR SOURCE.** Search terms: "lofi trap instrumental no copyright 125 bpm", "YouTube Audio Library hip hop calm".
- **Not in our library: non-meme "sad" sting.** **ASSET REQUIRED — USER TO PROVIDE OR SOURCE.** Search terms: "soft piano sting sad short", "low cinematic hit soft".
- Do not take the references' sounds; the exact sources are unknown, and the meme stings break the owner's rule.

## 8. Script / SRT structure
- **Formula (8/10):**
  1. Hook (1–2 sentences, 3–5 s).
  2. "Let me fix that" (3.5–8.5 s, median ≈ 4.5 s).
  3. "You only need N…" (finger count).
  4. #1 / #2 / #3, each with name → how → why (a muscle or a number).
  5. "That's it."
  6. Recap in 3 short negatives ("No fancy gym, no equipment, just…").
  7. A one-line payoff.
- **V04/V05 (test format):**
  1. Question hook.
  2. "Let's find out".
  3. Age ladder: 6 steps with a number each.
  4. A form reminder.
  5. "Be honest, how old are you and how many can you do?" (comment CTA).
- **Speech rate:** 166–223 words/min, median ≈ 183. **Length:** 34–56 s, median ≈ 47 s.
- **Humour:** one joke per section, always a comparison:
  - "like a starving bear" (V03)
  - "flare your elbows like a chicken" (V06)
  - "bad yoga" (V06)
  - "belly waves back at you" (V10)
  - "dehydrated bodybuilder" (V07)
- **Sync:** captions are 1–2 words and change exactly on the spoken word. Pose changes land on the **keyword** of each sentence (e.g. V03 "starving bear" → giant bowl; V10 "boom" → belly pops).

## 9. Topics
| Topic type | Videos | Viewer problem | Visual potential | Fit for H |
|---|---|---|---|---|
| Body-part fix (forearms, skinny, 3 muscles) | V01, V02, V08, V09 | "I look small" | High (body changes) | High (already our Day 1) |
| Standards / age test | V04, V05 | "Am I normal?" | High (reps, ladder) | **High, and not used by us yet** |
| Form fixes | V06 | "My push-ups don't work" | Highest (guides on the body) | High (Day 11 in our plan) |
| Nutrition / fat loss | V03, V10 | "Why no progress?" | Medium (icons, equations) | Medium (we have no food assets) |
| Attractiveness / body fat % | V07 | "Do I need abs?" | Medium | Medium |

I have no view counts, so the claim "these topics win" is **not proven**.

## 10. Cross-video matrix (count of 10)
| Technique | Count |
|---|---|
| Cover frame 0.1 s | 7 |
| Zoom-out or rise-in at 0.1 s | 9 |
| Black-background emotion beat | 8 (6 in the hook) |
| "Let me fix that" bumper | 8 |
| Finger-count close-up | 6 |
| #N text cards or headings | 7 |
| Circle bubbles / anatomy | 5 |
| Rep loops by pose swap | 5 |
| Diagram guides on the body (dashed lines, glow, dot) | 1 (V06) |
| Subscribe-button animation at the end | 4 |
| Question CTA | 2 |
| Glasses/sunglasses accessory | 10 |
| Real or meme footage | 3 (avoid) |

- **A. Repeated:** a hard cut on keywords, a pose that matches each sentence's attitude, the bumper, the finger count, numbered sections.
- **B. Distinctive:** V06 guide lines on the body; V10 icon equations and number count-up; V08 card fan preview; V04 corner shrink plus age ladder.
- **C. Weak:** meme footage (copyright, off-brand); sad meme stings; headings typed over the char's head (V04/V05, which breaks our rule).
- **D. Transferable to H:**
  - zoom-out hook
  - rise-in
  - finger count
  - #N cards
  - icon equations
  - number count-up
  - guide lines on the exercise
  - before/after dissolve
  - age/level ladder
- **E. Needs validation:** the 0.1 s cover frame, the black emotion beat, 45 s length vs our 20 s, and torso-captions vs bottom-captions.

## 11. Our videos vs the references (measured, same script)
| Metric | Ours (forearms3 / day2b) | References | Note |
|---|---|---|---|
| Length | 23.2 / 18.6 s | 34–56 s | Ours is about half as long |
| Speech rate | ~225 words/min (1.3x) | ~183 | Ours is faster |
| Frames with motion | 48 / 53 % | 17–34 % | Ours moves more, but **it is the slow camera push-in (1.0→1.07)**, not new drawings |
| Longest static | 0.9 / 1.2 s | 2.8–4.9 s | |
| Hook first motion | 0.03 s | 0.13 s | similar |
| Distinct gestures/poses per 10 s | ~3–4 (pose cards) | ~3–4 | similar |

So "our videos are too static" is **not supported**. What the references have and we lack:
1. A zoom-out or rise-in **entrance** in the hook.
2. Attitude poses (X arms, finger up, finger count, glasses) changing on every sentence.
3. Guide graphics on the exercise (dashed lines, joint glow).
4. Jokes as comparisons.
5. A longer, more explained body (≈45 s).

Whether any of these lifts *our* retention needs YouTube Studio data: retention graph, "viewed vs swiped away", and average % viewed per video. **Please export those for Day 1 and Day 2.**

---
# Deliverable 2: SFX master map (for H)
All are in our library unless marked. Volume is relative to the sfx bus (0.35).

| Event | Sound | Rule |
|---|---|---|
| Hook entrance (zoom-out or rise-in) | whoosh_soft (0.6 s) | Once, at 0.1 s |
| Heading / #N card pop-in | pop_soft | Max 1 per heading |
| Bumper "HERE'S THE FIX" | typing_loud, then whoosh_big on the punch-in | Already approved; keep it identical every video (brand stamp) |
| Pose change on a keyword | none, or click_soft | Not every cut; max 1 SFX per 1.5 s overall |
| Rep loop | none (voice counts) | No per-rep sound |
| Counter / number count-up | counter | Once |
| Good tip / result | ding | Max 2 per video |
| Mistake shown | **ASSET REQUIRED**: soft low "dull thud" (not a buzzer) | Max 1 |
| CTA comment bubble | notification | Once |
| Music bed | **ASSET REQUIRED**: calm trap/lofi 120–130 BPM at 0.025 | Whole video |

Never use: sad meme stings, bruh/fahhh/meme voice sounds (the owner's rule), camera shake sounds.

# Deliverable 3: H motion and pose library
**Attitude poses (existing assets, `hero_*`):**

| Action | Asset(s) | Use when the sentence… | Hold |
|---|---|---|---|
| Stop / no | arms_crossed (v1–v7), stop_palm (v1–v5) | says "Stop…", "No…", "Wrong" | ≥1.2 s |
| Rule / tip | point_up* (use teacher_pointer if missing) | gives a rule | ≥1.2 s |
| Count "only N" | count_1…count_5, counting_fingers | "You only need 2/3…" | 1.0–1.5 s |
| Talk to viewer | point_viewer | "you", questions, CTA | ≥1.5 s |
| Thinking / myth | thinking | "Most people think…" | ≥1.2 s |
| Sad / problem | sad_crying (v2) | the pain point | 1.0–1.5 s |
| Win / result | double_biceps, thumbs_up, gag_sunglasses_thumbs | payoff | ≥1.5 s |
| Shock | shocked | a surprising number | ≥1.0 s |
| Walk in / out | walk_toward, walk_away, walking (v2) | scene start/end | 0.6 s |

**Movement recipes (tool layers we already have; proposed, not observed in our videos):**
1. **Zoom-out entrance:** camera at 0.0 s zoom 1.8 focused on the problem body part (e.g. forearm), 0.35 s ease-out to 1.0. H stays still. Then whoosh_soft.
2. **Rise-in:** H starts at y +0.35 (below the frame) and scale 0.8, then over 0.5 s ease-out goes to the final y and scale 1.0.
3. **Corner shrink:** H (pointing at the viewer) shrinks over 0.3 s to width 0.35 at x 0.8, y 0.8. The exercise loop appears in the main area. Use for test/level videos.
4. **Rep loop:** 2 drawings, 0.4 s each (0.6 s for slow moves). 3–6 swaps per move, never under 1.5 s total.
5. **Before→after:** cross-dissolve of 0.5 s between 2 poses at the same position and size (e.g. bad_posture_desk → stand).

**Exercise pose library (existing):**

| Exercise | Frames | Status |
|---|---|---|
| Push-up | pushup_top (v1–v4), pushup_mid | OK. A **pushup_bottom** is missing (request it) |
| Squat | squat_top, squat_mid, deep_squat_hold, squat_wrong, sumo_squat | OK |
| Plank | plank | Static |
| Crunch | reverse_crunch (v2) only | **Missing: crunch_down / crunch_up** |
| Leg raise | leg_raise_down, leg_raise_up (v2, v3) | OK |
| Pull-up | pullup_hang, pullup_top | OK; hang_v2 is a different view, so don't loop it with hang |
| Dead hang | look_up_bar → pullup_hang_v2 (front) | Static hang |
| Lunge | lunge (v2) | OK |
| Dumbbell | curl_down/up, row_start/end, dumbbell_hold, pick_dumbbell | OK |

**Guide graphics to add to the tool (proposed, observed in V06):**
- A dashed line between the hands (green = correct width).
- A dashed vertical line for depth.
- A red soft dot on a sagging joint.
- A white dashed straight body line.

All must stay off the face and head.

# Deliverable 4: Production SOP (per video)
1. **Topic.** Pick from `TOPICS-30-DAYS.md`. Prefer problem fixes and **tests/levels** (V04/V05 type). Check the poses exist *before* writing; request missing ones the same day.
2. **Hook (0–3 s).** One line in ≤10 words: a "Stop…", a "Did you know…", or a myth plus "Wrong."
   - Entrance: zoom-out or rise-in.
   - Pose: an attitude pose that matches the line.
   - Pain circle on the body part.
   - Heading on screen from frame 1 (our rule).
3. **Script.**
   - Bumper "HERE'S THE FIX" by 5 s.
   - "Only N moves", using a count_N pose.
   - #1…#N, each = name → 1 how-to → 1 why.
   - One comparison joke.
   - "That's it", a recap of 3 short negatives, then the CTA.
   - Simple words.
   - **Test** 30–40 s instead of 20 s (see the plan).
4. **Storyboard.** One row per sentence, with columns: pose, heading, sub, overlay, SFX. Every sentence changes the pose or the overlay. Nothing is held under 1.2 s or over 3 s.
5. **Poses.** Check them in a contact sheet first. Never loop two different camera views.
6. **Build** `build_dayN.py` from the latest approved file. Anchors are sentence words.
7. **SFX** per Deliverable 2.
8. **Captions.** Small white at the bottom (y 0.82), with yellow keywords, hidden during the bumper.
9. **Render** with `fast_render.py` (1.3x, gaps cut).
10. **QA.** Check the frames sheet for:
    - overlaps
    - anything on the face
    - static runs over 3 s
    - the heading-to-H gap
    - loudness at -16 LUFS

    Then commit, push and send the upload text.

# Deliverable 5: Reusable master production prompt
```
You are making one YouTube Short for "Effortless Exercise" with the Reel Engine tool (repo rctripsinfo-ux/RCTRIPS,
branch given by me). Read work/HANDOFF.md, work/CAPTAIN-WORKOUT-STYLE.md and work/REFERENCE-ANALYSIS.md (SOP,
SFX map, pose library) first. Use as little of my usage as possible: no subagents, one render, then fix and re-render
only if the frame check fails.

INPUT: topic = <...>; script or SRT = <... or "write it">; target length = <30-40 s>; extra assets = <...>.

CHARACTER: only H (bald, tan, white "H" on forehead, black shorts, olive harness and belt with silver buckle, black
wrist wraps, olive sneakers). Use only hero_* images from the library; never redesign him. If a needed pose is missing,
stop and give me an image prompt for it (white background, same H) before building.

OUTPUT, in this order:
1. Timestamped storyboard table, one row per sentence: time | narration | H pose asset | entrance/transition |
   heading (top, y 0.15) | sub | overlay (pain circle, bubble, counter, guide line) | caption keywords | SFX | camera.
2. build_<name>.py (copy of the latest approved build) + <name>.txt + <name>.pauses.json.
3. One render: python3 fast_render.py <name> <name>.txt <name>.json 1.3
4. Frame check of final/<name>-frames.jpg: no overlaps between text, H, bubbles; nothing on H's face/head;
   no gap between heading and H; no static picture > 3 s, none < 1.2 s. Fix and re-render only if it fails.
5. Title, description, tags, thumbnail prompt; commit and push.

RULES: hook entrance at 0.1 s (zoom-out from the problem body part or rise-in); bumper "HERE'S THE FIX" with
typing_loud by 5 s; "only N" with hero_count_N; exercises as pose loops (0.4 s, 0.6 s slow), same camera view only;
beige #E2D3B9 background; small white bottom captions, yellow keywords; no green ticks, no meme sounds, no
camera shake, simple words, one joke as a comparison.
```

# Deliverable 6: Priority plan
| # | Change | Impact (guess) | Evidence | Effort | Cost | Do |
|---|---|---|---|---|---|---|
| 1 | Hook entrance: zoom-out from the problem body part (or rise-in) at 0.1 s | High | 9/10 refs | Low (camera keys only) | Low | **Now** |
| 2 | Attitude pose per sentence (X arms, finger up, count_N, point_viewer) | Medium–High | 10/10 | Low (assets exist) | Low | **Now** |
| 3 | One comparison joke per video | Medium | 8/10 | Low | none | **Now** |
| 4 | Test format "level/age test" (V04/V05 style) using corner-shrink plus a rep loop | High (Low confidence) | 2/10 refs, our topic list has tests | Medium | 1 build | **Test (Day 10 "Stronger than 92%")** |
| 5 | Length test: 30–40 s with 3 moves vs our 20 s | Unknown | refs 34–56 s | Low | 1 extra render | **A/B test**, judge by average % viewed |
| 6 | Guide graphics for form (dashed lines, joint dot) | Medium | 1/10 (V06, best demo) | Medium (tool layer) | Medium | Test on Day 11 push-up mistakes |
| 7 | Music bed under the voice | Medium | 10/10 | Low (needs an asset) | none | Once you send a track |
| 8 | Missing poses: pushup_bottom, crunch up/down, dead bug ×2, back view | Medium | | You generate | | Ask now |
| 9 | Black-background emotion beat with no meme sound | Unknown | 8/10 | Low | | Test later |
| 10 | 0.1 s cover frame | Unknown | 7/10 | Already supported (5th arg) | | Keep using it |

**Conflict to confirm:** the brief asks for a pure white background with the top 16–20 % and bottom 12 % empty. The approved format is beige, with headings at y 0.15 and captions at y 0.82, so both sit inside those zones. I have **not** changed the approved format. If you want the white safe-zone layout, test it as a separate A/B video.

## Pass B (31 Oct): measured at 30 fps on the chosen moments
- **Black "sad" beat** (the screen goes black, then the char slowly shrinks back):

  | Video | Time | Char height |
  |---|---|---|
  | V02 | 3.43–4.70 s | 153 → 137 px |
  | V03 | 2.30–4.10 s | 176 → 146 px |
  | V07 | 3.53–4.07 s | 140 → 76 px |
  | V08 | 3.67–4.93 s | 118 → 83 px |
  | V10 | 2.50–3.87 s | 144 → 138 px |

  V04 and V05 use the black beat the other way: the char grows in for a flex.
- **Shiver:** V06 1.6–2.9 s. The flex pose jitters a few px every frame over anime speed lines.
- **Card-flip turn:** V10 4.85 s (the char squeezes thin and turns). Also V05 39 s and V07 0.9 s.
- **Rise and fade-in from below:** V01 12 s (dead hang), V07 8 s, V09 10.6 s (bubble).
- **Sounds:** I matched our `teeth_chatter` and `shiver` against all those windows: no match (score ≈ 0). Their exact sounds are not in our library. We will use our own `teeth_chatter` on shiver beats, plus a non-meme sad sting (asset requested).
