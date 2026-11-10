# posture05 (v5): variation engine + high-energy hook

## What changed vs v4 (posture04/REVIEW_v4.md)
- **Hook (0–5 s):** 4 different moves: slide-in moving from frame 0, "this small" pop, flexing drop + "NOT MUSCLE" stamp slam,
  panel wipe. Plus zoom punches on key words, a traps highlight pop and word-by-word captions.
  Hook fast-motion frames: **23%** (reference 26%; v4 ≈ 9%).
- **Variation engine (`STYLE_SEED`):** each video draws its own palette (2 high-motion main transitions + 2 accents).
  Rules: never the same transition twice in a row, at most 2 flips, durations 9–16 frames, easing drawn per beat.
  Seed 5 (this video) = drop + panel / pop + cut. Seed 11 = rise + panel; seed 23 = rise + pop (same script, different look).
- **No idle wobble:** the character settles and holds. Emphasis = zoom punch that holds (no oscillation).
- **No same pose twice in a row** (enforced by an assert), no looping pulses/bobs.
- **4 different exercise label layouts** (round badge, sliding pill, top-centre, huge rising number + typed title).
- **SFX variety:** sound per transition type (drop → boing, panel → whistle, pop → pop), random pitch ±20% and volume.
- Overlays (captions, stamps, labels) are drawn after the zoom, so they're never cropped.

## Checks
| Check | Result |
|---|---|
| Template check (top type ≤ 50%, back-to-back ≤ 35%, flips ≤ 2) | **PASS** (33%, 29%, 1) |
| Transition types detected | 6 (cut, fade, pop, rise, scale, flip) |
| Arrow touches character | 0 frames |
| Hook burst frames | 23% (ref 26%) |
| Rest burst frames | 10% (ref 16%) |
| Frames with motion | 36.5% (ref 46%) |
| Loudness | -14.1 LUFS |

## Still open
- Body sections are calmer than the reference (10% vs 16% burst frames). More mid-beat events would close this.
- Logo watermark (needs your file); audio loudness range 0.6 LU vs about 2.2.
