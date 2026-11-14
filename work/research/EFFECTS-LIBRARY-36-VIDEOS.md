# Effects Library: competitor Shorts, 36 videos (14 Nov 2026)

Internal research. Competitor files stay in the scratchpad; nothing from them is copied into our videos.
This file lists what we SAW and MEASURED, so we can build our own versions of the techniques.

## 1. What was checked, and how

| Check | Method | Coverage |
|---|---|---|
| Every video, start to end | Contact sheet at 2 frames/s (1 frame every 0.5 s), read by eye | 36/36 videos (first 48 s each; the 152 s v10 to the end at 1 frame/s) |
| Exact timing of key effects | Strips at 30 fps (1 frame = 33 ms) | ~25 effects (owner's 5 + transitions, pops, typing, wipes) |
| Pixel detector, every frame | Per frame at 30 fps: background brightness, whole-frame brightness, background sharpness, red/green area, frame difference, motion direction, histogram cut | 36/36 videos, 47,000 frames |
| AI (Gemini) video pass | Tried; worked on 1 video, then the API hit its quota (429/503), so the rest was done by eye | 1/36 (not relied on) |

Not checked: sound design (done in the earlier c01 study), and the part after 48 s of 7 longer videos (v04, v21, v25, v28, v29, v32 at ~10 s each). Effects found there repeat ones already listed.

Video IDs (v01–v36) map to titles in `comp2/ids.txt` in the scratchpad.

## 2. The format every video follows (seen in 30+ of 36)

1. **0.0 s hook**: the character is already doing the move, shown as a blurred extreme close-up that zooms out to the full body in ~10 frames (11+ videos).
2. **Problem + gag (2–8 s)**: a relatable situation plus a visual joke, e.g. inflating fat, thought bubble, phone at 2 AM, super-saiyan aura, red X-ray disc on the belly.
3. **Bumper**: grey "LET ME FIX THAT" (or "HERE'S HOW") **typed on the empty set with a blinking cursor** (20+ videos).
4. **Sections**: each starts with a section marker (giant grey number behind the character, "#1" on a dark slate brush wipe or circle iris, or a hand showing 1/2/3 fingers). During the exercise:
   - a small **circle inset** sits at the top, showing the muscle;
   - **ghost reps** and **dashed motion arcs** show the movement;
   - **red or green muscle fill** marks the muscle.
5. **Ending**: a pointing or leaning close-up, or a callback to the opening joke. Sometimes an icon "explosion ring" plus a video card on top.

## 3. Owner's 5 screenshots (v05), measured frame by frame

| # | Effect | Exact look | Timing (measured) |
|---|---|---|---|
| 1 | **Circle badge with a red X** (top right) | Slate circle, dark rim, a bicep drawing inside, red X at its top right | Grows from ~10% to 100% in ~0.27 s with an ease-out pop. Stays on screen. |
| 2 | **Red circles on both forearms** | Translucent red disc (~55% opacity), lighter dashed rim | Grow from 0 to full in ~0.3 s |
| 2b | **Whole frame dims** at the same moment | Background brightness 198 → 110 (**−44%**); the character and badge darken too, **only the red circles stay bright** | 1.0 s ease-out (fast at first, then slower); stays dim until the transition |
| 3 | **Brush wipe** transition | Rough paint-brush strokes sweep in from the top | 3–4 frames (0.1–0.13 s). The next scene's background is a darker slate (brightness 148). |
| 4 | **Green muscle BLINK** | Solid green fill on the bicep | **on 3 frames → off 3 frames → on and stays** (2 blinks, ~0.1 s each) |
| 5 | **Cameo with the scene behind faded and blurred** | Muscular character fades and scales up over the old scene, which stays as a faint blurred ghost | ~0.5 s overlap |

## 4. Effects library (seen in at least N of 36 videos, read by eye)

Status = what our engine (director.py) can do today. Have, Partial or Missing.

### A. Transitions / screen changes
| Effect | Look and timing | Seen in | Status |
|---|---|---|---|
| Blurred close-up zoom-out (hook) | 2x close, motion blur, out to full body in ~10–12 frames | 11+ | Have |
| Squash ("flip") | Character squeezes to a vertical line in 4 frames (ease-in), 1 empty frame, new character expands from the line in 6 frames (ease-out). ~0.37 s. Used for before/after body changes. | 4 | Missing |
| Brush-stroke wipe | Dark slate paint strokes cover the frame in 3–4 frames; reveals a giant "#1" on a dark background | 2 | Missing |
| Circle iris in/out | A big slate circle grows from one side to fill the frame (in), or a circular mask shrinks to close a scene (out) | 2 | Missing |
| Blinds / bar wipe | Vertical stripes of different widths slide in and change the background colour (one colour per list item) | 3 | Missing |
| Diagonal stripe wipe | Red, pink and dark-red angled wedges sweep in from the left in ~8 frames and leave a red "danger" background | 1 | Missing |
| Stair-step bars | Dark slate step blocks rise from the bottom one by one under a seated or standing character | 4 | Missing |
| Crossfade between poses | 0.35–0.6 s dissolve; the old pose is visible as a ghost (weak → strong body, sad → happy) | 9 | Partial (fade layer only) |
| Inset grows to full screen | Circle inset zooms until it fills the frame, then the next scene starts | 2 | Missing |
| Slide in/out from the edges | Character or giant number slides in from a frame edge (ease-out, ~10 frames) | most | Have |
| Ranking carousel | Characters pass right → left in a conveyor (~0.5 s per level), grey label above each, commentator in the corner | 3 | Missing |
| Tilted end card | The scene shrinks into a rotated photo frame | 1 | Missing |

### B. Highlights / pointing at things
| Effect | Look and timing | Seen in | Status |
|---|---|---|---|
| Red muscle fill / disc | Solid or translucent red over the muscle; sometimes pulses; soft red glow for pain | 17+ | Partial (paint, no pulse or glow) |
| Green muscle fill + blink | Green fill (correct or working muscle); blinks 2x then stays | 11+ | Partial (paint, no blink) |
| Red translucent forearm circles + dim | See section 3 | 2+ | Missing |
| Circle inset badge | Slate or cream circle with a muscle or object drawing, dark rim. Pops from ~125% (blurred) down to 100% in ~4 frames, or grows from small. Often big at the centre first, then shrinks to the top. | 21+ | Missing |
| X-ray disc on the body | Red disc on the belly showing the food inside (fat), sometimes with a meter beside it | 3 | Missing |
| Dashed motion arcs | Grey, green or red dashed curves with arrowheads along the movement path | 11+ | Partial (ghost only) |
| Ghost reps (onion skin) | 2–4 faded copies of the moving limb or body | 6+ | Have (aligned pairs only) |
| Straight guide lines | Grey or red dashed line along the body or bar path (alignment) | 5 | Missing |
| Sight-line cone | Red translucent cone from the eyes (where to look), fades out | 2 | Missing |
| Red DOWN-arrow block | Translucent red arrow on a sagging body part | 1 | Missing |
| Correct-form green ghost | Green translucent copy of the correct position laid over the wrong one | 1 | Missing |
| Dark translucent box | Rectangle behind a moving fist or limb (focus box) | 1 | Missing |
| Red X / green tick | Drawn mark beside wrong or right equipment; ticks appear on insets one by one | 6 | Missing |

### C. Background / whole-frame changes
| Effect | Look and timing | Seen in | Status |
|---|---|---|---|
| Whole-frame dim / spotlight | Frame darkens 27–45% in 2 frames to 1 s while one element stays bright, or a new big character steps in front | 7+ | Missing |
| Background blur behind focus | Others go soft while a close-up character talks in front | 2+ | Missing |
| Stage spotlight cone | White light cone from the top onto the character (reveal or win) | 6 | Missing |
| Radial sunburst | Grey or white rays behind a winner, a food reveal or a flex | 6 | Missing |
| Dark slate section background | Full background switches to ~#4B5568 for "#1" section cards | 4+ | Missing |
| Gradient darkening | Top → bottom gradient darkens for a sad moment | 2 | Missing |
| Set colour | ~#BAC8D0 (most); light grey #E0E0E0 variant; solid red for "NO" | all | Have |

### D. Text / graphics
| Effect | Look and timing | Seen in | Status |
|---|---|---|---|
| Typewriter bumper + cursor | Grey condensed bold caps, ~33 characters/s, blinking bar cursor, held ~1 s, ~35% height | 20+ | Partial (typing yes, cursor no) |
| Giant grey section number | 1/2/3 or "#1" behind the character; fades out (~0.5 s) once the exercise starts | 13+ | Have |
| Giant grey stat | "87%", "4,000", "2:00 AM", "100", "90%" behind the character; slides or rises in | 8 | Have (bgwords) |
| White label boxes | Small white rounded boxes, thin dark border. Drop from above (~8 frames, ease-out, motion blur) or stack one by one into a list; leader lines to insets. Some show BLURRED text that is revealed later (curiosity gap). | 27+ | Partial (tag style) |
| Stacked grey words | Several typed words pile up behind the character (SETS / REPS / REST / WEIGHT) | 3 | Partial |
| Arched text | A word curved over the head | 1 | Missing |
| Coloured bold word drop | Red heavy caps ("MUST", "TERES MAJOR") drop with motion blur, then fade | 2 | Missing |
| Equation / flowchart layout | Icon + icon = result, or tree lines from an inset to labels, built one item per spoken noun | 5 | Missing |
| Progress / level bar | Small bar at the top that fills green or drains red | 5 | Missing |
| UI mock-ups | iOS toggle, slider, search bar, smartwatch, running stopwatch, clock | 6 | Missing |
| Spinning prize wheel | Half a wheel at the screen edge, segments rotating | 2 | Missing |

### E. Characters / props / gags
| Effect | Look and timing | Seen in | Status |
|---|---|---|---|
| Commentator cameo | Second character rises or peeks from a bottom corner, small, in front | 15+ | Have |
| Aspiration ghost | Big faded muscular copy behind a small or fat character (dream body) | 6 | Missing (easy: layer alpha) |
| Icons in an arc / ring | Circle icons pop one by one in an arc around the head; final "explosion" ring with lines | 14+ | Missing |
| Thought / speech bubbles | Cloud with a drawing inside; spiky white or grey speech bubbles as dialogue | 7 | Missing |
| Props pop per noun | Food or objects pop in one by one, stack, multiply, or are tossed into the frame | 4+ | Have (pop) |
| Body inflate / grow | Character scales fatter or bigger over ~1.5 s | 3 | Missing |
| Gags | Sunglasses + smoke puffs, super-saiyan aura, rainbow, girls reacting, Pac-Man chomp | 8 | Missing |
| Particles | Green PLUS signs floating up (growth), blue electric sparks, fire on an object, music notes, sparkles | 10 | Missing |
| Stress / shock lines | Anime lines above the head, spiky impact stars, trembling outlines, speed lines | 7 | Partial (shiver) |
| Screen-in-screen | Phone or TV frame showing a video; end "watch next" card | 4 | Missing |

## 5. Pixel detector numbers (36 videos, 26.1 min)

- **Hard cuts:** 5.7/min. They appear in only 15 of 36 videos; most changes are on-set layer moves.
- **Red highlight appears:** 2.4/min (27/36 videos).
- **Green highlight:** 0.7/min (11/36 videos).
- **Detected wipes:** 1.8/min (18/36 videos). Directions: up 21, left 20, right 5, down 2.
- **Measured dims:** median depth −27%, onset 2 frames (fast) up to 1 s (owner's v05 example, −44%).
- The automatic blink counter was too coarse: it missed 3-frame blinks. Blinks were checked by eye at 30 fps instead.

## 6. Build priority (most-used first)

1. Circle inset badge (pop-from-big, big-centre-then-shrink-to-top, red X / green tick).
2. White label boxes (drop with blur, stacked list, leader lines, blurred-text reveal).
3. Muscle fill upgrades: blink 2x then hold, pulse, red glow, translucent disc with dashed rim.
4. Whole-frame dim (keeps chosen elements bright) + background blur behind a focus layer.
5. "LET ME FIX THAT"-style typewriter bumper with a blinking cursor (our own wording).
6. Dashed motion arcs and straight guide lines.
7. Transitions: squash, brush wipe, circle iris, blinds, stair steps, crossfade.
8. Icons in an arc around the head, thought / speech bubbles, aspiration ghost.
9. Backgrounds: spotlight cone, sunburst, dark slate section card.
10. Particles (plus signs, sparks, fire), progress bar, UI mock-ups, ranking carousel.
