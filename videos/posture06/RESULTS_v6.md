# posture06 (v6): colours/fonts, nothing cut by the frame, readable script-paced motion

## Findings on v5 (measured)
- **Text contrast (WCAG):** red text scored 1.4–3.0 on every background (fails); green numbers were borderline (3.2–4.5).
- **Frame cuts:** 12 scenes had settled elements cut by the frame edge: 6 anatomy badges, "EVERY 15°" (wider than the frame),
  "GAP" (above the top), 2 arrows (right edge), and 3 characters (sides).
- **Pacing:** scene changes 0.32 s apart in the hook; entrances 6–9 frames with sharp "expo" easing (too fast to follow).

## Fixes in v6
- **Palette:** white + yellow (#FFD447) text with a dark outline on everything (contrast 4.3–11.7). Red is used only for graphics,
  plus the stamp, now white text on a solid red box. Numbers are yellow.
- **Frame safety (automatic):** every text/badge auto-fits the width and is clamped 30 px inside the frame; arrows are
  clamped inside; characters are fitted to the frame width; zoom punches are capped so no element leaves the frame.
  `audit.py` (in this folder) registers every drawn element per frame and lists anything cut for ≥ 0.2 s.
  **Result: 0 settled elements cut.** The only off-frame moments are entrances (≤ 0.3 s, sliding/dropping in by design).
- **Script-paced motion:** entrances 14–20 frames (~0.5–0.7 s), gentle easing only, scene changes ≥ 0.74 s apart and on
  script words ("body" → highlight, "small" → small pose, "lack muscle" → flex + stamp, new sentence → panel), slow
  zoom (16 frames, 4–8%) on key words that then holds.

## Checks
| Check | Result |
|---|---|
| Elements cut by the frame (settled) | 0 |
| Arrow touches character | 0 frames |
| Template check | PASS (top 50%, repeats 23%, 1 flip) |
| Hook fast-motion frames | 22% (ref 26%) |
| Text contrast | ≥ 4.3 everywhere |
| Loudness | -14.1 LUFS |

Note: slower, readable motion lowers the overall motion share (23% of frames vs 46% in the reference). That follows the
owner's request (movement must follow the script, not be too fast).
