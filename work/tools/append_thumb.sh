#!/bin/bash
# usage: tools/append_thumb.sh video.mp4 thumb.png out.mp4 [seconds=0.1]
# appends the thumbnail as the last frames of the Short (pick it as the cover when uploading); audio padded with silence
v=$1; img=$2; out=$3; d=${4:-0.1}
ffmpeg -loglevel error -y -i "$v" -loop 1 -framerate 30 -t "$d" -i "$img" -filter_complex \
 "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p[t];[0:v]fps=30,format=yuv420p,setsar=1[m];[m][t]concat=n=2:v=1:a=0[v];[0:a]apad=pad_dur=$d[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -shortest "$out"
