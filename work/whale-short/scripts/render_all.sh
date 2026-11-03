#!/bin/bash
# renders the short in chunks at 720x1280 (dpr 0.6667), resumable: skips chunks that already exist
cd "$(dirname "$0")/.." && . scripts/env.sh
mkdir -p out/final4/chunks
for a in 0 250 500 750 1000 1250 1500 1750; do
  b=$((a + 249)); [ $b -gt 1891 ] && b=1891
  f=out/final4/chunks/c_$(printf %04d $a).mp4
  [ -s "$f" ] && continue
  PROPS='{"post":{"dpr":1}}' CHROME=$CHROME GL=$GL node scripts/render.mjs WhaleShort "$f.tmp.mp4" $a-$b 1 1 >> out/final4/render.log 2>&1 && mv "$f.tmp.mp4" "$f"
  echo "chunk $a-$b $(date +%T)" >> out/final4/render.log
done
echo ALLDONE >> out/final4/render.log
