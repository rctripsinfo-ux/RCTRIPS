# Plan: "Captain Workout" type videos with our H

Based on 5 reference shorts (Why Your Arms Still Look Small, Biceps Workout for Huge Arms, How to Get an Aesthetic
Physique, How Many Ab Exercises, Why Your Abs Workout Hurts Your Back). Analysed frame by frame (1 fps and 4 fps
sheets), cut timing, transcripts and audio loudness.

## 1. What the references do

### Format
| Item | Value |
|---|---|
| Length | 34–62 s (short ones 34–37 s, list videos 45–62 s) |
| Words | 75–150, fast confident voice (~2.6 words/s) |
| Background | one flat blue-grey colour, `#BCC8D1`, the whole video. No rays, no gradients |
| Character | one stylised muscular figure, always full body or a big close-up, on the flat background |
| Picture changes | every 1–2 s (pose change, zoom, inset, label, arrow) |
| Music | none or almost none (0.6 s gaps are near silence). Voice + light sound effects only |
| Loudness | -16 to -20 LUFS |

### Script formula (all 5 follow it)
1. **Hook insult/pain (1 sentence, 3–4 s):** "You're curling every session, but your arms still look like coat hangers."
   Always a funny comparison: coat hangers, breadsticks, dying bug, new chiropractor.
2. **"Let me fix that."** (or "Here's what's actually happening." / "Want to fix it?") on an empty screen with typed text.
3. **The truth in 1–2 sentences:** "Biceps don't make your arms look huge. Triceps do."
4. **The promise with a number:** "Here are three moves that get it done."
5. **Three numbered items**, each: name ("First, overhead extensions.") + why (1 line) + 2–3 short form cues
   ("Elbows tucked, chest up.") + one alternative ("No machine? Bench dips.").
6. **Short close:** "These three exercises will give you maximum gains." / "No fluff, just gains."
   No "send this to a friend" ending.

### Visual grammar (what appears on screen)
| Element | How it looks | When |
|---|---|---|
| Hook entrance | figure slams in with motion blur, shake lines around him | first frame |
| Movement | still drawing + a faded "ghost" copy of the other position (dumbbells down/up), small zoom pulses | every exercise |
| Section line | "LET ME FIX THAT" typed letter by letter with a cursor, grey condensed font, empty screen | after the hook |
| Big number | huge faded grey "1" / "2" / "3" behind the figure, sometimes the topic written vertically beside it ("THE GOLDEN RATIO", "ARM SIZE") | start of each item |
| Muscle highlight | the worked muscle painted red (problem) or green (target) on the figure | when the muscle is named |
| Anatomy | clean medical diagram (bones + muscle heads) with white tag labels ("long head", "lateral head") | the "truth" part |
| Inset bubble | round circle with a zoomed diagram or a mini exercise next to the figure | explaining a muscle |
| Arrows | thin dotted curved arrow showing the movement path | form cues |
| Measure | dashed line across shoulders / waist with "×1.6", "×0.5" | numbers |
| Gauge | vertical body-fat meter (10% / 20% / 30%) filling yellow → green | body fat |
| Props | small emoji-style food (pizza, chicken), fire, crossed arms "STOP" pose | jokes |
| Recurring gag | the character sipping from a red cup, unbothered | after the hook insult |
| Captions | small white bold words (2–3 at a time) with a thin dark outline, at about 78% of the height, over the legs | whole video |
| Ending | figure flexing, light grey rays behind him | last 2 s |

### Sound
Whoosh on each new picture, small pops on labels and numbers, a light "ding" on the fix, nothing loud, no meme voices.

## 2. Our version: same structure and feel, our own character

We copy the **format** (script formula, pacing, layout, flat background, small captions, numbered items, anatomy
insets), **not** their character, logo or drawings. Their masked figure with the "W" is their brand: using it would be
copying their channel. We use **H** (our muscular character) everywhere.

| Reference | Ours |
|---|---|
| Grey masked "W" figure | H (our existing 190 poses + new ones below) |
| Blue-grey `#BCC8D1` | our own flat colour, e.g. light warm grey `#D9DEE3` or keep blue-grey (your choice) |
| Red cup gag | H sipping his protein shaker (`hero_drinking_shake`, already in the library) |
| "LET ME FIX THAT" | same typed line, our font |
| No music | no music or music at -30 dB under the voice |

### Template timeline (40 s video)
| Time | Part | Visual |
|---|---|---|
| 0–3.5 s | Hook insult | H slams in (motion blur + shake lines) doing the wrong thing; red muscle |
| 3.5–5 s | Signature gag | H sipping the shaker, unbothered |
| 5–6.5 s | "Let me fix that." | typed grey text, empty screen |
| 6.5–12 s | Truth | H flex close-up, red then green muscle, anatomy inset with labels, "1/3 → 2/3" |
| 12–14 s | "Here are three moves" | H showing 3 fingers |
| 14–36 s | Item 1, 2, 3 (~7 s each) | big grey number behind H → exercise (clip or 2 poses with ghost) → dotted arrow + green muscle on the cue → alternative in an inset bubble |
| 36–40 s | Close | the three moves side by side, then H double-biceps on light rays |

## 3. Tool changes I will make (no assets needed)

| Feature | Status in our tool | Work |
|---|---|---|
| Flat coloured background | canvas background exists | set it per plan |
| Small white outlined captions at 78% | captions exist, other look | add a caption look `"look": "clean"` (white, thin dark outline, 3 words) |
| Typed section line with cursor | `typewriter` text exists | add the cursor + grey condensed style |
| Big faded number behind H + vertical label | giant text exists | add opacity + vertical label option |
| Ghost copy of the other position | not there | new `ghost` layer: second pose at 35% opacity |
| Slam entrance with blur + shake lines | `whip` entrance + shake exist | new `slam` entrance (blur + shake lines) |
| Red / green muscle | `glow` exists | add a solid "paint" style that colours only the muscle |
| Tag labels, inset bubble, dotted arc, measure ×1.6, gauge | `callout`, `zoomBubble`, `path`, `measure`, `progress` exist | restyle to the thin clean reference look |
| Clips on a coloured background | clips use multiply: H's skin would tint blue | make clips with a transparent background, or keep clip scenes white |
| No music, -14 LUFS final | done in the last video | keep |

## 4. Assets I need from you

### Must have (for the reference look)
1. **Anatomy diagrams** (transparent PNG, clean medical-illustration style, no text on them, I add the labels):
   biceps (long + short head), triceps (long, lateral, medial head), brachialis, shoulders (front/side/rear delt),
   lats/back V-shape, abs (six-pack + obliques), hip flexors / psoas. 7 images.
2. **H close-ups** (same H, plain background): side-view arm flex (upper body only), front upper-body flex,
   H at the bottom corner thinking (head + shoulders, looking up), H with arms crossed in an X ("STOP").
3. **Body types of H**: fat H (big belly), average soft H (skinny-fat). Skinny H already exists (`hero_beginner`).

### Per topic (only if we do gym videos like the references)
Our library is home / bodyweight. The references use gym machines (cables, dip machine, preacher bench, hanging bar,
incline bench). For each gym exercise I need either a clip (I write the clip prompt, 12 credits each) or 2 poses
(start + end). For the first video (arms) that is: overhead triceps extension, dumbbell lying triceps extension,
dip machine (or bench dips: we already have `clip_chair_dip`).

### Optional
- A better voice: our Kokoro voice is fine but calmer than theirs. If you have ElevenLabs, send a voice you like.
- Your choice of background colour.

## 5. First video (sample in this format)

Topic #1 from the list, rewritten in the reference formula (home version, works with today's library):

> You're curling every single day, but your arms still look like two dry noodles. Let me fix that. Your biceps are
> only one third of your arm. The other two thirds? Triceps. Hit them, and your sleeves start fighting for their
> life. Here are three moves. First, diamond push-ups. Hands close, elbows tight to your ribs, chest to your thumbs.
> Second, chair dips. Hands behind you, elbows straight back, lower until your arms make ninety degrees. Third,
> pike push-ups. Hips high, head down between your hands, press back up. Three sets of ten, three times a week.
> No more noodles. Just arms.

All three moves already have animation clips (`clip_diamond_pushup`, `clip_chair_dip`, `clip_pike_pushup`).

## 6. Questions for you
1. Home exercises (our channel, works today) or gym exercises like the references (needs new assets)?
2. Does this replace the storytelling style from the last sample, or do we keep both?
3. Captions: small white ones like the references (recommended), or none?
4. Ending: their short "No fluff, just gains" close, or keep our "Send this to the friend who …"?
