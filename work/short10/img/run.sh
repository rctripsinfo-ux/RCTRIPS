#!/bin/bash
# run.sh <name> <ref1[,ref2]> <description> [orientation]  -> <name>.png. Background is part of the description (no forced white).
n=$1; r=$2; d=$3; O=${4:-vertical 9:16}; mkdir -p job_$n; args=(); i=0
for f in ${r//,/ }; do i=$((i+1)); cp $f job_$n/ref$i.png; args+=(-i ref$i.png); done
cd job_$n
codex exec --sandbox workspace-write --skip-git-repo-check "Use your built-in image generation tool to create: $d Format: $O, no watermark. Save it as $n.png in the current directory." "${args[@]}" > log.txt 2>&1 < /dev/null
cp $n.png ../$n.png 2>/dev/null && echo "$n ok" || echo "$n FAILED"
