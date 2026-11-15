# Image generation (Codex + ChatGPT Plus)

When the user asks to generate an image, use the Codex CLI signed in with their ChatGPT account. Do NOT ask for an OpenAI API key or call api.openai.com directly.

1. Install if missing: `npm install -g @openai/codex`
2. Check `codex login status`. If not logged in, run `codex login --device-auth` in the background (output to a file), then give the user the link https://auth.openai.com/codex/device and the one-time code, and wait for them to say "done".
3. Generate:
   `codex exec --sandbox workspace-write --skip-git-repo-check "Use your built-in image generation tool to create: <prompt>. Save it as <name>.png in the current directory."`
   (Generated files also land in `~/.codex/generated_images/`.)
4. Send the image to the user. For the Effortless Exercise Shorts, ALWAYS commit the generated images (owner, 15 Nov 2026), so another machine can rebuild the videos.

## Workflow (agent-skills)

Skills from addyosmani/agent-skills (commit 39b723c, MIT) are vendored in `.claude/` and load automatically in every session.

- For any engineering task, check `.claude/skills/using-agent-skills/SKILL.md` and apply the matching skill.
- Lifecycle: `/spec` → `/plan` → `/build` (or `/build auto`) → `/test` → `/review` → `/ship`.
- Other commands: `/constraints`, `/code-simplify`, `/webperf`.
- Subagents: `code-reviewer`, `security-auditor`, `test-engineer`, `web-performance-auditor`.
- Shared checklists: `.claude/references/`.

## Effortless Exercise Shorts (main project in this repo)
- How every video is made: `.claude/skills/shorts-director/SKILL.md`, section "THE METHOD". Thumbnails: `.claude/skills/effortless-exercise-thumbnail-prompts/SKILL.md`.
- New machine: `bash work/setup_env.sh`, then follow `work/HANDOFF-PROMPT.md`.
- The owner reads replies in Hinglish. Scripts, titles and prompts are in English. Keep usage low.
