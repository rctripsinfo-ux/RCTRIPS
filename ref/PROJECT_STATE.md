# PROJECT_STATE: reference-channel reverse engineering (source of truth for new sessions)
Last update: 2 Nov 2026. Branch `claude/intelligent-euler-6jm4o0`, repo `rctripsinfo-ux/RCTRIPS`.

## Restore in a new session
```bash
pip install -q gdown && mkdir -p ref/raw && gdown --folder "https://drive.google.com/drive/folders/1_FLBzd0J0zkQn9ux34C4Td20vO0fXb3L" -O ref/raw
python3 -I ref/tools/inventory.py ref/raw ref/analysis        # cached: skips unchanged files
python3 -I ref/tools/analyze.py ref/raw ref/analysis          # cached by sha1 + TOOL_VER (~14 s/video if re-run)
python3 -I ref/tools/overview.py ref/raw ref/analysis         # 1 fps sheets (git-ignored)
python3 -I ref/tools/motion_events.py ref/analysis
```
- `ref/raw/`, `analysis/sheets/` and `analysis/overview/` are **git-ignored**: third-party frames stay local.
- Measurements (csv/json) are committed.

## Phases
| # | Phase | Status | Output |
|---|---|---|---|
| 1 | Inventory | COMPLETE | `analysis/REFERENCE_INVENTORY.csv`, `INITIAL_ASSESSMENT.md` |
| 2 | Local analysis tools | COMPLETE | `tools/*.py`, `analysis/R*/`, `analysis/ANALYSIS_MANIFEST.json`, `analysis/SCENE_TIMELINE.csv` |
| 3 | Style reverse engineering | PARTIAL | First findings in `INITIAL_ASSESSMENT.md` §3. To do: typography, caption timing, sfx classes, colour palette. |
| 4 | Frame-level blueprint | PARTIAL | `CAMERA_MOTION_RULES.json` (rise-in, punch zoom, slides). To do: 3–4 scene specs. |
| 5 | Subagents | DECIDED: none for now | `INITIAL_ASSESSMENT.md` §6 |
| 6 | Style rulebook | NOT STARTED | `CHANNEL_STYLE_RULEBOOK.md` |
| 7 | Tech decision | PROPOSED (A: Reel Engine + patches) | `INITIAL_ASSESSMENT.md` §4 |
| 8 | 5–10 s reconstruction test | NOT STARTED | Suggested: R07 0.0–10.2 s (before/after, rise-ins, word-pop heading, "LET ME FIX" bumper) |
| 9 | Gap audit | NOT STARTED | `RECONSTRUCTION_GAP_REPORT.md` |
| 10 | Skill | NOT STARTED | `.claude/skills/channel-video-engine/SKILL.md` |
| 11 | Full original video | NOT STARTED | |
| 12 | Persistent files | PARTIAL | This file, `NEXT_STEPS.md` |

## Owner decisions
- **2 Nov:** background is **white**. Keep H. The channel is Zenox (10 Shorts, all analysed). Weight the rules toward R04 and R05 (3.1M / 2.4M views).
- **29 Oct (from the H project):** no exercise clip videos. Exercises use H pose images.

## Known issues
- **R09/R10:** a burned-in grey bar from the capture. It adds static features, so camera motion is under-estimated there.
- **Flat backgrounds:** "camera" motion = motion of the main content layer. A true camera move can't be separated from a layer move.
- **Transitions:** the first frame of a transition is often a cut frame and isn't tracked, so travel distances are lower bounds.
- **Captions:** auto-generated SRTs have unreliable punctuation, and "[music]" tags appear inside the text.
