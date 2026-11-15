# Image generation (Codex + ChatGPT Plus)

When the user asks to generate an image, use the Codex CLI signed in with their ChatGPT account. Do NOT ask for an OpenAI API key or call api.openai.com directly.

1. Install if missing: `npm install -g @openai/codex`
2. Check `codex login status`. If not logged in, run `codex login --device-auth` in the background (output to a file), then give the user the link https://auth.openai.com/codex/device and the one-time code, and wait for them to say "done".
3. Generate:
   `codex exec --sandbox workspace-write --skip-git-repo-check "Use your built-in image generation tool to create: <prompt>. Save it as <name>.png in the current directory."`
   (Generated files also land in `~/.codex/generated_images/`.)
4. Send the image to the user, and save it into the repo only if asked.
