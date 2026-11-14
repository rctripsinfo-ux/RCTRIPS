# Competitor forensics, round 1 (14 Nov 2026): inventory, limits, first measured findings

Source: owner's Drive folder (12 MP4 files) + owner's word-level SRTs for the 6 Shorts (TurboScribe).
Raw videos, 10 fps frames (2,624 for the Shorts), transcripts and per-video measurements are kept OUT of the repo
(copyright; internal research only). This file holds only our measurements and conclusions.

## 1. Inventory (what was received)
| ID | Title (file name) | Format | Length | Video | Processed |
|---|---|---|---|---|---|
| c01 | Why Your Arms Still Look Small | Short | 62.5 s | 720x1280 30fps | frames 10/s, cuts, motion, loudness, SRT words, music bed |
| c02 | What's Your Body Fat Percentage? | Short | 27.1 s | 720x1280 60fps | frames, cuts, motion, loudness, SRT |
| c03 | Why your abs workout hurts your back | Short | 37.1 s | 720x1280 60fps | frames, cuts, motion, loudness, SRT, music bed |
| c04 | How Many Ab Exercises Do You Really Need? | Short | 34.1 s | 720x1280 60fps | frames, cuts, motion, loudness, SRT, music bed |
| c05 | How to Get an Aesthetic Physique | Short | 45.9 s | 720x1280 60fps | frames, cuts, motion, loudness, SRT, music bed |
| c06 | Biceps Workout for Huge Arms (Do THIS!) | Short | 56.1 s | 720x1280 60fps | frames, cuts, motion, loudness, SRT, music bed |
| c07 | Why Training Your Neck Changes Everything | Long | 8:01 | 1280x720 | inventoried only |
| c08 | Calisthenics vs Gym: Which Is More Effective? | Long | 10:25 | 1280x720 | inventoried only |
| c09 | Want a Sharper Jawline? Start Here | Long | 8:21 | 1280x720 | inventoried only |
| c10 | Want BIGGER forearms? DO THESE | Long | 8:30 | 1280x720 | inventoried only |
| c11 | The #1 Method To Lose Belly Fat (NO CARDIO) | Long | 9:46 | 1280x720 | inventoried only |
| c12 | I Took Creatine For 365 Days... | Long | 8:20 | 1280x720 | inventoried only |

Missing: channel URL, views, likes, publish dates (no channel link given; YouTube Data API is blocked here, the
YouTube website is reachable). So nothing below says which video performed best.

## 2. Measured: competitor Shorts vs our Day 4-6 (same method for both)
| Measure | Competitor (c01-c06) | Ours (Day 4-6 mix) |
|---|---|---|
| Hard cuts per video (scene-change detector) | 0-6 | 19-26 |
| Big whole-frame jumps (0.1 s steps) | 0-52 | 109-185 |
| Mean frame change per 0.1 s | 1.4-8.3 | 11.6-17.8 |
| Share of 0.1 s steps with motion | 30-69 % (100 % on the slow-pan c02) | 84-89 % |
| Longest calm hold | 1.7-3.9 s | 1.0-1.2 s |
| Narration speed | 132-170 words/min | 230-238 words/min |
| Pauses of 0.35 s or more | 5-15 per Short (1.7 s after the hook joke) | 0 (every gap cut to 0.05 s) |
| Loudness | -17.5 to -20.5 LUFS, LRA 3-4.5 | -13 LUFS, LRA 1.6-2.4 |
| Voice above music bed (between words) | 11-14 dB (c04: 6 dB) | about 34-36 dB (music almost inaudible) |

## 3. What the frames show (checked on 1 fps sheets and 0.1 s strips)
1. **One stage, not slides.** Flat grey-blue background for the whole Short. c03 keeps the SAME hanging pose and set for
   0-22 s; things are added and removed on top of it. c01 uses 3 sets in 62 s.
2. **Layers enter and leave on their own.** c01 2.3-2.9 s: the character leaves left in ~0.2 s, the stage is EMPTY for
   ~0.4 s (a beat on "but your arms"), the new pose slides in from the right in ~0.2 s. c01 34.6-35.0 s: a second
   "commentator" copy of the character rises from the bottom-right corner, small to big in ~0.3 s, arms crossed,
   over the exercise picture, which stays. c03 9.1-9.7 s: a judging copy fades in on the left while the main one
   swaps pose in place (legs up) with wobble lines.
3. **Scale is the camera.** Full body -> chest close-up -> full body by scaling the cut-out on the same stage
   (c01 8-13 s). No new image is needed for a close-up.
4. **Motion drawn into the picture.** Ghost / onion-skin copies of the moving limb (curl, dip, extension, leg raise),
   dashed motion arcs, shiver lines. One image shows the whole rep.
5. **Words as set dressing.** Big low-contrast grey words typed BEHIND the character ("0 GAINS / BACK PAIN /
   CHIROPRACTOR", giant grey "1 2 3" behind the exercise). Captions are small, white, low; they never compete.
6. **Props and gags recur.** The shaker cup the character sips (c01 at 3 s and 13-16 s), equipment appearing one by
   one (dumbbells, rope, cable: c01 24-27 s), fire rising from the floor on "that burn?" (c03 12-14 s), anatomy
   labels popping one at a time (c01 17-20 s), X-ray inset circle (c03 19-22 s).
7. **Endings.** c01 ends on a recap collage of all three exercises + the thinking close-up. c03 ends "LEVEL UP".
   c02 is 6 s of voice + 21 s of music while the camera pans a body-fat lineup (comment bait).

## 4. What the transcripts show (SRT word timings)
- First word at 0.00 s in every Short. Hook = an insult with a funny picture: "coat hangers", "breadsticks",
  "like a dying bug", "ends with you crying in a plank". Then the brand bumper "Let me fix that" (c01, c05, c06).
- The joke gets room: 1.7 s of silence after "coat hangers?" (c01) and after "breadsticks?" (c06).
- Personification and slang carry the humour: "this shady little muscle called the psoas", "flailing mess",
  "sleeve-busting size". Numbers structure the body: "Number one / two / three".

## 5. Why ours feels like a slideshow (root causes, in order of impact)
1. A new full-frame picture every ~1.5-2 s, each with its own background -> 4-5x more cuts and whole-frame jumps.
2. No persistent character on a persistent stage; reactions are new pictures instead of a pose swap in place.
3. The voice is rushed (silence cutting + 1.2x = 230+ wpm) and has no comedy pauses, so nothing can "land".
4. Audio is loud and flat (-13 LUFS, tiny LRA) with an almost silent music bed; theirs is softer with an audible
   bed ~12 dB under the voice, which is what makes it sound smooth and relaxing.
5. Our scripts explain; theirs roast first, then fix, with one funny image per beat.

## 6. Next tasks (proposed order)
1. Channel URL -> public inventory of all Shorts (titles, views, dates) to rank what works.
2. Per-Short beat sheets for c01, c03, c06 (pose / layer / camera / SFX per beat, 0.1 s checked at each change).
3. Engine: stage + independent layers (enter/exit per layer, pose swap in place, scale-camera, corner cameo,
   onion-skin, typed background words, empty beat) in director.py.
4. Voice: stop cutting every pause; keep ~150-170 wpm with planned pauses; re-test the Gemini TTS model (the old
   gemini-2.5-flash model id now returns 404 for text; TTS needs a fresh test).
5. Mix: -14 to -16 LUFS, music bed ~12 dB under the voice with ducking, SFX under the voice.
6. One original demo Short, built on 2-3 stages with existing H poses, then review against c01/c03.

## 7. Public channel inventory (14 Nov 2026, yt-dlp flat list; full list in channel-inventory-2026-11-14.csv)
View counts are public totals on the collection date; publish dates were not in the flat list (order = newest first),
so older videos have had more time. Views are NOT retention.
- **Captain Workout** (610K subs): 43 Shorts, median 232K views (51K-4.2M); 54 long videos, median 145K (15K-4.6M).
  The 6 Drive Shorts are its #1-#5 and #8 most viewed Shorts. Top Shorts are older uploads (#20-#41 by age).
- Top Shorts are one concrete, visible body problem + "you're doing it wrong" hook (arms look small, abs workout hurts
  your back, too many ab exercises) or a self-rating comment bait (physique level, body-fat %, back level).
- Lowest Shorts are the newest and abstract/nutrition/hormone topics (creatine, testosterone x2, body recomp: 51-65K).
- **Effortless Exercise** (44 subs): 28 Shorts, median ~1,050 views (65-1,800). Older posts sit at ~1.1-1.8K; the
  newest Day-format posts are lower (squat 148, neck 318, biceps 386), but they are also the youngest.
- Our titles copy theirs closely ("Why your abs workout hurts your back" is the same title). Same topics with weaker
  execution compete head-on with a 610K channel; we need our own angle per topic.
