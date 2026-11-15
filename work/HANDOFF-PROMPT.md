# Handoff prompt: paste this into a NEW Claude Code session (any cloud / machine) that has this repo

Copy everything inside the box into the first message.

```
You are taking over the "Effortless Exercise" YouTube Shorts project (cartoon character H + sidekick Mini-H).
Repo: rctripsinfo-ux/RCTRIPS. All work lives in work/. The latest state is on branch claude/intelligent-euler-6jm4o0:
fetch that branch and merge it into the branch you are allowed to work on (do NOT open a PR unless I ask).

1. Read, in this order:
   - CLAUDE.md
   - .claude/skills/shorts-director/SKILL.md (section "THE METHOD": this is exactly how every video is made)
   - .claude/skills/effortless-exercise-thumbnail-prompts/SKILL.md (brand colours dark red #7A1A1A + teal #0F8B85 + white words; layout varies)
   - work/content/30-DAY-SHORTS-PLAN.md (topics + scripts)
   - work/content/week1_upload.md and week2_upload.md (upload text style)
2. Set up the machine: run `bash work/setup_env.sh`.
   It installs ffmpeg, the Python libs, the Reel Engine tool, our library additions and the Codex CLI.
3. Voice needs GEMINI_API_KEY in the environment.
   - If it is missing, tell me to add it in the environment settings.
   - Never print it.
4. Images: use the Codex CLI with my ChatGPT account (CLAUDE.md).
   - Run `codex login status`.
   - If you are not logged in, run `codex login --device-auth` in the background and send me the link and the code.
5. Verify the setup by re-rendering one existing video, e.g. `cd work && LUFS=-20 python3 week1/day02_plan.py`.
   - Run `python3 tools/label_qa.py week1/day02_plan.py`.
   - Compare the result with final/day02.mp4.
6. Status:
   - Day 1–8 are DONE (work/final/dayNN_upload.mp4, with the thumbnail in the last frame).
   - Day 1 is uploaded.
   - Continue with Day 9 onward from the 30-day plan, one video at a time, exactly by THE METHOD:
     a. script
     b. two voices
     c. Codex poses (reuse the gesture library in work/week1/img2)
     d. plan with pose animation in every scene
     e. render at −20 LUFS
     f. label QA
     g. brand thumbnail appended to the last frame
     h. upload text
   - Commit everything, Codex images included, and push.
7. Reply to me in Hinglish. Scripts, titles, descriptions and prompts in English. Keep my usage low: no subagents, no needless renders.
```
