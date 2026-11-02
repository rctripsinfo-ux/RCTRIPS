# System failure analysis: why the pipeline produced the gaps

## 1. Analysis problems
| Failure | Effect | Evidence |
|---|---|---|
| Reference videos weren't in the repo. The skill docs point to `vids/` and `measure/`, which were never shipped. | No frame-level motion or timing truth for the reference. Camera and editing rules were copied from text. | audit §1 |
| Two prior reports contradict each other: "holds 80 %, cuts almost never" vs "moving 65 %, big reframes are cuts". | We followed the bridge recipe (cuts on reframes) and ended up with 29 hard changes. | gap G5 |
| Our QA compared only against our own earlier frames ("is it better?"), never measured against the reference. | Brightness 0.63 vs 0.37 went unnoticed for 4 versions. | gap G1 |
| The skill author's personal rule "no captions" was treated as a style rule. | Captions, which appear on every reference frame, were missing. | gap G4 |

## 2. Asset problems
| Failure | Effect |
|---|---|
| No model library (kenney.nl blocked). Everything is built from boxes, cylinders and lathe shapes. | Low detail density (edge density about 0.55x the reference). Cars, truck and dozer look like toys. |
| The sand is one texture tile over a 500 m plane. | Large flat areas, low fine detail. |
| The set lacks dressing near the camera. | The frame's foreground is empty. |

## 3. Animation problems
| Failure | Effect |
|---|---|
| Characters only blink and change expression. No idle sway, gestures or weight shifts. | They look static and pasted on. |
| One "event" per shot, while the reference changes the picture about every second. | New-picture rate 0.68 vs 0.93. |
| Voice pauses (8.6 s in total) were kept when the voice was swapped. | Dead air and low energy. |

## 4. Rendering problems
| Failure | Effect |
|---|---|
| No GPU, so SwiftShader runs at about 4.3 s/frame at 1080p. Each full render costs 2.4 h. | Few iteration rounds, so fixes got verified on stills only. |
| Lens blur used on many shots. | Lower sharpness. |
| The `@react-three/postprocessing` composer renders blank under SwiftShader. Fixed with a hand-built composer. | Fixed. |

## 5. Composition problems
| Failure | Effect |
|---|---|
| The open-beach setting gives large uniform sand and sky areas. | Bright, low detail, weak focal hierarchy. |
| Cuts are used to reframe instead of motivated camera travel. | Choppy rhythm. |

## 6. Style-translation problems
| Failure | Effect |
|---|---|
| The reference stories mostly play in interiors or night streets with practical lights. Ours is a sunny beach. The style was copied, but the mood wasn't adapted. | Wrong brightness and contrast regime. |
| Midday light chosen for "readability" | Flat. Late afternoon keeps readability and adds depth (verified in the test segment). |

## 7. QA / verification problems
| Failure | Fix (now in place) |
|---|---|
| No numeric gate. | `analysis/measure.py` reports 10 picture metrics plus pacing against the reference distribution. |
| Captions and their timing weren't checked. | Word timings are generated with the voice (`voice/words.json`). Accuracy is an estimate; this still needs an aligner. |
| No side-by-side review with reference stills. | `SIDE_BY_SIDE_DIFFERENCE_REPORT.md` and the sheet in `analysis/sbs_test.jpg`. |
