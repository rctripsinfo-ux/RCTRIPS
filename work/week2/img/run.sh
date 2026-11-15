#!/bin/bash
# run.sh <name> <ref.png> <description>  -> <name>.png (Codex image, same character as the reference)
n=$1; r=$2; d=$3; mkdir -p job_$n; cp $r job_$n/ref.png; cd job_$n
codex exec --sandbox workspace-write --skip-git-repo-check "Use your built-in image generation tool to create: $d Keep the exact same character as the attached reference (H: bald muscular man, white H mark on the forehead, same face, skin tone, black shorts, olive tactical belt with pouches, black wristbands, dark olive sneakers, same semi-realistic comic illustration style with clean ink outlines and cel shading). Plain pure white background, nothing else, vertical 9:16, no text, no watermark. Save it as $n.png in the current directory." -i ref.png > log.txt 2>&1
cp $n.png ../$n.png 2>/dev/null && echo "$n ok" || echo "$n FAILED"
