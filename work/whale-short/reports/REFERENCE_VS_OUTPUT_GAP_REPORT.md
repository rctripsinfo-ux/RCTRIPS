# Reference vs output: gap report (v4)

**Scope note:** reference = the 38 stills + 20 sheets in the skill folder. The user's 88-frame set was not available; if it differs, every reference column must be re-measured on it.

Method: `analysis/measure.py` runs the same metrics on the 38 reference stills (540x960) and on 38 frames sampled
evenly from our v4 (scaled to 540x960). The caption band (58-78 % of the height) is masked in both. Pacing uses the 20
reference overview sheets (60 tiles ~1 s apart per video) vs 60 tiles 1.1 s apart across our 66 s. Raw numbers:
`analysis/v4_metrics.json`. Values are p25 / **median** / p75.

## 1. Measured numbers
| Metric | What it means | Reference | Ours v4 | Gap |
|---|---|---|---|---|
| lum_mean | average brightness | 0.27 / **0.37** / 0.59 | 0.52 / **0.63** / 0.69 | ours **+70 % brighter**, washed |
| p2 | darkest 2 % (deep darks) | **0.085** | **0.140** | ours lacks deep darks |
| dark_frac (luma < 0.12) | ink + deep shadow area | **0.075** | **0.018** | ours **4x less** dark mass |
| sat | mean saturation | **0.47** | **0.39** | ours −17 % |
| edge_frac | strong edges per pixel | **0.099** | **0.054** | ours **~0.55x** (sparse scenes) |
| detail_hf | fine texture energy | **0.017** | **0.011** | ours ~0.65x |
| sharp_lapvar | sharpness | **0.009** | **0.005** | ours ~0.55x |
| lum_std | contrast | **0.204** | **0.187** | close |
| colorful (Hasler) | colour spread | 0.27 | 0.30 | close (ours uses big flat hues) |
| new_picture_frac | 1-s samples showing a NEW picture | **0.93** | **0.68** | ours holds the same picture 3x more often |
| hard changes per video | cuts / flash cuts | UNVERIFIED: 0-1 in 12/20 (prior report, contradicted by motion.md) | **29** (16 cut keys + 13 hard shot changes) | ours is cut-driven |
| captions | burned-in words | 38/38 skill stills; user's 88 frames: none (not available here) | none | **not a gap: user decision, no captions** |
| speech pauses | silence inside narration | UNVERIFIED: < 1 s total (prior report) | **8.6 s** | ours has dead air |

## 2. Gaps (category, problem, where, why it hurts, root cause, fix, priority, confidence)

| # | Cat. | Problem | Where | Why it weakens | Root cause | Fix | Prio | Conf. |
|---|---|---|---|---|---|---|---|---|
| G1 | Light/colour | Picture too bright and flat (lum 0.63 vs 0.37), no deep darks | every beach day shot | reads "cheap/pastel", no mood | midday sun on a pale sand plane filling 50-70 % of the frame; shade lifted to 0.42 | late-afternoon key from side-back, violet shade, richer sand albedo; night/interior beats | P1 | high |
| G2 | Light/colour | Saturation 0.39 vs 0.47 | day shots | less "premium" | pale sand + white heads dominate | sat 1.12, warmer key, saturated props | P1 | high |
| G3 | Detail | Edge density 0.55x, texture 0.65x | open beach, aerial, parking lot | empty, unfinished frames | few props near the lens; plain sand texture; procedural primitives | dense set dressing (grass, footprints, shells, kelp, props per shot), stronger sand texture | P1 | high |
| G4 | Typography | ~~No captions~~ **WITHDRAWN.** The 38 skill stills show captions, but the user's 88 reference frames reportedly don't, and the user didn't ask for captions. | — | — | — | captions disabled by default (`inputProps.captions` must be `true` to show them) | — | — |
| G5 | Editing | 29 hard changes vs ~0-1 | whole video | choppy; reference feels like one continuous camera | camera plan built from cuts (copied bridge recipe) | continuous travel between subjects, follow-the-object moves, 4-frame flashes, 6-8 f dissolves for place changes | P1 | medium (prior report) |
| G6 | Pacing | 8.6 s of silence; picture changes less often (0.68 vs 0.93) | gaps between lines, long holds 3-5 s | low energy | voice v1 gaps kept by the slot fit; few events per shot | re-time voice to < 1 s total pauses; add an event every ~1 s (gesture, prop, effect, camera beat) | P1 | medium |
| G7 | Sharpness | lap-var 0.55x | everywhere | soft look | DOF on many shots, lens blur with large cInf, h264 at 55 MB | DOF only on CU/MS beats (~1/3), lower cInf on wides, encode crf 15 | P2 | medium |
| G8 | Characters | Static standing poses, little idle life | MS shots | "pasted on" | no idle motion beyond blinks | head sway, weight shift, gestures on key words | P2 | high |
| G9 | Assets | Primitive cars/truck/dozer; chunks read as rocks in places | lot, burial | breaks realism | no model library (Kenney blocked) | higher-detail procedural models, or a user-supplied CC0 pack | P2 | high |
| G10 | Integration | Faces fine now; feet contact OK; golden shadows hard | crowd shots | minor | card shadows on | keep blobs by day, soft shadows golden | P3 | medium |
| G11 | Explanation readability | Night whale reads as a dark shape | physics shot | the "up" idea is the core of the story | night shade on a dark whale | lamp/rim light on the whale, brighter belly, diagram arrows larger | P2 | high |
| G12 | Audio | Music now ~25 dB under voice (user wish) vs reference 5-10 dB | mix | intentional deviation | user request | keep; revisit only if the user asks | — | — |
