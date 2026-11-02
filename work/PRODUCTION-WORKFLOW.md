# PRODUCTION WORKFLOW (owner, 1 Nov 2026), overrides older format rules where they clash

Owner's master prompt, short form. Every new video follows it.

1. **Inputs from owner:** script, one scene prompt and one image per sentence or phrase, in order. Never skip, reorder or add unrelated visuals. Check each image against its line before editing.
2. **Voice first:** owner voice (Gemini Fenrir or owner's file). Get word times. The voice sets the timeline: every cut lands on its phrase.
3. **Basic cut first:** all images in order, synced, no blank frames, 9:16. Effects come after.
4. **Transitions:** connected entry and exit (push: the old image leaves while the new one enters, overlapping, so there are NO empty frames). Mix them: slide, pendulum, push, zoom, wipe, parallax. Never one pattern for the whole video.
5. **First 5 s:** strongest visual, action at once, fast timed changes, strong expression, kinetic type, sound in sync. Clear problem or question, not chaos.
6. **Exercise animation:** pose-to-pose loops from real pose images (start/end). No warping of flat images. Motion only where it teaches.
7. **Backgrounds:** white-background images stay on pure WHITE, H big, room for captions. Full-environment images go FULL SCREEN (crop or pan to 9:16, no stretching, no small card).
8. **Captions:** one word at a time, big bold italic, BLACK with RED keywords. Centre for talk scenes, lower safe area for exercises. Never on the face, the moving body parts, headings, labels or props. Position set per scene.
9. **Intro cards:** a ~2 s white card ("01 — CHIN TUCKS", black + red) when a new exercise or step starts, only where it helps.
10. **Unique direction:** review the last video first (hook, transitions, animation, captions, rhythm, weak points), then plan a fresh approach that keeps what worked.
11. **Sound:** whooshes on directional moves, impact on warnings, pops on kinetic type, music under the voice, fades. Every SFX has a purpose; no repeated pattern.
12. **QA before delivery:** script complete, mapping right, sync, hook, smooth transitions, zero blank frames, readable captions with no overlaps, intro cards, levels, safe framing. 1080x1920, 30 fps, H.264 MP4.
13. **Order:** script → assets → voice → timestamps → basic timeline → concept → transitions → animation → hook → cards → captions → caption positions → audio → render → review → fix → final render.

## Review of the last video (Day 4 remake, 1 Nov): what to fix next
- 13 one-frame empty frames at the side-push cuts: the old image exits before the new one enters. Needs overlapping push.
- Every scene uses the same fly-left/fly-right: repetitive.
- Captions are small white words over H's body: must become one-word bold italic black/red, placed per scene.
- Beige background: white images must go on white; full scenes were shown as small cards and must go full screen.
- Only one exercise had a pose loop. No intro cards for #1/#2/#3.
- Keep: frame-1 close-up with smash zoom, red slam heading, kinetic HERE'S THE FIX, -13 LUFS, owner voice.

## Owner rules added 1 Nov (after Day 5/6)
- WHITE background always. Build each video as a MIX: H library poses animated by swapping real poses on the words
  (rep loops, reaction changes) wherever poses can show it, and the owner's scene images only where poses can't.
  The owner's images are material, not the whole video.
- Highlights must change with the meaning: red pain circle, spotlight, red label tag, red arrow, white ring (no single
  green circle every time, no ring sound). Captions: one word, white, middle, dodge the highlight.
- Audio: voice loudest, SFX clearly lower, music lowest (director.py measures every stem).
- Never cut H's head/feet with zooms (zoom <= ~1.18, focus not above the middle). Day 4 exercise cards.
- Template: d06_plan.py (director.py). Library landmark points are unreliable for marks: give x/y by hand and check a still.
