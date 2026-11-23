---
name: "effortless-exercise-thumbnail-prompts"
description: "Write image-generation prompts for Effortless Exercise YouTube thumbnails (Shorts 9:16 or long-form 16:9) from a video title, topic or script, using the H-forehead character. Use whenever the user sends a title, topic, script or batch of scripts and wants thumbnails or thumbnail prompts, asks to redo failed thumbnails, or sends back a generated thumbnail to review."
---

# Effortless Exercise thumbnail prompts

Use this whenever the user sends a video title, topic or script (one or many) for the Effortless Exercise fitness / calisthenics channel and wants thumbnail prompts. The user feeds the prompts plus the character reference image to an AI image tool (Google Flow or an agent). Your job is to write prompts that produce consistent, on-brand, instantly clear thumbnails.

Always reply in English, even if the user writes in Hindi or Hinglish.

## OWNER UPDATE (15 Nov 2026): new thumbnail style, overrides "Brand style" and "Text" below

The owner rejected the white-background + black/red label-box thumbnails ("bahut bekaar"). Study of 35 top outlier thumbnails (Yellow Dude, Captain Workout, Bro Pump, 5-Minute Fitness, Calisthenic Crafted, The Core Man, BlueGym, Built For Aesthetic):

- NO label box, NO rectangle behind the text, NO black-and-red title box.
- 0 to 3 words, integrated into the image: either big white heavy italic with a thin dark outline and a soft shadow, or short handwritten black words with a hand-drawn arrow.
- Flat saturated background: sky blue, teal, purple, lavender, or a vertical split of two colours for contrasts. A soft lighter circle or radial glow behind the character is allowed.
- One strong visual idea:
  - exposed red anatomical muscle (anatomy-chart fibres) on the target muscle
  - a magnifier circle inset of the muscle
  - a split before/after or wrong/right (e.g. "2 HOURS" vs "40 MIN")
  - Mini-H (chibi H, purple shirt) reacting in shock
  - levels 1-2-3
  - a funny emotion
- Generate with Codex (CLAUDE.md). Approved examples, Day 1: `work/thumbs/day01v2/PROMPTS.md`.
- Keep words and subject inside the central ~70% of the height. Same character rules as below.

**BRAND COLOURS, LOCKED (owner, 15 Nov 2026). The layout is NOT locked.**
- Every thumbnail uses only these for the background and graphic shapes: dark muted red `#7A1A1A` and fresh teal `#0F8B85`, plus white words.
- Words: extra-bold condensed italic, white, thin dark outline, soft shadow, no box.
- The layout changes per video, for example:
  - split halves
  - full teal with a dark-red band or circle
  - full dark red with a teal glow or a teal magnifier ring
  - a radial burst
- Examples: `work/thumbs/brand/PROMPTS.md` and `work/thumbs/split/PROMPTS.md`. Do not make every thumbnail a split.

## Format decision

- Short script or the user says Shorts or 9:16: 1080x1920, 9:16 vertical.
- Long-form or the user says 16:9: 1280x720, 16:9 horizontal.
- If unclear, Shorts (9:16) is the default.

## Output format

- Always give the FULL detailed prompt. Never give a short version.
- Before each prompt, give two short lines only:
  - **Thumbnail text:** the two lines, and why they name the topic.
  - **Concept:** one or two sentences describing the visual idea.
- Then the prompt in one code block.
- Batches: ALL prompts of a batch go in ONE code block (owner's choice, 16 Oct; see the builder script below). If some images fail, the owner sends back the ones that worked: match them to the videos and give ONE new box with only the missing prompts.
- First line of the box: "CREATE ALL IMAGES FOR THESE N THUMBNAILS. Make each one as a SEPARATE image (N images total). Treat every prompt below as a completely separate, independent image request. Attach the same character reference image to every single one. Follow each prompt exactly as written." Then each prompt under a header "THUMBNAIL X OF N: name" so the owner can name the files for the covers ("<number>-<name>.jpg").
- CRITICAL: every prompt must be fully STANDALONE. Repeat the size, character block, crop-safe block, background, text block with the font line, style and avoid list inside EVERY prompt. Never put shared rules once at the top and refer to them. Agents run each prompt separately, and shared rules get lost, which causes thin or changed fonts and character drift.

## The character (never changes)

Every prompt opens with:

"Use the attached character image as the main character and build this thumbnail from it. Keep his face, head shape, skin tone, body proportions and outfit 100% identical to the reference. Do not redesign or restyle him. Same art style as the reference."

Then state how many times he appears ("Only ONE character appears" / "The same character appears twice").

Character details line: "bald muscular man, warm tan skin, white letter \"H\" on his forehead, olive military utility belt with pouches and a silver buckle, black shorts with olive harness straps, black wrist wraps, olive combat sneakers."

Only change the outfit or body when the concept needs it, and say so explicitly (e.g. "OUTFIT FOR THIS IMAGE: plain black fitted t-shirt", "NO wrist wraps so forearms are visible", "IMPORTANT BODY CHANGE: skinny-fat body"). Keep the face and the H unchanged.

## Brand style (never changes)

- Background: plain pure white. No colored backgrounds, gradients or scenery. Only a thin faint grey floor line and soft grey shadows where needed.
- Art style: clean semi-realistic comic illustration, bold black outlines, smooth shading, highly detailed and anatomically accurate muscles, strong soft top lighting, crisp shadows, high contrast so it reads instantly on a small phone screen.
- Color meaning: bold RED glow/overlay = problem or wrong way. Bright glowing GREEN with clear muscle fiber lines and a soft green glow = target muscle or right way. A red X over an object = don't do this.

## Text (the thumbnail is a second title)

- The text must state the video topic plainly so any viewer understands it in one second. Never hide the topic behind a vague or clever hook. If the user looks at it and can't tell the topic, it has failed.
- Use simple words. Avoid technical or uncommon terms: say "side abs" not obliques, "muscle pain" not soreness, "upper back" not traps, "side rib muscle" not serratus, "hidden muscle" or the exercise name, not brachialis.
- Two lines in a white rectangular label box with a thick black border, centered at the top of the safe area. Line 1 in solid black (usually the problem, e.g. "SKINNY WRISTS?"), Line 2 in bold red (usually the fix or answer, e.g. "WATER BOTTLE FIX").
- Write the label lines as: "The label shows exactly two lines of text and nothing else. Top line: WORDS (written in solid black letters). Bottom line: WORDS (written in bold red letters). Write only these words; never write color names or quote marks in the label." (16 Oct: 'Line 1 in solid black: "X"' made the image tool print BLACK "X" RED "Y" in the label.)
- Include this font line in every prompt: "FONT: Anton (or Impact), extra-heavy condensed bold sans-serif, ALL CAPS, very thick strokes, the same font and weight for both lines. Large and readable, filling most of the safe width. Never thin, never regular weight, never a different font."
- Small panel tags (WRONG/RIGHT, EASY/HARD) use the same font: red tag with white text for bad, green tag with white text for good.
- No other text anywhere.

Examples that worked: "SKINNY WRISTS? / WATER BOTTLE FIX", "TRAIN YOUR / SIDE ABS", "THICK ARMS? / TRAIN TRICEPS", "BOX BODY? / GET A V-TAPER", "HOW MANY PUSH-UPS? / NOT 100", "CRUNCHES / WON'T BURN FAT", "DON'T STRETCH / BEFORE WORKOUT".
Examples that failed (too vague): "NOT SORE?", "SAME BELLY?", "SKINNY ARMS?", "SWEAT = FAT LOSS?".

## Crop-safe spacing

For 9:16 Shorts, include this block in every prompt (the top and bottom get cropped):

"CROP-SAFE SPACING (very important, follow strictly):
- Leave a large completely empty white margin at the TOP (about 18% of the image height) and at the BOTTOM (about 20% of the image height). Only plain white background there, nothing else.
- [List what must sit inside] must all sit inside the central 62% of the image height. Do NOT let anything run down to the bottom edge.
- Keep about 8% empty margin on the left and right.
- No element, text or body part touches or is cut off by any edge."

When the character is cropped (at belt, knees, chest), say where and that the crop line must sit above the bottom 20%. Characters running to the bottom edge is a common failure.

For 16:9: keep about 5% empty margin on all edges.

## Concept rules

- One idea per thumbnail, very few elements. The image alone should show the topic.
- Fresh concept every time. Do not copy past thumbnails or reuse the same layout across a batch. Rotate between: wrong vs right stacked panels, big character + tiny chibi version for contrast, single close-up of the target muscle glowing, top-down view with shapes drawn over the body, a simple prop that tells the story (water bottle, chair, crossed-out dumbbell, battery icon, stopwatch).
- Show the exact exercise from the script, accurately. Visuals must match the words (a table is a table, a chair is a chair).
- Prefer pure side view for floor exercises (push-ups, planks, dips, bridges); AI tools get poses right more reliably than 3/4 angles. Spell out the pose: both palms flat on the floor, arms straight, exactly two legs, both feet on toes.
- In stacked comparisons, keep the same camera angle and the same size in both panels so only the key thing changes.
- Never invent numbers or claims that are not in the script.

## Prompt structure (use this order every time)

1. IMAGE SIZE line
2. Character instruction + appearance count
3. Character details line (+ any outfit/body change)
4. CROP-SAFE SPACING block
5. CORE IDEA (one or two sentences: what the text says and what the image proves)
6. BACKGROUND
7. LAYOUT, numbered: 1. TEXT (with the two lines and the FONT line), then the scene, panels, props, each with pose, highlighted muscle, color overlay and expression
8. STYLE
9. AVOID: always include "thin or light font, a different font", content in the top/bottom margins, anything touching the edges, colored or dark background, gradients, scenery, extra text, numbers, arrows, circles, badges, icons, fire, sparks, extra characters, changing the character's face or design, realistic photo style, 3D render, spelling errors, extra limbs, extra fingers, watermarks, plus pose-specific mistakes (hands off the floor, more than two legs, wrong angle).

## Reviewing a generated image

When the user sends back a generated thumbnail, check honestly: is the topic clear in one second, is the pose correct (count limbs and feet), is the font heavy and consistent, are the top and bottom margins empty, is the character unchanged, does the visual match the script. Say plainly whether it is usable. If not, list the problems and give a complete corrected prompt.

If the character drifts across a batch, advise generating 2 to 3 at a time and always attaching the original character image, never an earlier generated thumbnail.

## Builder script (for batches)

`scripts/thumb_prompts.py` assembles the standalone prompts and the single batch box from a list of entries, so the fixed blocks (character, crop-safe, font, style, avoid) stay word-for-word identical across a batch. Read its docstring for the entry format, then call `build(V, out_path, heading, thumbs_path=...)`. `thumbs_path` receives only the thumbnail box. For failed images, call it again with only the missing entries. For one or two thumbnails, writing the prompts by hand following the structure above is fine.


## LONG-VIDEO THUMBNAILS: the Yellow Dude formula (owner, 18 Nov 2026: "exactly use the Yellow Dude formula")
Measured from 12 of their outlier thumbnails. The first attempts were rejected because they used saturated full red/teal backgrounds, shouty all-caps text and clutter.

**Formula**
- **One character, one idea, lots of empty space.**
  - Draw H in a clean FLAT comic style: bold outlines, 2-tone cel shading, less texture.
  - Say this in the prompt.
- **Background:** one plain muted colour (pale blue `#CCD8F0`, cream `#F5F0E6`, dark navy `#22304F`, or white), never busy.
- **The image tells the story**, through ONE exaggerated visual:
  - sweat puddle + shaking lines
  - glowing red anatomy muscles on the skin
  - a circle inset zooming into a joint
  - red glowing hands
  - before/after split
  - fist smashing
- **Text:** 1–4 words, or a small handwritten label with a dashed arrow ("30 days later", "real strength").
  - Dark navy rounded bold ("Just A PLANK?") on light backgrounds; white italic on dark ones.
  - The text never repeats the title.
- **Challenge videos:** add a dark red `#7A1A1A` circle badge "30 DAYS". The brand red/teal appear only as accents (badge, tag), not as full backgrounds.
- **Prompt runner:** `thumbs/brand/run2.sh` (no forced white background).
- **Reference set:** `work/thumbs/long01/yf_a`, `yf_b`, `yf_c`.


## SHORTS COVERS (owner, 18 Nov 2026, final)
- Keep the brand red/teal thumbnails as before (`thumbs/brand`, `thumbs/week1`), appended to the last frame. The Captain Workout cover formula was tried and DROPPED.
- **H is always EXACTLY the reference character:** semi-realistic detailed comic, never flat or 2D. Prompt line: "Do NOT make him flat or 2D or simplified."


## BACKGROUND RULE (owner, 19 Nov 2026, latest, overrides older background rules)
- **LONG-video thumbnails use the plain flat CREAM background `#F5F0E6`.** Nothing else goes in the background.
- **SHORTS covers keep the brand red/teal colour code** (owner, 19 Nov): dark red `#7A1A1A` + teal `#0F8B85` backgrounds with white extra-bold italic words. Add the safe zone below and an out-of-the-box visual idea.
- Brand dark red `#7A1A1A` and teal `#0F8B85` stay as accents only: badges, words, glows.
- Text is dark navy `#1E2A4A` extra-bold italic.
- Formula that worked (the push-up mistakes video): one surprising visual gag, a 2–3 word question, the exact H big and clear.
- Reference: `work/long06/thumb/sk_e.png` (BALLOON vs CABLE).


## SHORTS COVER SAFE ZONE (owner, 19 Nov 2026)
- **The feed crops the top and bottom of a 9:16 Shorts cover.** Never place text or faces in the top 20% or the bottom 20%.
- **Text sits in the middle band (about 25–45% of the height). The full character fits between 20% and 80%.**
  - Prompt: "Leave the top 20% and bottom 20% as plain empty cream background; all text and the character's head stay inside the middle 60%."
- (Out-of-the-box gag covers were tried on 20 Nov and REJECTED by the owner. Use the brand style below.)

## A/B results so far (YouTube Test & Compare, 20 Nov 2026, tests still running)
- Long 05 push-ups (160 views): "STUCK AT 20?" big 3D number on teal 37% > "NOT A PUSH-UP" close-up 33% > "BANANA PUSH-UP" cream 28%. One giant number + 2-3 word question wins.
- Long 06 skinny vs big (521 views): "BALLOON vs CABLE" cream side-by-side comparison + first-person story title "I Lost to a 60 kg Guy in 4 Seconds" 43% > "4 SECONDS?!" 30% > "ONE FINGER?!" 26%.
- So: (1) a simple visual comparison on plain cream, or one giant number with a short question; (2) first-person story titles ("I ...") beat explainer titles.

## SHORTS COVERS: ALWAYS THE ORIGINAL BRAND STYLE (owner, 20 Nov 2026, final)
Reference covers: `work/thumbs/brand/day0X.png` (e.g. day04 arm levels, day06 WHY IT HURTS, day07_t LOW TESTOSTERONE?).
- ONE flat background: brand dark red `#7A1A1A` OR teal `#0F8B85` (optionally a soft glow of the other colour behind H). No split diagonal, no scenes.
- H big in the frame (chest-up or full body), exact semi-realistic H, one simple pose that shows the topic.
- At most ONE simple supporting graphic: a circle inset zoom (e.g. tendon), a battery, a row of icons/numbers. No absurd gags.
- 1-3 huge white extra-bold italic words with a dark outline at the top (keep them below the top 10% so nothing is cut).
- If a brand cover already exists for that day, use it as is.

## SHORTS COVER: APPROVED FORMULA (owner, 23 Nov 2026, latest, overrides older Shorts rules)
Approved: `work/short10/thumb/cw_a.png` (push-up 10 vs 40). Captain-Workout split style in brand colours:
- Top half dark red `#7A1A1A`, bottom half teal `#0F8B85`, split by a TORN diagonal paper edge.
- Top = the bad/low version of H (collapsed, struggling), bottom = the good/high version (strong, confident). H big, cropped close.
- Only white label boxes with a thick black outline and a big black number/1-2 words ("10", "40"). No title.
- Must be understood in one second without reading. Everything inside the middle 60% of the height (Shorts safe zone).
- Rejected for Shorts: cream backgrounds, heart/metaphor gags the owner could not read at a glance, handwritten-notes covers.
