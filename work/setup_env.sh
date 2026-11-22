#!/bin/bash
# One-time setup of a fresh machine for the Effortless Exercise Shorts pipeline (run from anywhere: bash work/setup_env.sh)
# Installs: ffmpeg + python libs, the Reel Engine tool (word alignment server + H pose library), our own library additions,
# the Codex CLI (image generation through the owner's ChatGPT account). Safe to run again.
set -e
W="$(cd "$(dirname "$0")" && pwd)"; R="$(dirname "$W")"
command -v ffmpeg >/dev/null || { (sudo -n true 2>/dev/null && S=sudo) ; $S apt-get update -qq && $S apt-get install -y -qq ffmpeg; }
python3 -m pip install -q pillow numpy scipy opencv-python-headless pocketsphinx soundfile yt-dlp 2>/dev/null || python3 -m pip install -q --break-system-packages pillow numpy scipy opencv-python-headless pocketsphinx soundfile yt-dlp
# Reel Engine tool + H images (skill reel-video-maker unpacks tool.tar.gz and the reel-hero-images-1..3 packs)
[ -d ~/reel-engine-tool/public/library/hero ] || python3 "$R/.claude/skills/reel-video-maker/scripts/make_video.py" setup
[ -d ~/reel-engine-tool/node_modules ] || (cd ~/reel-engine-tool && npm install --silent)
# our additions to the library: aligned push-up pair, props, synthesized SFX
cp -n "$W"/character/pairs/*.png "$W"/character/props/*.png ~/reel-engine-tool/public/library/hero/ 2>/dev/null || true
cp -n "$W"/sfx/*.wav ~/reel-engine-tool/public/library/sfx/ 2>/dev/null || true
# Codex CLI for images (log in once: codex login --device-auth, the owner enters the code)
command -v codex >/dev/null || npm install -g @openai/codex
echo "Setup done. Next: GEMINI_API_KEY must be set (voice). Codex: run 'codex login status' (login with --device-auth if needed)."
pip install -q "earshot @ git+https://github.com/Leonxlnx/earshot"  # SFX maker (MIT); pack in work/sfx/es
