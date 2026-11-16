import sys, subprocess, numpy as np, json
v = sys.argv[1]; fps = 6; w, h = 160, 90
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{v}.mp4", "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
a = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.int16)
d = np.abs(np.diff(a, axis=0)).mean((1, 2))
moving = (d > 0.6).mean(); big = d > 12
ev = int(((big[1:]) & (~big[:-1])).sum())
# longest still run (s)
still = d <= 0.6; best = cur = 0
for s in still: cur = cur + 1 if s else 0; best = max(best, cur)
bg = np.median(a[:, :4, :4])
json.dump(dict(v=v, dur=len(a) / fps, moving=round(float(moving), 2), hardcuts_per_min=round(ev / (len(a) / fps / 60), 1), longest_still_s=round(best / fps, 1)), open(f"{v}.motion.json", "w"))
print(v, f"moving {moving:.0%}", f"big changes/min {ev / (len(a) / fps / 60):.1f}", f"longest still {best / fps:.1f}s")
