# Reference style rulebook (engineering targets)

Every rule says where its number comes from:
- **[M]** = measured in this audit on the 38 stills or 20 overview sheets (`analysis/measure.py`).
- **UNVERIFIED** = taken from the skill author's earlier reports. Not checked by us; the videos aren't in this environment.

## Picture targets (gate a shot if it falls outside)
| Rule | Target | Source |
|---|---|---|
| Mean luminance (caption band masked; measured on the 38 skill stills only) | 0.30-0.50 (median 0.37) | [M] |
| Darkest 2 % | ≤ 0.10 | [M] |
| Dark mass (luma < 0.12) | 0.03-0.15 of the frame | [M] |
| Mean saturation | 0.42-0.55 | [M] |
| Strong-edge density | 0.08-0.13 | [M] |
| Fine detail energy | ≥ 0.015 | [M] |
| Sharpness (Laplacian variance at 540x960) | ≥ 0.007 | [M] |
| World ink lines | near-black, about 3 px at 1080, on silhouettes and creases | UNVERIFIED outlines.md |
| Shade colour | violet-blue, never brown/grey; shade/lit about 0.5 by day | UNVERIFIED lighting.md |
| Key light | side-back (az 40-70°) by day; backlit at sunset; night-blue for explanations | UNVERIFIED |
| Heads | pale, brightness about 0.93-0.97 in every light; no blush, no catchlights | UNVERIFIED characters.md |
| DOF | on about 1/3 of screen time (CU/MS/inserts), off on wides | UNVERIFIED depth.md |
| Foreground framing prop | in about 38 % of MS/CU | UNVERIFIED depth.md |
| Shot mix | CU 3 %, MS 27 %, FS 28 %, WS 12 %, EWS 8 %, inserts 22 % | UNVERIFIED depth.md |
| Camera height | about 0.8x character height, eye level 82 % | UNVERIFIED depth.md |

## Editing and motion targets
| Rule | Target | Source |
|---|---|---|
| Hard cuts | 0-1 per video in 12 of 20 | UNVERIFIED STYLE_BIBLE |
| Place changes | 4-frame white flash, or a 6-8 frame dissolve, or continuous camera travel / follow an object | UNVERIFIED |
| New picture rate | 86-95 % of consecutive overview tiles differ | [M] computed on the 20 sheets. The tile spacing (~1 s) is an ASSUMPTION; video lengths are unknown. |
| Holds | always creep (push-in about 0.15-0.35 %/frame); no static hold of 12 frames or more | UNVERIFIED motion.md |
| Impacts | flip-sign shake decaying over 7 frames, on the word | UNVERIFIED |
| Character action | lands 0-3 frames before its word | UNVERIFIED |

## Typography
| Rule | Target | Source |
|---|---|---|
| Captions | **Conflicting evidence.** All 38 stills in the skill's `references/frames/` show one burned-in caption word (files and words listed in `EVIDENCE_INTEGRITY_AUDIT.md`). The user reports a separate set of 88 reference frames with no captions. That set isn't in this environment. **Decision: no captions** (the user didn't ask for them). | [M] for the 38-frame set only |

## Audio
| Rule | Target | Source |
|---|---|---|
| Narration | 3.5-4.1 words/s, under 1 s of total pauses, starts on frame 1-4, ends on the last word | UNVERIFIED |
| Loudness | -14 LUFS integrated | UNVERIFIED |
| Music bed | 5-10 dB under speech in the reference. **Our user wants it lower: we keep it about 25 dB under.** | UNVERIFIED |
