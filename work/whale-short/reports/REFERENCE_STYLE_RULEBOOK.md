# Reference style rulebook (engineering targets)

Every rule says where its number comes from:
- **[M]** = measured in this audit on the 38 stills or 20 overview sheets (`analysis/measure.py`).
- **[P]** = from the skill author's earlier reports on the full videos. Not re-verifiable here, because the videos
  aren't in the repo.

## Picture targets (gate a shot if it falls outside)
| Rule | Target | Source |
|---|---|---|
| Mean luminance (caption band masked) | 0.30-0.50 (median 0.37) | [M] |
| Darkest 2 % | ≤ 0.10 | [M] |
| Dark mass (luma < 0.12) | 0.03-0.15 of the frame | [M] |
| Mean saturation | 0.42-0.55 | [M] |
| Strong-edge density | 0.08-0.13 | [M] |
| Fine detail energy | ≥ 0.015 | [M] |
| Sharpness (Laplacian variance at 540x960) | ≥ 0.007 | [M] |
| World ink lines | near-black, about 3 px at 1080, on silhouettes and creases | [P] outlines.md |
| Shade colour | violet-blue, never brown/grey; shade/lit about 0.5 by day | [P] lighting.md |
| Key light | side-back (az 40-70°) by day; backlit at sunset; night-blue for explanations | [P] |
| Heads | pale, brightness about 0.93-0.97 in every light; no blush, no catchlights | [P] characters.md |
| DOF | on about 1/3 of screen time (CU/MS/inserts), off on wides | [P] depth.md |
| Foreground framing prop | in about 38 % of MS/CU | [P] depth.md |
| Shot mix | CU 3 %, MS 27 %, FS 28 %, WS 12 %, EWS 8 %, inserts 22 % | [P] depth.md |
| Camera height | about 0.8x character height, eye level 82 % | [P] depth.md |

## Editing and motion targets
| Rule | Target | Source |
|---|---|---|
| Hard cuts | 0-1 per video in 12 of 20 | [P] STYLE_BIBLE |
| Place changes | 4-frame white flash, or a 6-8 frame dissolve, or continuous camera travel / follow an object | [P] |
| New picture rate | 86-95 % of 1-second samples show a different picture | [M] |
| Holds | always creep (push-in about 0.15-0.35 %/frame); no static hold of 12 frames or more | [P] motion.md |
| Impacts | flip-sign shake decaying over 7 frames, on the word | [P] |
| Character action | lands 0-3 frames before its word | [P] |

## Typography
| Rule | Target | Source |
|---|---|---|
| Captions | one word at a time (sometimes 2-3), white heavy sans with a thin black outline, centred, 60-74 % of the height, hard swap on each word | [M] visible in 38/38 stills |

## Audio
| Rule | Target | Source |
|---|---|---|
| Narration | 3.5-4.1 words/s, under 1 s of total pauses, starts on frame 1-4, ends on the last word | [P] |
| Loudness | -14 LUFS integrated | [P] |
| Music bed | 5-10 dB under speech in the reference. **Our user wants it lower: we keep it about 25 dB under.** | [P] |
