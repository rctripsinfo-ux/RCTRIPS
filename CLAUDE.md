# Image generation (Codex + ChatGPT Plus)

When the user asks to generate an image, use the Codex CLI signed in with their ChatGPT account. Do NOT ask for an OpenAI API key or call api.openai.com directly.

1. Install if missing: `npm install -g @openai/codex`
2. Check `codex login status`. If not logged in, run `codex login --device-auth` in the background (output to a file), then give the user the link https://auth.openai.com/codex/device and the one-time code, and wait for them to say "done".
3. Generate:
   `codex exec --sandbox workspace-write --skip-git-repo-check "Use your built-in image generation tool to create: <prompt>. Save it as <name>.png in the current directory."`
   (Generated files also land in `~/.codex/generated_images/`.)
4. Send the image to the user, and save it into the repo only if asked.

## Workflow (agent-skills)

Skills from addyosmani/agent-skills (commit 39b723c, MIT) are vendored in `.claude/` and load automatically in every session.

- For any engineering task, check `.claude/skills/using-agent-skills/SKILL.md` and apply the matching skill.
- Lifecycle: `/spec` → `/plan` → `/build` (or `/build auto`) → `/test` → `/review` → `/ship`.
- Other commands: `/constraints`, `/code-simplify`, `/webperf`.
- Subagents: `code-reviewer`, `security-auditor`, `test-engineer`, `web-performance-auditor`.
- Shared checklists: `.claude/references/`.
