# Animation style spec (copied from the 5 reference shorts, frame by frame)

Measured at 8–12 frames per second with timestamps. Our version: H (skin) on a WHITE background, everything else the same.
"Tool" column: ✅ our tool already does it · 🟡 close, needs a small change · ❌ needs new tool work.

## 1. How the character ENTERS the frame

| # | Name | Exactly what happens | Duration | Used for | Tool |
|---|---|---|---|---|---|
| E1 | **Zoom-slam** | first frame the figure is ~2.5× too big and heavily motion-blurred (radial blur), it shrinks to normal size | 0.15–0.2 s (4–5 frames) | the hook (first frame), big reveals ("STOP") | 🟡 `enter: "zoom"` is 1.6× and slower |
| E2 | **Rise-in** | comes up from below (~15% of the height) while fading 0→100% and growing ~90→100%, soft ease-out, tiny settle | 0.3 s | a new pose after an empty screen ("here's the truth") | 🟡 `up` has no scale |
| E3 | **Whip-in from the side** | slides in from the right or left edge with horizontal motion blur, no bounce | 0.2 s | exercise figure arriving over the big number | ✅ `whip` (ours has a squash, theirs none) |
| E4 | **Plain cut** | just appears | 0 s | most pose changes inside one idea | ✅ `cut` |
| E5 | **Corner peek** | a small reaction figure (head + shoulders) slides up from the bottom-left/right corner, starts ~40% transparent | 0.3 s | jokes / "thinking" / pointing at the viewer | ❌ needs crop poses + layer |
| E6 | **Side-by-side** | a second figure slides in from the left next to the first (comparison: big vs skinny) | 0.3 s | "his biceps vs yours" | ✅ second image layer + `left` |
| E7 | **Diagram swing-in** | anatomy drawing slides up from bottom-left with a slight rotation (~8° → 0°) | 0.35 s | anatomy | ❌ rotation enter |
| E8 | **Prop fly-in** | each prop (dumbbells, rope, clip) flies in from the bottom with a small spin, one per spoken word, they pile up as a collage | 0.3 s each | "dumbbells, ropes, cables" | 🟡 image `up` + rotation |
| E9 | **Inset circle pop** | a round bubble (thin light border) grows from 0 to full with a small overshoot, a zoomed diagram or mini exercise inside | 0.25 s | explaining a muscle / a variation | 🟡 `zoomBubble` (only zooms the same pose) |

## 2. How the character MOVES while on screen

| # | Name | Exactly what happens | Tool |
|---|---|---|---|
| M1 | **Slow push-in** | every shot keeps slowly zooming in (~3–5% per second, linear) | ✅ `motion: zoomIn` |
| M2 | **Keyword punch zoom** | on the key word the camera pushes 1.0 → ~1.35 in 0.25 s and holds | ✅ `camera` |
| M3 | **Zoom-through to close-up** | camera rushes into the body (1 → 1.6 in ~0.12 s), then cuts to a close-up drawing (arm / chest) | 🟡 camera ✅, close-up drawings ❌ (assets) |
| M4 | **Effort shake** | wavy "vibration" squiggle lines around the whole body, redrawn every frame + 1–2 px jitter | ❌ |
| M5 | **Ghost position** | a 30–40% faded copy of the OTHER position of the move (dumbbells down while he holds them up) fades in 0.3 s after he appears and stays | ✅ image `opacity` (done in v1 hook) |
| M6 | **Dotted movement arrow** | thin dashed curved arrow beside the moving limb, drawn from start to end in ~0.4 s, arrowhead at the end | 🟡 `path` (ours is thick, with a running dot) |
| M7 | **Muscle paint** | the muscle is filled solid red (problem) or green (target), fades in 0.25 s; red → green is a 0.3 s cross-fade | 🟡 `glow` (ours is a soft glow with sparkles) |
| M8 | **Blink / eye change** | eyes squint or blink once on a sarcastic line | ❌ (needs eye-variant poses) |
| M9 | **Exit** | almost always a hard cut; sometimes the figure slides down out of frame (0.3 s) | ✅ `cut`, `exit: down` |

## 3. How TEXT appears

| # | Name | Exactly what happens | Tool |
|---|---|---|---|
| T1 | **Captions** | small, white, bold rounded sans (Poppins-like), lowercase as spoken, thin dark outline, 2–3 words, at ~78% of the height, words simply swap (no pop) | ❌ ours: dark italic |
| T2 | **Section line** | EMPTY screen, a thin cursor bar appears, then the line is typed **word by word** (not letter by letter) in sync with the voice, grey condensed bold uppercase (Anton-like), cursor stays ~0.5 s, hard cut. Typing sound only while words appear | 🟡 ours types letters at a fixed speed |
| T3 | **Big section number** | hard cut to an EMPTY screen with a giant solid grey "1" (~40% of the height) for ~1 s while the voice says the exercise name; then the figure whips in IN FRONT of it; optional thin vertical label beside it ("THE GOLDEN RATIO") | 🟡 number ✅, vertical label ❌ |
| T4 | **Stacked keywords** | giant grey condensed words appear behind the figure one by one, each on the word it is spoken, stacking downward ("0 GAINS" / "BACK PAIN" / "CHIROPRACTOR") | 🟡 several giant texts |
| T5 | **Repeating word** | a giant grey word repeated across the top behind the figure ("STOP STOP"), fades out | ✅ `marquee` (ours scrolls) |
| T6 | **Tag labels** | small white rectangles, thin black border, black lowercase text, thin leader line to the body part; fade + slide in 0.25 s, one per spoken term | 🟡 `callout` (ours is a coloured chip) |
| T7 | **Hand-drawn note** | "1/3", "2/3", "×1.6" in a handwritten font with a thin line, fades in | ❌ |
| T8 | **Check mark** | a green tick drawn next to a tag | 🟡 |
| T9 | **Gauge** | vertical body-fat meter (10/20/30%), the bar fills yellow → green | ❌ |

## 4. Rhythm and screen rules
- A change every **0.5–1.5 s** (new pose, zoom, label, prop). Nothing static for more than ~1.5 s.
- The figure is **big**: full body fills ~80% of the height, close-ups crop at the waist.
- **Empty screen moments are part of the style**: section line and section numbers sit on an empty background.
- Effects on the scene: fire flames growing behind the figure, tears, smoke puff, light grey rays only on the last shot.
- Colours: everything greyscale, only the muscle paint (red / green), fire and food props are coloured.

## 5. Sound (what each visual gets)
| Visual | Sound |
|---|---|
| Zoom-slam | low whoosh + hit |
| Whip-in / rise-in | short whoosh |
| Section line | soft key clicks only while words appear (word by word) |
| Big number | soft pop / hit |
| Tag label, inset, prop | soft pop or click |
| Muscle paint | none or a soft "ding" |
| Joke / fail | cartoon sound (slide whistle down, boing) |
| Music | quiet bed, 12–15 dB under the voice |

## 6. What it takes to copy it exactly

**Tool work (needed for an exact copy):** T1 captions look, T2 word-synced typing with cursor, E1 stronger zoom-slam,
E2 rise-in with scale, M4 shake lines, M6 thin dotted arrow, M7 solid muscle paint, T3 vertical label, T6 tag labels,
T7 handwritten notes, T9 gauge, E5 corner peek, E7 rotation entrance. About 1 day of tool work, then every video uses it.

**Assets (images of H):**
1. Close-ups: side arm flex (waist up), front chest/abs (waist up), back (waist up).
2. Corner-peek crops: H head + shoulders thinking, pointing at the viewer, laughing, shocked.
3. Eye variants of 3 main poses: squint / sarcastic look.
4. Anatomy drawings (no text): triceps, biceps, shoulders, abs, hip flexors, back.
5. Props: rope attachment, cable clip, bench, pull-up bar (flat illustration, transparent).
6. Fat H and skinny-fat H.
