# Reference source manifest (source of truth)

Rule: only sets marked **APPROVED** may define production targets for the whale project. Every other set is study
material. A claim about "the reference" must name an APPROVED file and frame.

Search done 2026-11-02 over: the whole filesystem (`find / -xdev`, images and videos), every branch in git history
(`origin/main`, `origin/claude/intelligent-euler-6jm4o0`, `origin/claude/gifted-babbage-nco1vf`), the uploads folder,
and a fresh clone of the skill's source repo (`mromidev/claude-animated-shorts`, commit e3b817b).

## Reference sets

| ID | Set | Path | Source | Contents | Purpose | Verification | Status for the whale project |
|---|---|---|---|---|---|---|---|
| R1 | Skill stills | `.claude/skills/cartoon-3d-short/references/frames/` | skill author (GitHub repo) | 38 JPEG 540x960, frames 60/180 of 20 shorts; all carry burned-in captions | stills of the approved 20 reference videos | inspected 38/38 | **APPROVED** (user, 2026-11-02: the 20 reference videos are the skill author's 20 shorts) |
| R2 | Skill overview sheets | `.claude/skills/cartoon-3d-short/references/sheets/` | skill author | 20 sheets, 60 tiles each, one whole video per sheet | overview of the approved 20 videos | inspected; docs describe them wrongly as 2 s strips | **APPROVED** (pacing / shot variety only; not frame-level motion) |
| R3 | Skill reports + style bible | `.claude/skills/cartoon-3d-short/references/reports/*.md`, `STYLE_BIBLE.md` | skill author's agents, measured on videos we don't have | numbers and recipes, partly about the bridge short | measurements of the approved videos | not re-verifiable; contradictions found | **APPROVED SOURCE, UNVERIFIED numbers**: use as hypotheses until re-measured on the videos |
| R4 | The 20 reference videos (= the approved reference) | named in the skill docs as `references/vids/*.mp4` | skill author | — | motion, cuts, timing, audio | **not found** (not in the upstream repo either) | MISSING |
| R5 | "88 reference frames" mentioned by the user | — | user | — | — | **not found**; the user has since named R1/R2 (the 20 videos) as the reference | open question, not blocking |
| R6 | Tutorial transcript | `/root/.claude/uploads/.../bd6e918e-download_6.txt` | user upload | transcript of the tutorial video about making the skill | method context | read | context only, not a visual reference |

## Non-reference media found (not references)
- `whale_short_final.mp4`, `whale_short_v3.mp4`, `whale_short_v4.mp4` (repo root), and the outputs in
  `work/whale-short/out/`: our own renders. **v4 is preserved unchanged** (55,583,021 bytes, 2 Nov 12:55).
- `work/clips/library/*.mp4` (77), `work/character/`, `work/cards/`, `work/anatomy/`, `work/flow_raw/`,
  `work/scenes_*`, `work/thumbnails/`, `.claude/skills/reel-hero-images-*`: the user's other projects
  (Effortless Exercise). Not references for this style.
- `/tmp/react-motion-render*/pre-encode.mp4`: render temp files.

## Classification of existing findings
| Finding | Class | Why |
|---|---|---|
| Our v4 measurements (brightness 0.63, saturation 0.39, edges 0.054, detail 0.011, sharpness 0.005, 8.6 s of speech pauses, 29 hard changes, new-picture rate 0.68) | **VERIFIED** (about our video) | measured on our file |
| R1-based targets (brightness 0.37, saturation 0.47, edges 0.099, etc.) | **VERIFIED, APPLICABLE** | measured on stills of the approved videos (38 frames, caption band masked) |
| Captions in the reference | **VERIFIED present** in 38/38 approved stills; **not a requirement**: the user decided no captions | user decision overrides |
| R3 numbers (cut rate, holds, shot mix, camera height, DOF share, voice speed, loudness) | **UNVERIFIED** | prior reports, partly contradictory |
| R3 bridge-specific "ours" values and recipes (soldiers, bridge, park swing) | **NOT APPLICABLE** | about another project |
| Technical fixes for this machine (SwiftShader + headless shell; hand-built post-processing composer; real dpr) | **VERIFIED** | they work in our renders |
| Whale-project readability fixes (recognisable whale and gulls, front-view close-ups, eye focus, cap fix) | **VERIFIED** (on our renders) | before/after stills |

## Reusable technical components (kept)
- `analysis/measure.py`: picture metrics + pacing. It re-runs on any approved set:
  `python3 analysis/measure.py <ours.mp4> <out.json>`. To point it at R5, change the `REF` path.
- `scripts/stills.mjs`, `render.mjs`, `render_all.sh`, `env.sh`, `sheet.py`, `voice_fit.py` (writes word timings),
  `sound.py`.
- Scene code `src/videos/whale/*` (captions OFF by default, opt-in only).

## Missing source material
1. **R4: the 20 reference video files**, or their URLs. These are needed for any claim about camera motion,
   transitions, animation timing, pacing and audio. Stills cannot establish those.
