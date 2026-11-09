# posture04 (v4) — detailed review: "template feel", repeated wobble, double character, + more

New tool: `.claude/skills/reference-video-analysis/scripts/transitions.py` tracks the foreground against the flat
background and classifies every transition (flip / rise / slide / scale / fade / cut), then reports variety, repeats and rhythm.
It was run on green.faction's top-10 reels and on v4. 30 fps strips: `review_tilt_cmp.jpg`.

## Key numbers
| | Reference top 10 | Ours v4 |
|---|---|---|
| Transition mix | fade 26%, scale/pop 26%, cut 23%, rise 21%, **flip 4%** | flip 36%, fade 29%, cut 21%, scale 7%, rise 7% |
| Flips per video | **0–2** (an accent) | 5 detected / 12 pose changes use the flip |
| Dominant transition | **different in every reel** (cut, rise, fade, fade, fade, scale, scale, rise, cut, rise) | flip |
| Transitions per minute | 18–28 | 17 |
| Shortest gap between transitions | 0.2–0.4 s (quick bursts) | 1.2 s (no bursts) |
| Gap variation (CV) | 0.33–0.87 | 0.44 |
| Still frames | 64% | 81% |
| Fast "burst" frames | **17.9%** | **8.7%** |
| Character after entering | **holds completely still** | rocks back and forth on emphasis words |

## A. The owner's points, confirmed
1. **Template feel.** Every pose change uses the same card flip with the same 10-frame timing, and every exercise
   has the identical structure (green number + title → highlight → anatomy badge → arrow). In the reference the flip is
   rare (4% of transitions), and each reel has its own dominant style, so the reels don't look alike in bulk.
2. **Same character twice at the start.** v4 shows the hook pose, then cuts to a zoomed copy of the *same* pose
   (1.9 s), and the same happens at the wall test (14 s). The reference never re-zooms the same pose. It keeps the pose and adds
   overlays, or brings in a second panel/character.
3. **Repeated wobble looks like a glitch.** Our tilt is a back-and-forth oscillation with the same shape on 6 words.
   At 30 fps the reference character *never* wobbles: it enters (flip, rise, pop), settles, and holds. The rotation the
   motion tool measured in the reference was panels sliding, not the character.

## B. More problems found
4. **Too few real moves.** Burst frames are 8.7% vs 17.9%. The reference feels alive because of frequent, fast, varied moves,
   not because of constant small motion.
5. **Flat rhythm.** No quick bursts (min gap 1.2 s). The reference alternates clusters of 0.2–0.6 s changes with 4–6 s holds.
6. **Fixed durations everywhere.** Flip always 10 frames, tilt always 24, pops always 8, labels always the same timing. Identical
   timing is what the eye reads as a template. Reference transition lengths vary a lot (CV 0.6–0.9).
7. **Endless periodic loops.** Highlight pulse, badge float, and arrow bob all repeat on fixed cycles, which looks mechanical.
   Reference overlays animate in once and then hold.
8. **One composition.** One centred character in 14 of 17 beats. The reference keeps changing layout: split panels, two
   characters, rising panel bars, a big number rising, full-screen cards, close vs wide.
9. **Identical exercise layout ×4.** Same label position/style for all 4 exercises. The reference varies (big "1" rising from
   the bottom with typed "Exercise", labels on the body, none at all).
10. **Entrances only from below.** No slide from the side, no drop from the top, no scale-from-a-point, no panel push.
11. **Single background tone.** The reference also uses lighter panel tones and two-tone splits that change with the content.
12. **Same whoosh on every entrance.** The same sample at the same volume makes the sound repetitive too.
13. Still open: logo watermark; audio loudness range 0.7 LU vs about 2.2.

## C. Anti-template system (proposal for v5 and every future video)
- **Per-video style seed:** each video draws its own transition palette (2 main + 2 accent types with weights, e.g.
  this video = pop + rise, accent slide + flip), its own easing set and its own tempo. Bulk videos get different signatures.
- **Rules:** flip ≤ 2 per video; never the same transition twice in a row; durations drawn from a range (5–14 frames);
  **no idle wobble**: the character settles and holds; emphasis comes from events (sticker pop, colour beat, a new
  pose, a quick zoom *with* a new overlay), never from rocking the same image.
- **Meaning-driven motion:** problem → pop/scale; comparison → split panels; list → rising number; reveal → flip (rare);
  time/scale → full-screen card.
- **Composition quota:** at least 4 layouts per video (close-up, wide, split, two-character, full card, panel bars).
- **Rhythm:** mix bursts (0.3–0.6 s) with holds (3–6 s).
- **Overlays animate once, then hold.** No looping pulses or bobbing.
- **Varied SFX:** several whoosh/pop samples, randomised pitch and volume.
- **Automatic template check before delivery:** run `transitions.py` on the render. It fails if the top transition is over 50%,
  back-to-back repeats are over 35%, flips are over 2, or transition lengths have CV under 0.4; it also compares this video's signature with previous videos.
