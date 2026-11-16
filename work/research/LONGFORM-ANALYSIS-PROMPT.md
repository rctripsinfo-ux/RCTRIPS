# Prompt: forensic analysis of animated long-form videos (use for any reference channel)

You are analysing reference videos so that we can rebuild their *craft* (not their character or art) in our own engine (`work/director.py`).
Every claim must be **measured** (a number, a frame time) or **seen** (a frame you looked at). Write "not measured" where you could not measure something. Never guess.

## 0. Setup
- Download every video to the scratchpad. Never commit competitor media or transcripts.
- Note each video's id, title, length, resolution and fps, plus its views and multiple of the channel median when known.
- Tools are in `work/research/longform_tools/`:
  - `tx.py`: words with timestamps
  - `uni.py`: contact sheets
  - `motion.py`: motion stats
  - `fx16x9.py`: 30 fps effect forensics
  - `audio_fx.py`: audio layer
  - `strip.py`: 30 fps strips around one event

## 1. Audio layer (every video)
1. **Loudness.** Measure integrated LUFS and true peak.
2. **Voice.**
   - words per minute, overall and per section
   - pauses longer than 0.4 s and 0.7 s
   - sentence length
   - energy over time
3. **Music.**
   - Is there music under the voice?
   - Measure the music level in the speech gaps (dB under the voice).
   - Note genre and tempo by ear only if possible. Otherwise write "not measured".
   - Does the music change at section boundaries?
4. **SFX.**
   - Find onsets that are not speech: spectral-flux peaks in the gaps and transients over speech.
   - Report the count per minute.
   - Classify each one: whoosh, pop/click, ding, impact, riser, comedic.
   - Check whether SFX line up with visual events (the time gap in frames).

## 2. Script layer (every word)
1. **Hook (0–20 s):**
   - the device: question, number, pain, claim, story or countdown
   - the first visual
   - the time until the first promise
2. **Structure.**
   - Divide the video into sections with timestamps: hook, context, stages/list items, sponsor, results, takeaway, CTA, sign-off.
   - Record the length of each section.
3. **Retention devices:**
   - open loops ("stick around", "but here's the thing", "the surprising part")
   - callbacks
   - questions per minute
   - how often "you" vs "I" is used
4. **Humour:** the time of each joke, its type (metaphor, self-deprecation, absurd image, reaction), and how often jokes come.
5. **Evidence:** numbers, studies and citations: how often, and how they are shown.
6. **Honesty beats** (what did not work), the CTA wording, and how the sponsor is brought in.

## 3. Visual layer (30 fps, frame by frame)
1. **Shot and scene segmentation.**
   - Find every scene change.
   - Measure scene length (median and range) and the number of distinct layouts.
2. **Transitions between scenes.**
   - Type: cut, dissolve, blur, whip-pan, zoom-through, iris, push, colour-fill or match-cut.
   - Duration in frames.
   - Whether it lands on a word.
3. **Element motion (inside a scene).** For every element that enters or exits:
   - type: slide, pop/scale, fade, draw-on, grow, count-up or swap
   - direction
   - duration in frames
   - easing: the share of the distance done in the first third, and any overshoot
   - stagger between elements
4. **Camera.**
   - drift (push-in or pan speed, % per second)
   - punch-in zooms (size, frames)
   - shake
   - parallax between layers
5. **Colour.**
   - background colour per scene (hex) and the palette per video
   - accent colours and what they mean
   - every **colour change**: background swap, dim (depth, ramp frames), flash, glow (where, how long), red/green highlight (blink pattern, frames on/off), vignette, spotlight
6. **Light and focus:** blur/defocus (to separate layers or as a transition), glow halos, rays, shadows.
7. **Typography.**
   - font family (closest free match), weight, italic, case, colour, outline/shadow
   - size as a % of frame height, position
   - entry animation, time on screen
   - words per text, text events per minute, whether there are burned-in captions
8. **Characters.**
   - number per frame
   - framing (extreme close-up, close-up, waist, full, tiny-in-world)
   - facing
   - pose library size (distinct drawings)
   - how often drawings are reused
   - rep-loop tempo and number of frames per loop
   - motion blur or ghost trails
9. **Worlds and graphics.** Catalogue the backdrops, props, metaphors, infographics (chart types and how they build) and UI mock-ups, each with a frame time.
10. **Particles and overlays:** type, count, motion, lifetime.
11. **Pacing.**
    - big changes per minute
    - longest still stretch
    - % of time with motion
    - pacing per section: the hook vs the middle vs the end

## 4. Sync
- **Visual vs words.** For each visual event, find the time to the nearest word onset, and to the *keyword* it illustrates. Do visuals lead, land on, or follow the word?
- **SFX vs visuals.** Measure how far each SFX is from its visual event, in frames.

## 5. Verify by eye
- For every event class the detectors report, look at 30 fps strips of at least 2 examples from different videos.
- Confirm or correct the classification, and write down what it really looks like.
- Look at the 36-frame overview sheet of every video.

## 6. Output
1. **Per-video scorecard:** a table with all the numbers above.
2. **Cross-video patterns:** medians and ranges, and what all or most videos do, compared with what only the top performers do.
3. **Effects spec:** for each effect, the measured parameters (frames, easing, sizes, colours), so we can implement it 1:1 in `director.py`.
4. **Gap list vs our current long video:** the same measurements run on `final/long01.mp4`.
5. **Plan:** engine changes, asset library, script rules and pipeline, ordered by impact.
