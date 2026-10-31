#!/usr/bin/env bash
# Puts the Reel Engine tool back exactly as it was in the last session (fresh cloud container).
# 1. installs the tool from the reel-video-maker skill, 2. copies our tool patches and asset libraries over it,
# 3. starts the server on port 3011 (the port fast_render.py uses).
set -e
W="$(cd "$(dirname "$0")" && pwd)"
T="$HOME/reel-engine-tool"
# the skill is in this repo (.claude/skills), so any Claude account gets it from git; else an installed/synced copy
MAKER=$(ls "$W"/../.claude/skills/reel-video-maker/scripts/make_video.py /root/.claude/skills/*/*/reel-video-maker/scripts/make_video.py "$W"/reel-video-maker/scripts/make_video.py 2>/dev/null | head -1)
[ -d "$T/node_modules" ] || python3 "$MAKER" setup

cp "$W"/tool-patches/{Captions.jsx,Video.jsx,fx.jsx,layers.jsx,schema.js,timeRefs.js} "$T/src/"
L="$T/public/library"
cp "$W"/anatomy/images/* "$W"/gags/images/* "$W"/cards/*.png "$L/hero/"
cp "$W"/clips/library/*.mp4 "$L/clips/"
cp "$W"/tool-patches/sfx/*.{wav,mp3} "$W"/tool-patches/typing_loud.mp3 "$L/sfx/" 2>/dev/null || true
cp "$W/tool-patches/hero-library.json" "$L/hero/library.json"
cp "$W/tool-patches/clips-library.json" "$L/clips/library.json"
cp "$W/tool-patches/sfx-library.json" "$L/sfx/library.json"

pkill -f "node tools/server.mjs" || true
cd "$T" && (PORT=3011 nohup node tools/server.mjs > /tmp/reel-server.log 2>&1 &)
for i in $(seq 30); do curl -s localhost:3011 >/dev/null && echo "Reel Engine up on :3011" && exit 0; sleep 1; done
echo "server did not start, see /tmp/reel-server.log"; exit 1
