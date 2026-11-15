#!/bin/bash
# one Codex image job: run.sh <name> <description>
n=$1; d=$2; mkdir -p job_$n; cp ref_h.png job_$n/; cd job_$n
codex exec --sandbox workspace-write --skip-git-repo-check "Use your built-in image generation tool to create: the same character as in the attached reference image, called H (exact same face, bald head with the white H mark on the forehead, same skin tone, same body, black shorts, olive tactical belt with pouches, black wristbands, dark olive sneakers, same semi-realistic comic illustration style with clean ink outlines and cel shading). Scene: $d. Plain pure white background, nothing else in the background, vertical 9:16, no text, no watermark. Save it as $n.png in the current directory." -i ref_h.png > log.txt 2>&1
cp $n.png ../$n.png 2>/dev/null && echo "$n ok" || echo "$n FAILED"
