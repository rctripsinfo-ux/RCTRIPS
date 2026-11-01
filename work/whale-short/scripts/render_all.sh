#!/bin/bash
# renders the short in chunks at 720x1280 (dpr 0.6667), resumable: skips chunks that already exist
cd "$(dirname "$0")/.." && . scripts/env.sh
mkdir -p out/final/chunks
for a in 0 250 500 750 1000 1250 1500 1750; do
  b=$((a + 249)); [ $b -gt 1974 ] && b=1974
  f=out/final/chunks/c_$(printf %04d $a).mp4
  [ -s "$f" ] && continue
  PROPS='{"post":{"dpr":0.75}}' CHROME=$CHROME GL=$GL node scripts/render.mjs WhaleShort "$f.tmp.mp4" $a-$b 0.75 1 >> out/final/render.log 2>&1 && mv "$f.tmp.mp4" "$f"
  echo "chunk $a-$b $(date +%T)" >> out/final/render.log
done
echo ALLDONE >> out/final/render.log
