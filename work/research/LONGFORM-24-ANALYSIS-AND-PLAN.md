# Long-form analysis: 24 Yellow Dude videos, and our production plan

Date: 16 Nov 2026.

**Sources**
- The owner's Drive folder: 24 videos, 1280x720, 1:15 to 11:04 long, 3 h 11 min in total.
- Raw videos, transcripts and frame sheets stay in the session scratchpad (competitor material, not committed).

**How we measured**
- **Sampled frames.** Every video got a 36-frame overview sheet. Five videos (L04, L11, L14, L17, L21) got second-by-second sheets of 17 s each.
- **Motion.** Measured at 6 fps on every video (`motion.py`).
- **Shot cuts.** Counted with ffmpeg scene detection.
- **Words.** Every word was transcribed with timestamps (faster-whisper; small.en for L01–L02, base.en for the rest).
- **Our video.** The same motion measurements were run on our `final/long01.mp4`.

---

## 1. The numbers

| | Yellow Dude (median of 24) | Our long01 |
|---|---|---|
| Length | 8:05 (4:00 to 11:04) | 4:38 |
| Speech | 150 wpm (126–179) | ~155 wpm |
| Sentence length | 7–10 words | 6–8 words |
| Screen moving (frame-to-frame change) | 64% of the time | 66%, but mostly the "breathe" wobble and swap flicker |
| Big visual changes | ~15 per minute (one every 4 s) | 36 per minute, all hard pose swaps with no in-between motion |
| Longest still stretch | ~10 s | 1 s |
| Burned-in captions | **none** | yes, on every word |
| Background | one pastel colour per video, darker panels of the same hue | plain white |
| Text on screen | a few big italic keywords, no boxes | a white box label on almost every line |
| Different drawings per video | ~100–250 | ~40 (13 new + gesture library) |

Views (from our outlier sheet):
- 6-pack morning routine: 3.7M
- Quit gym, do calisthenics: 3.4M
- Laziest way to build muscle: 3.1M
- Shoulders: 3.0M
- Dead hang 30 days: 2.6M
- 100 burpees a month: 2.4M
- Grip: 2.4M
- Core: 2.3M
- Home calisthenics: 2.3M
- The boring exercise: 2.7M
- Everything before calisthenics: 2.7M

All of these are 6–15x the channel median.

**Why ours felt flat (फीकी):**
1. **It is the same picture over and over.** H stands left, a white box appears on the right, and the next scene repeats the layout. Yellow Dude never repeats a layout twice in a row.
2. **Nothing travels.** Our poses swap in place, so the eye sees flicker. Their elements slide, grow, draw on, zoom through and orbit, so the eye sees motion.
3. **It has no world.** Ours is white emptiness. They show rooms, a bed at night, a desk, a park, a globe, a gym in line-art, fire, rain and charts.
4. **There is too much box text.** Our boxed labels plus captions read like a slideshow. They show one or two big words, and the picture carries the meaning.
5. **It is too short and too thin.** At 4.6 min, each week got one or two beats. They give each stage 40–70 s with a problem, a reason, a fix, a joke and a number.

---

## 2. The visual system (what is on screen, frame by frame)

### 2.1 Character and drawing style
- **One mascot.** A flat yellow skin, grey sleeves and shorts, clean black outline, and cel shading in 2 tones. The style is identical in all 24 videos.
- **Many drawings.** A new drawing appears every ~3–4 s. The same pose is rarely reused in one video unless it is a callback.
- **Many instances at once.** One talking H in front, with 1–5 small H's behind doing the exercise (L17 0:01, L21 1:45). There are also line-ups and crowds (L09, L20), "past me" ghosts, and before/after pairs.
- **Scale changes all the time.** A shot can be:
  - an extreme close-up (hands on the bar, eyes, a bicep)
  - a waist-up talking shot
  - a full body
  - a tiny figure in a big world (on a globe, a mountain, a track)
- **Point-of-view shots.** First-person hands hold a phone, an eye mask or a bar (L11 2:15, L09).

### 2.2 Colour
- **One pastel hue per video:** light blue (13 videos), lilac (6), cream (4) or charcoal (1).
- **Darker panels.** Chapter cards and data panels use a darker tone of the same hue (L12 purple, L18 navy "REALITY CHECK").
- **Fixed accent meanings:**
  - red = muscle working, pain, warning, an X
  - green = healing, "+", correct, a tick
  - orange fire = intensity or burn
  - blue water = sweat or recovery
- **Black is for drama only:** "DAY 1" cards and the dark "POOR LIFE CHOICE" panel.

### 2.3 Scene types: the catalogue (each seen in 5 or more videos)

| # | Scene type | Examples |
|---|---|---|
| A | Talking pose, waist-up, with a gesture (think, point, shrug, cross arms, facepalm) | every video |
| B | **Exercise loop**: a 2–4 frame rep cycle at real tempo, side view, sometimes a motion-blur ghost | every video |
| C | **Anatomy cut-away**: red muscle on the body, a skeleton or spine, an organ (heart, lungs) | L02, L05, L06, L13, L14, L17 |
| D | **Circle insets**: a zoomed crop (grip, muscle, lungs) next to the body, sometimes linked by lines | L04, L13, L17, L20 |
| E | **Data visuals**: bar charts growing day by day, curves drawn on, progress bars, stopwatch rings ("30 Sec"), week calendars, tables, checklists, pyramids, a staircase, citations "[PubMed 27433992]" | L04, L14, L18, L20, L21, L22 |
| F | **Environment**: a room, an office desk, a bed at night, a city, a park, a running track, a gym drawn in line art, outer space | L10, L12, L13, L14, L17 |
| G | **Visual metaphor**: fire aura, sweat rain, battery, door, finish line, mountain, globe, crown, brain, a laboratory capsule | L11, L13, L14, L17, L21 |
| H | **Kinetic type**: 1–3 big italic words that slide or type in ("IT'S NOT", "CALISTHENICS", "NO MORE EXCUSES"), sometimes behind the figure | L03, L11, L17, L21 |
| I | **Phone or app UI**, product shots and sponsor segments, at ~35–50% of the runtime | 14 of 24 |
| J | **Section cards**: "DAY 1", "WEEK 1 REALITY CHECK", "Exercise #1", "THE EXERCISE" | L04, L05, L18, L13 |
| K | **Comedy beats**: ??? marks, sweat drops, stress lines, speech bubbles, emoji, a cat, a doctor, "past me" | every video |

### 2.4 Motion grammar (what makes it feel alive)
1. **The camera is never locked.** It does a slow push-in or pan on every scene, and a quick punch-in on key words.
2. **Things enter.** Elements slide in from the side with overshoot, pop in at 110% and settle, fade up, or scale from a point.
3. **Things build.** Bar charts grow bar by bar (L21 1:37), curves draw from left to right, calendars fill with ticks, and timers count.
4. **Loops run at rep tempo** (about 0.8–1.2 s per rep) while the voice talks.
5. **Transitions are motivated:**
   - zoom-through: push into the body, a colour fill, then the next scene (L11 0:11)
   - whip-pan with motion blur (L17 0:10)
   - blur dissolve
   - iris circle (L19)
   - a hard cut on a joke
6. **Big change every ~4 s, small motion in between.** In a static stretch, something still moves: particles, ghost trails, a slow zoom.
7. **There are no burned-in captions.** Text is reserved for the key idea.

---

## 3. The script system (word by word)

**Speed and sentences**
- 150 wpm and short sentences.
- About one question per 40 s (4–16 per video).
- "you" is 5–12% of all words: the viewer is talked to directly.
- Challenge videos switch to "I" (L04 6.6%, L18 4.4%).

**Hook (first 15–20 s):** pain or a bold claim, then a specific number, then a twist and a promise. Examples:
- "The plank minute feels longer than a normal minute… I tested it for 30 days, starting at **23 seconds and finishing at 247**. The surprising part wasn't my core. It was what happened in my head." (L18)
- "Go hang from a bar right now… a **140,000 person study** says it predicts how long you're going to live, better than your blood pressure." (L13)
- "10 squats. Sure. 15. Still good. 20, and you're thinking about lunch. Then rep 25 shows up…" (L02, a countdown hook)

**Body structure.** Each stage is 40–70 s and follows the same sequence:
1. what happened (with numbers)
2. why it happens (science, often cited on screen)
3. the fix or the cue
4. a joke
5. a mini result

The stages are:
- **Challenge videos:** day or week stages.
- **List videos:** exercise #1–#5.
- **Explainers:** myth → truth sections.

**Humour.** One line every 20–30 s, mostly visual metaphors you can draw:
- "At one minute you're basically a coffee table. Please place cups gently."
- "My stomach still looks like it enjoys weekends."
- "The receptionist says free Wi-Fi… slower than your weight-loss progress."

**Honesty beat.** Each video says what did NOT change (no visible abs, no muscle growth, my back got worse first). This builds trust.

**Ending:**
1. a takeaway rule ("You don't need motivation every day. You need a plan…")
2. a comment CTA tied to a number ("Post your baseline and your day-30 time")
3. a sign-off ("Now go train!")

**Sponsor.** In 14 of 24 videos the sponsor comes in naturally at the point where a problem appears (boredom → jump rope).

---

## 4. OUR PLAN: how we make long videos from now on

The plan has two parts:
- **What we keep:** H and Mini-H, the brand colours, and our comic style. We do not copy the yellow mascot.
- **What we change:** we copy the *grammar*: density, motion, a world, data visuals and the script shape.

### 4.1 Look
- **Background:** one light tint per video from a brand-safe set: pale teal `#DDEFED`, pale blue-grey `#E3E8F0` or pale lilac `#E6E1F2`. No white, no cream, no orange (owner rule).
- **Panels and cards:** a darker tone of the same tint. Day and chapter cards are dark red `#7A1A1A` with white extra-bold italic text, matching the thumbnails.
- **Accents:**
  - red: muscles and warnings
  - green `+`: growth and correct
  - teal: data
  - fire: intensity
- **Text:** no boxes and no burned captions in long videos. Show 1–3 big white or dark italic keywords that slide in, and upload an SRT (we already have every word's timing) as YouTube subtitles.

### 4.2 Asset library (a one-time build, reused forever)

Each Codex image takes ~1 min, and 3 run in parallel.

| Pack | Count | Use |
|---|---|---|
| Talking poses, waist-up, 3/4 view (think, point, shrug, cross, facepalm, shock, laugh, tired, proud, sweaty, sleepy, phone) | 30 | type A |
| Exercise loops: push-up (normal, knee, wall, decline, diamond, wide), squat, lunge, plank, side plank, burpee (4 frames), pull-up, dead hang, dip, crunch, leg raise, jumping jack, mountain climber, bridge, dead bug, jump rope | 25 loops (2–4 frames each) | type B |
| Anatomy: red-muscle overlays for chest, triceps, shoulders, core, quads, glutes, back, forearms; heart, lungs, brain/nerves, tendons | 15 | type C/D |
| Worlds: bedroom night, living room, office desk, park, city street, running track, line-art gym, kitchen | 8 backdrops | type F |
| Props and metaphors: fire aura, sweat drops, battery, calendar, stopwatch, phone, biscuit, plate, door, finish line, mountain, globe, mirror | 20 | type G |
| Mini-H reactions | 10 | comedy beats |

After the library exists, each new video needs only ~30–50 topic images (about 20 min of Codex time) instead of 150.

### 4.3 Engine upgrades (`work/director.py`, LANDSCAPE mode)

1. **Camera drift on every scene,** plus punch-ins on keywords.
2. **Enter and exit moves:** slide with overshoot, pop 110%→100%, scale from a point, fade up. Exits leave before the next element enters.
3. **Exercise loops at tempo with in-betweens:** a cross-dissolve of 2–3 frames between poses and a motion-blur ghost. This replaces hard swaps, so flicker goes from 36 hard changes/min to ~15 "real" changes/min.
4. **Multi-figure layouts:** a main H plus 1–4 small H demo loops, line-ups, and "past me" ghosts.
5. **Data builders:**
   - bar chart growing day by day
   - curve drawn on
   - progress bar
   - stopwatch ring that counts
   - week/month calendar that fills with ticks
   - checklist
   - stat number counting up
   - citation tag in the corner
6. **Kinetic type:** big italic words that slide or type in, optionally behind the figure.
7. **Backdrop layer:** worlds with a slow parallax.
8. **Transitions:** zoom-through (into an element → colour fill → next scene), whip-pan with blur, blur-dissolve, iris, and a hard cut on jokes.
9. **Particles:** plus signs, sweat drops, question marks, stars, fire flicker.
10. **QA:**
    - label QA in landscape (already works)
    - a "variety check" that warns when two scenes in a row use the same layout
    - a motion check: the longest still stretch must be under 3 s, and big changes must stay between 10 and 20 per minute

### 4.4 Script rules (long video)
1. **Length:** 7–9 min, ~1,100–1,300 words, 150 wpm, sentences ≤ 10 words, about one question per 40 s.
2. **Hook (0–20 s):** pain or a claim, then a specific number, then a twist and a promise. Never a slow intro.
3. **Stages of 40–70 s,** each following the same sequence:
   - what happened (with a number)
   - why (science, cited on screen)
   - the fix or the cue
   - a joke you can draw
   - a mini result
4. **Mini-H:** Mini-H is the viewer's voice and makes the joke beats, every ~30 s. H is the coach.
5. **Honesty beat:** what did NOT change.
6. **End:** a takeaway rule, then a comment CTA tied to a number, then a sign-off line ("Now go train!").
7. **Beat sheet, written with the script:** one visual beat per 3–4 s (~140 beats for 8 min). Each beat names a scene type (A–K) and its assets. No two neighbouring beats use the same type.

### 4.5 Pipeline per video (after the library and engine are built)
1. Topic (outlier list), then script + beat sheet: owner approval.
2. Voice: `tools/long_voice.py`, chaptered, gemini-3.8-flash-tts.
3. Assets: ~30–50 Codex topic images + the library, then align and cut out.
4. Plan from the beat sheet, then preview stills (6 sheets), then the full render (~1 h for 8 min), then label + motion + variety QA.
5. 16:9 brand thumbnail, upload text with chapters, SRT subtitles. Commit everything.

### 4.6 Order of work
1. **Demo first (approval gate, like the shorts):**
   - a 60–90 s 16:9 demo of the new system
   - content: the "100 push-ups / 30 days" hook + Week 1, rewritten with the new script rules
   - it shows every new element: world backdrop, multi-figure, chart build, stopwatch, zoom-through, kinetic type, no captions
2. Owner approves (or corrects) the look.
3. Build the asset library (§4.2) and finish the engine upgrades (§4.3).
4. Remake long video #1 at full length (8 min) with the new script.
5. Then one long video per week, using THE METHOD (long), saved as a skill.

---

# DEEP PASS: following `LONGFORM-ANALYSIS-PROMPT.md`

**What was run on all 24 videos (plus our `long01` for comparison):**

| Pass | Detail |
|---|---|
| `fx16x9.py` | 30 fps forensics. 315,000 frames, 4,433 transition and motion events. |
| `audio_fx.py` | Loudness, music bed, onsets. |
| Script statistics | Computed from every word. |
| Sync | Every visual event checked against word timings. |

**What was verified by eye:**
- 16 event examples were checked as 30 fps strips: 2 per class, from different videos.
- Plus the 5 second-by-second sheets and the 24 overview sheets.

## D1. Transitions and motion: measured (median of 24 videos, per minute; durations at 30 fps)

| Event (verified by eye) | Theirs per min (range) | Duration | Ours per min |
|---|---|---|---|
| **Hard cut**, mostly on a new sentence or a section card | 2.1 (0–26) | 1 frame | **22.9** |
| **Camera move**: continuous pan, tilt, push-in or pull-out on a held picture (L13, L09, L10 strips) | **5.1** (0–12) | 20 frames (8–33), ease in and out | 3.2 |
| **Dip-to-background**: the old scene fades to the bg colour, then the new elements fade or pop in (L04, L20 strips) | 3.4 (0–13) | 11 frames out (8–19) + ~6–8 in | 8.6 (our hard swaps) |
| **Blur or grey-dim out** before the next scene (L22 strip: grey overlay over ~12 frames) | 3.2 (2–19) | 5 frames (4–16) | 7.8 |
| **Slide/move** of an element (enters from the side, eases out) | 2.2 (0–6) | 5 frames (4–11). Half the distance is covered in the first third (ease-out). Overshoot in only 18%. | 4.3 |
| **Scale pop**: insets and badges grow from a point near the body to 100% (L17, L03 strips) | 1.6 (0.4–9) | 4–5 frames, ease-out, no bounce | 0.9 |
| **Zoom + move** (zoom-through) | 0.6 (0–1.4) | 19 frames | 0 |
| **Section card**: a cut to a dark panel ("DAY 3" navy `#3c4870`, "WALK DAILY" dark blue, white bold text) for ~1–1.5 s, then a hard cut to a close-up | 0.3 per min (cut + colour change) | 4 frames | 0 |
| Small swaps (rep loops, puppet motion, UI micro-animation) | 52 (16–166) | 1–3 frames | 88 |

**Read the table like this:**
- They use **few hard cuts and many soft moves:** camera moves, fades and pops.
- We use **10x more hard cuts**, plus "flash" jumps (10 per min vs 0.9). That is exactly the flicker the owner felt.
- **Characters are never frozen.** The L23 strip shows a slow head and body tilt ("puppet" motion) on a held drawing. Fire auras flicker frame by frame (L17). Phone UIs scroll (L18, L21). Stars fill one by one (L12).

## D2. Colour, dim and glow: measured
- **Background:**
  - one tint for 70–100% of each video: blue `#CCD8F0` (13 videos), lilac `#D8CCF0`/`#CCCCE4` (7), cream `#F0E4CC` (4), charcoal `#303030` (1)
  - **darker panels of the same hue** for 2–20% of the time: lilac `#9078B4`/`#605484`, blue `#84A8D8`/`#243C78`, dark `#303030`
  - our long01 is 74% white `#FCFCFC` and 19% grey `#CCCCCC` (the Mini-H focus blur)
- **Dims:**
  - 1.7 per min, lasting 47–189 frames
  - they darken the background for a "serious" stretch or a card. They are not a blur behind every cameo.
  - ours: 6.9 per min
- **Red highlight:**
  - on screen 1.9 times per min, median 67 frames
  - it is a steady red muscle overlay or a glowing red joint, usually inside a circle inset (L03, L15 strips)
  - ours: 0.2 per min
- **Green:** rare (0.1 per min), only for healing or "correct".
- **Glow:** soft halos around hot joints and white spotlights or rays (L15 strip, L13 overview).
  - The automatic glow count is not reliable: our white background inflates it.

## D3. Audio: measured
- **Loudness** is not standardised:
  - −10 to −27 LUFS (median −19)
  - true peak around 0 dBFS
  - YouTube normalises long videos to about −14 anyway
- **Music bed:** present in all videos, sitting **7–23 dB under the voice** (median ~11 dB).
- **SFX:** I could not separate them reliably from music and speech. Onsets near visual events: 13%, the same as the random control (13%). So "SFX on every cut" is **not proven**, and SFX density is **not measured**.

## D4. Sync with the words: measured
- Visual events land on word starts: the median offset is **−0.03 s**.
  - 42% are within ±0.1 s of a word start.
  - 35% come **before** the word.
  - 23% come after it.
- **Rule for us:** start the move 0–3 frames before the keyword.

## D5. Script numbers (every word, all 24)

| Measure | Value |
|---|---|
| Numbers spoken | 0.7–9.3 per min. Challenge videos are the highest: L18 9.3, L14 8.4, L02 7.7. |
| Open-loop phrases ("the surprising…", "here's the thing", "turns out") | 0–7 per video |
| Science words (study, research, percent) | up to 10 per video. Explainers are the highest: L21 10, L13 7, L20 6. |
| Sponsor read | 14 of 24, placed at 16–89% of the runtime (median ~55%) |
| Ending | comment/like/subscribe in about half. "Now go train!" in 2. |
| Stage cues ("day X", "week X", "first", "next", "exercise N") | 3–29 per video. Challenge format: 17–29. |

## D6. Effects spec for `director.py` (build these 1:1)

| Effect | Spec |
|---|---|
| Camera move | every held picture drifts: push-in 3–6% over the scene, or a pan/tilt over 20–33 frames, ease in and out |
| Dip-to-background transition | old scene α→0 over 8–12 frames into the bg tint, then new elements fade or pop in over 6–8 frames, staggered 3–4 frames |
| Blur/grey-out transition | 4–12 frames, grey overlay up to ~35% |
| Slide-in | 5 frames (up to 11), cubic ease-out, overshoot rare (≤ 5%) |
| Scale pop | inset or badge from 0→100% in 4–5 frames, ease-out, anchored near the body part it explains |
| Section card | dark panel of the video hue (for us dark red `#7A1A1A`), white bold sans, 1–1.5 s, hard cut in and out |
| Puppet motion | ±1–2° rotation and ±1% scale, slow (2–4 s), on every held figure |
| Frame-by-frame FX loops | fire, sweat, stars filling, UI scroll |
| Highlight | steady red overlay inside a circle inset, held ~2 s (not a fast blink everywhere) |
| Rates per minute | hard cuts ≤ 3, soft transitions ~10, camera moves ~5, insets/pops ~2, section cards when the stage changes |
| Timing | moves start 0–3 frames before the keyword |
| Audio | music 10–12 dB under the voice. Normalise the final mix to −14 LUFS for long-form (YouTube target), not −20. |
