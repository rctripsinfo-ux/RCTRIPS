# Style v2 plan: "Simple, smooth, H first" (15 Nov 2026)

Owner feedback on Pilot 1:
- Too many elements and too much text; the captions are too big and bold.
- The character looks like a side pose, while the elements look big.
- The competitor's videos are smooth and simple, with the character in focus.

Owner answers (15 Nov):
- Mostly close-ups.
- Keep only **Mini-H** and **Mirror Check**.
- Small captions like the competitor's.
- Generate new images with Codex (works now: test image below).

## 1. What the competitor actually does (re-measured, 36 videos, 3,134 frames at 2 frames/s)
| Measure | Competitor | Our Pilot 1 |
|---|---|---|
| Separate objects on screen | median **2**; **75%** of frames have ≤2 | 68%; stickies, headers, meters and mirror on top |
| Main subject height | median **60%** of the screen; 34% of frames ≥70% (big / close-up) | bbox similar, but the main object is often the mirror or a prop, not H |
| Close-ups that fill the frame | 7.2% of frames | 0.8% |
| Captions | ~2.6% of screen height (small), lowercase white, thin dark outline, no box | ~4% + coloured swipe boxes |
| On-screen words besides captions | rare (one grey word or number) | headers, sticky notes, meter labels on almost every page |
| Motion | 64% of frames still; changes are eased slides / swaps; no shake | page turns, scribbles, slaps every 2–3 s |

**Conclusion:** the competitor wins on *focus*. One character, one idea per shot, quiet screen, small captions. We copy that discipline, not their look.

## 2. Style v2 rules (every video)
1. **H is the frame.** Shot mix:
   - **50%** close-ups (chest-up / face)
   - **30%** waist-up
   - **20%** full body, only for showing an exercise
   - H stays centred or slightly off-centre. Never a "side pose next to a prop".
2. **Max 2 things on screen:** H + one supporting thing (Mini-H, the mirror, or one prop). No stickies, meters, headers or labels.
3. **Background:** flat Ice `#E6F2F3`. No grid, no texture, no vignette. It is the same colour across a video; one darker tone `#CFE3E5` is allowed for a "moment" shot.
4. **Captions:** small, about 2.8% of the screen height.
   - lowercase white, thin dark outline
   - bottom at ~78%, 2–3 words per line
   - no boxes, no colour swipe
   - Mini-H lines are the same size in light purple `#B9A8FF`.
5. **Smooth motion only:**
   - Slow camera drift (1.00→1.05 over a shot).
   - A gentle "breathing" scale on H (±1%), so long holds never look frozen.
   - Eased 0.4 s slides and clean cuts on sentence ends; soft 0.3 s dissolves between related shots.
   - At most 1–2 punch-ins per video. No shake, no smears, no page turns, no scribbles.
6. **Mini-H** (Codex-generated chibi H, purple shirt) pops in small from a bottom corner, says one line, then leaves. 3–5 lines per video.
7. **Mirror Check** only in topics about how you look (back, belly, posture, arms). It is a full illustrated scene: H in front of a mirror, the reflection changes.
8. **No muscle paint by default.** A close-up image of the muscle (generated) does the job. A soft glow is allowed only if a topic really needs it.
9. **Audio stays:** deep calm H voice, Mini-H second voice, music 11 dB under, −20 LUFS. Sparse soft SFX only on Mini-H entries.

## 3. Images: Codex (ChatGPT Plus), one consistent character
- **Test passed:** new close-up pose from the library H as reference (`research/codex-test-pose.jpg`). Same face, H mark, belt and wristbands. About 1 minute per image.
- **Per video:** ~10–14 illustrated shots (close-ups, reactions, the exercise, Mirror scene), all on a flat `#E6F2F3` background, vertical 9:16.
- **Fixed prompt block in every prompt:**
  - same character as the reference
  - same comic style
  - background flat hex `#E6F2F3`
  - no text
  - the framing of the shot (close-up / waist-up / full)
- **Reusable library to build once:** 12 H reaction close-ups (smirk, shocked, thinking, explaining with a hand, pointing at the viewer, laughing, facepalm, proud, tired, whisper, side-eye, thumbs up) + 6 Mini-H poses. After that, each video only needs its topic-specific shots (~5–6).

## 4. Pilot 2: proposal
Topic: **Day 1, "The Laziest Way to Build Muscle"**, from the 30-day plan. It's the strongest brand fit and is publishable if approved.

| # | Line (speaker) | Shot (Codex image) | Framing |
|---|---|---|---|
| 1 | H: You don't need two hours in the gym. | H collapsed on the gym floor beside dumbbells, exhausted (the "old way") | full → slow push-in |
| 2 | H: You need forty minutes, three times a week. | H smirking, holding up 3 fingers | close-up |
| 3 | M: That's it? I was promised suffering. | Mini-H disappointed, bottom corner over shot 2 | 2 objects |
| 4 | H: Rule one. Full body, three days a week… | H doing a goblet squat | full body |
| 5 | H: Rule two. Fewer sets, but hard ones… | H's strained face on the last rep of a curl | face close-up |
| 6 | M: So… quit early? | Mini-H squinting | corner |
| 7 | H: Quit smart. Rule three. Add one rep… every week. | H sliding a small plate onto a bar, calm smile | waist-up |
| 8 | H: Forty minutes. Three days. One more rep each week. | H relaxed on a couch after training, thumbs up | waist-up |
| 9 | M: Okay, which day are you starting? | Mini-H pointing down at the comments | corner over shot 8 |

Steps:
1. Build the base library + 6 topic shots with Codex.
2. Re-skin the engine to style v2: flat set, small captions, breathing, drift, dissolves.
3. Generate both voices.
4. Render, run the frame check, send it.

## 5. Decisions needed
1. Pilot 2 topic: **Day 1** (recommended), or the fridge/back topic again so it can be compared with Pilot 1?
2. Background: flat Ice `#E6F2F3` (recommended), or plain white?
