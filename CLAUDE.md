# Working rules for Claude in this repo

## Usage efficiency (top priority)
Minimize usage of weekly and 5-hour session limits while still completing tasks fully.

- Act directly. Skip long plans, recaps and option surveys unless asked.
- Don't spawn subagents or run parallel research unless the user asks.
- Read only the files and line ranges needed; use grep/search before opening whole files.
- Batch independent tool calls in one step; avoid re-reading files already seen.
- Prefer cheap paths: shell one-liners over many tool calls, existing scripts over new ones.
- Use web search sparingly ("standard" mode first); no deep research unless asked.
- Don't publish artifacts, generate images/video, or run heavy renders unless the task needs it.
- Keep replies short: result, what changed, anything blocking.
- If a task is better done outside Claude (e.g. in ChatGPT Plus: quick Q&A, brainstorming,
  rewording, image generation, translations), say so in one line instead of doing it here.
