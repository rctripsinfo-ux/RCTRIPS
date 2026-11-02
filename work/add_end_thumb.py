# Adds the owner's thumbnail as the LAST 0.1 s of a finished video (owner, 1 Nov), silent, 1080x1920.
# usage: python3 add_end_thumb.py day04 thumbnails/day04.jpg   (writes final/dayNN.mp4 in place; keeps final/dayNN-nothumb.mp4)
import os, shutil, subprocess, sys
n, thumb = sys.argv[1], sys.argv[2]
v, keep = f"final/{n}.mp4", f"final/{n}-nothumb.mp4"
if not os.path.exists(keep): shutil.copy(v, keep)
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", keep, "-loop", "1", "-t", "0.1", "-framerate", "30", "-i", thumb,
    "-f", "lavfi", "-t", "0.1", "-i", "anullsrc=r=48000:cl=stereo",
    "-filter_complex", "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p,fps=30[t];"
    "[0:v]fps=30,format=yuv420p,setsar=1[m];[m][0:a][t][2:a]concat=n=2:v=1:a=1[v][a]",
    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", v], check=True)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v], capture_output=True, text=True).stdout.strip()
print(n, "with end thumbnail:", d, "s")
