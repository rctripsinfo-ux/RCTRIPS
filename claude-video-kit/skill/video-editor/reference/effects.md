# Effects library (51 face-aware effects)

Engine: `SKILL_DIR/effects` (MIT, see NOTICE.md). Effects track the face and can sit behind the head.

## Setup (once)
`bash SKILL_DIR/effects/scripts/setup.sh` → prints `READY` (creates `effects/.venv`). Python = `effects/.venv/bin/python` (Windows: `effects\.venv\Scripts\python.exe`).
Linux only: if `libEGL.so.1` missing → `sudo apt-get install -y libegl1 libgles2 libgl1`.
A `TypeError ... NoneType ... ImageSegmenter.__del__` at the very end is harmless.

## Pipeline order
cut.mp4 → **effects pass** (`fx.py`, keeps audio, outputs 1080×1920) → loudnorm → Remotion overlay (captions, hook, progress bar, whooshes). Set `zooms: []` in data.json when effects already move the camera. Add `hideCaptions: [[s,e],…]` for effects that use the chest/bottom area (`tape-label`, `messages`, `checklist`, `liquid-glass-graph` under chin, `apple-toggles pos=below`). Add a whoosh SFX at every effect start.

## Commands
- Plan file `work/<project>/fx_plan.json`: `{"effects":[{"fx":"<name>","start":s,"end":e, ...options}]}` (times = cut-video seconds).
- Check stills (do this first): `PY SKILL_DIR/effects/scripts/fx.py --plan fx_plan.json cut.mp4 work/<project>/check.png --still t1,t2,...` (middle of each effect). LOOK at them: face covered? text cut off? unreadable?
- Render: `PY SKILL_DIR/effects/scripts/fx.py --plan fx_plan.json cut.mp4 work/<project>/fx.mp4`

## How to choose (talking-head reels)
- 6–12 effects per minute, 1.5–4 s each, on the punchiest lines. Never two text-heavy effects back to back.
- Match meaning: brand/name → `backdrop-word`; "no/never/fake" → `reject-stamp`; "not X, but Y" → `huge-strike` X then `apple-toggles` Y; price/claim → `tape-label`; "smart move"/key line → `lean-in`; what people say/DMs → `messages`; list of 3 → `todo` (ticks on each spoken item); #1/winner → `glitter-spotlight`; conclusion → `slow-push`; final message → `led-sign`; numbers growing → `liquid-glass-graph` (real numbers only); steps → `checklist`; CTA end → `comment-box` / `tap`.
- Use only real numbers the user gave. Never invent stats.

## Effect names
noise, lineup, locked-on, orbit, lean-in, backdrop-word, spotlight (look=sparkle → glitter-spotlight), the-bill, moody, swipe, todo, comment-box, tap, pause-point, uninstall, reel-frame, shortcut-rain, reject-stamp, countdown-flip, rabbit-hole, cover-star (look=editorial), scribble, glass-widgets, red-collage, split-headline, pastel-word, check-pills, timeline, headline-box, profile-wall, tier-list, broll-split, phone-fan, dot-reveal, headline-wall, checklist, liquid-glass-graph (look=bento), carousel-spin, match-cut, apple-toggles, led-sign, slow-push, over-the-shoulder-zoom, messages, place-in-grid, tape-label, select-resize, wave-trim, huge-strike, crayon-write, fan-build.
Options per effect: see the `@effect(...)` functions in `effects/scripts/fx.py` (common: `text` with `|` between lines, `color` hex, `x`/`y` 0–1).

## Gotchas found in testing
- `todo` `ticks` = **video seconds**; `apple-toggles` `ticks` = **seconds from the effect's start** (e.g. `0.3|0.8`).
- `messages` default sits over the face — use `"y": 0.93` (stack grows upward from the bottom).
- `huge-strike` word mostly hides behind the head; use a short word (≤7 letters).
- Effects needing `images` (orbit, noise, phone-fan, profile-wall, place-in-grid, fan-build, carousel-spin) need a folder of the user's reel covers — ask for it or skip those.
- Speed reference: 86 s reel with 11 effects ≈ 5 min on a 4-core CPU without GPU; faster on M-series Macs.
