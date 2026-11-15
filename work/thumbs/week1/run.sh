#!/bin/bash
# run.sh <name> <ref.png> <description>  -> <name>.png (Codex image, same character as the reference)
n=$1; r=$2; d=$3; mkdir -p job_$n; cp $r job_$n/ref.png; cd job_$n
codex exec --sandbox workspace-write --skip-git-repo-check "Use your built-in image generation tool to create this thumbnail, using the attached character reference: $d Save it as $n.png in the current directory." -i ref.png > log.txt 2>&1
cp $n.png ../$n.png 2>/dev/null && echo "$n ok" || echo "$n FAILED"
