# Captain Workout style guide (from a Google AI Studio analysis of 6 Shorts, 26 Oct 2026)

AI Studio timings are approximate and some details may be guessed. Check against real frames before copying exact numbers.
The 65 s (creatine) and 151 s (Hero Project) videos are outliers. The ones to copy are 19–39 s.

## Script formula (Shorts, 20–35 s, 155–175 words per minute)
| Time | Part | Example |
|---|---|---|
| 0–3 s | Provocative hook: what the viewer does is wrong / is hurting them | "Your arms look small? It's not your biceps, it's your forearms." |
| 3–5 s | Pivot bumper: same words + same slam sound every video (brand stamp, resets attention) | Theirs: "LET ME FIX THAT". Ours must be our own, e.g. "HERE'S THE FIX". |
| 5–20 s | Why: one simple chain or one funny analogy ("uncooked spaghetti arms") | "X causes Y, Y causes Z." |
| 20–30 s | Fix: 1–2 moves or option A / option B, dead simple | "#1 Rice bucket. #2 Dead hangs." |
| last 3 s | Payoff + CTA: comment question, or "subscribe" on the shirt | "What's your level? Comment below." |

No greetings, no filler. Every sentence earns its place.

## Visuals
- **Frame 1:** the character + the problem shown at once (e.g. forearms circled in red dashes).
- **Every noun gets a picture.** Spoken word → icon or effect at that exact moment (rice → bucket drops in, "small" → red X on the biceps).
- **Something changes every 1.2–2.4 s:** a new icon, a pose, a punch zoom (100% → 115% → 100%), or a label.
- **Background:** flat slate grey/blue gradient (#9AA6B2 → #B0BAC3), no clutter.
- **Character:** dark, low-colour, so red (#EF4444), green (#22C55E) and yellow accents pop.
- **Props and outfits** change per video: shaker, sunglasses, suit, a "SUBSCRIBE" t-shirt.
- **Muscle highlight:** a red dashed circle or a glow on the muscle. No anatomy diagrams.
- **Labels:** short "#1 The rice bucket" style labels at the top. Captions are separate, at the bottom.
- **Captions:** bold sans, white with a soft shadow, lower third, and the spoken word turns yellow (#FACC15).
- **Transitions:** cuts almost always, one fade at the end.

## Audio
- **Voice:** male, late 20s–30s, confident, playful, close-mic, compressed, no echo.
- **Music:** low trap/phonk beat, 120–130 BPM, well under the voice.
- **Sound effects:**
  - whoosh on every pop-up
  - a heavy slam on the bumper
  - a ding on a good tip
  - a buzzer on a myth

  Owner rule (Oct): no meme sounds, so skip the record scratch and guitar screech, and keep the buzzer rare.

## Formats worth copying
1. **Myth / problem fix** (forearms 39 s, stress 31 s, plastic 35 s): hook → bumper → why → fix → CTA.
2. **Level / tier list** (back levels, 19 s): one slow horizontal pan across 6 bodies (BEGINNER → ELITE), a tier label on top, and one spoken line: "What's your back level? Comment below." It is cheap to make, loops, and gets lots of comments.

## What this means for H (Effortless Exercise)
- **Keep:** the hook-in-frame-1, a fixed bumper (ours), a picture per noun, a change every ~2 s, top labels with bottom captions, cuts, and a short 20–35 s length.
- **Try:** the slate grey background instead of white (tan H on grey gives red/green better contrast). Test it in one video first.
- **New H images the owner should generate** (white background, same H):
  - H with the problem area circled
  - H with sunglasses and a thumbs up
  - H in a "SUBSCRIBE" t-shirt
  - H hanging from the bar, front view
  - H with a shaker
  - 6 back views from beginner to elite (for the tier format)
  - a few props: rice bucket, shaker, a red X, a green tick

## Measured from the owner's analysis files (26 Oct; these beat the AI Studio guesses above)
| Video | Length | Words/min | Hard cuts | Something moves every | Bumper at |
|---|---|---|---|---|---|
| Forearms | 39 s | 157 | 6 | 0.36 s | 12 s |
| Plastic / testosterone | 37 s | 145 | 0 | 0.50 s | 5 s |
| Stress / testosterone | 32 s | 138 | 5 | 1.0 s | 5 s |
| Creatine | 66 s | 165 | 1 | 0.54 s | 4 s |
| Back level | 20 s | 15 words only | 0 | one slow pan | none |

- **Few hard cuts (0–6 per video).** Pace comes from constant small motion (pop-ins, zoom punches, prop moves), not from cutting. This matches the owner's "smooth, few transitions" rule.
- **Background:** light grey-blue (brightness 146–174, not white 240). The character is dark grey with a white "W" mask.
- **Captions:** small white text in the lower middle, under the character. There are no big top labels in these videos. Our top headings are our own choice.
- **Bumper position:** "Let me fix that" comes right after the hook, at 4–5 s. In the forearms video it comes at 12 s, after a longer roast.
- **Back level:** 15 spoken words in the first 5 s, then 15 s of music while the camera pans the 6 levels. The labels at the top do all the work.
- **Ending:** a close-up punch-in on the face, or the "SUBSCRIBE" t-shirt.

## APPROVED TEMPLATE (owner, 27 Oct): `build_posture2.py` → `final/posture2.mp4`
Copy that file for every new video. Rules it follows:
- **Length and voice:** 25–30 s, about 70 words, voice speed 1.05, -16 LUFS. Music volume 0.025, sfx volume 0.35.
- **Hook (0–3 s):**
  - The first heading is shown in full from frame 1 (no typing).
  - 2–3 pose swaps.
  - A spinning dashed red pain circle on the problem area.
  - A camera punch on the key word.
- **Bumper:** "HERE'S THE FIX" on a dark card, with a loud typing sound and a punch-in. No captions during the bumper.
- **Exercise scenes:** clips from `work/clips/library/` (77 clips), on a WHITE scene background. Speed them up (rate 1.3–1.5), with no camera zoom.
- **Image scenes:**
  - Sand beige (#E2D3B9) with a spotlight.
  - H width 0.8.
  - A slow push-in from 1.0 to 1.07.
- **Anatomy circles** (`work/anatomy/images`, 60 images): only 1–2 per video.
- **Headings and captions:**
  - Headings at the top are typed. Captions are small and white, at the bottom.
  - Keywords in yellow.
  - Small subs under the heading.
  - Rep counter.
- **CTA:** "COMMENT <WORD>" heading, a pop-up comment bubble with a notification sound, and a punch-in on the face.
- **Never use:** colored box labels, small icons on the character, green ticks or glows, red X on top of a circle, or meme sounds.
- **Tool changes** (pain circle, bubble connector line, `sfx_typing_loud`, library snapshots) are in `work/tool-patches/`. Copy them back into `~/reel-engine-tool` in a fresh session.

## Owner rules, 28 Oct (override the voice speed above)
- **Voice:** 1.2x. `fast_render.py` cuts dead air but keeps short natural breaths (≤0.22 s at sentence ends, ≤0.1 s at commas). It holds longer only where `<plan>.pauses.json` says, e.g. 0.7 s after "fix." so the bumper and its 0.9 s typing sound finish before the next scene.
- **Flow:** systematic, not rushed.
  - Every picture or heading stays on screen at least ~1.5 s, one idea per beat.
  - At most 2 pictures per section (problem → cause → test → fix cards → result → CTA).
  - No rapid pose swaps.
- **Format:** "Day 2 V3" (`build_belly3.py`) is the reference.
- **Anatomy circles never on H's face** (owner, 28 Oct).
  - Place them in the lower half, beside the legs or hips (e.g. x 0.77, y 0.62–0.68), never next to the head.
  - The tool also pushes a circle off a known face box (`tool-patches/layers.jsx`, `Video.jsx`), but always check the frame.
- **Clip scenes** (owner, 29 Oct): no text on H's head or body.
  - No camera zoom on clips. Clip at y 0.62.
  - Captions move up to y 0.27 with `captions.high` (tool patch).
  - The key number as one red line at y 0.36. No small subs.
- **Typed cards:** exact style D from `make_cards.py`, with no pop per letter (no shaking).
- **Voice:** 1.3x with short holds (`belly6.pauses.json`), about 28 s.
- **Captions** (owner, 29 Oct): old-viral style, `captions.look = "viral"` (tool patch).
  - One word at a time, bold italic white with a thick dark outline, keywords yellow.
  - Mid-screen at y 0.56. During clips it goes to y 0.41 (`captions.high`) so it sits above H's head.
