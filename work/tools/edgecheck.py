# usage: python3 -I edgecheck.py video.mp4 -> runs of frames where content touches a frame edge, + empty/black/frozen frames
import subprocess, sys, numpy as np
W, H = 360, 640; src = sys.argv[1]
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.int16); n = len(F)
sets = np.array([(186, 200, 208), (75, 85, 104)])
def fg(px):  # pixel is not one of the flat set colours
    return np.min(np.abs(px[..., None, :] - sets).sum(-1), -1) > 45
res = []
for i, f in enumerate(F):
    e = {"top": fg(f[:3]).mean(), "bottom": fg(f[-3:]).mean(), "left": fg(f[:, :3]).mean(), "right": fg(f[:, -3:]).mean()}
    res.append({k: v for k, v in e.items() if v > 0.02})
runs = []; cur = None
for i, r in enumerate(res + [{}]):
    key = tuple(sorted(r))
    if key and (cur is None or cur[2] != key): 
        if cur: runs.append(cur)
        cur = [i, i, key]
    elif key: cur[1] = i
    elif cur: runs.append(cur); cur = None
for a, b, k in runs: print(f"{a/30:6.2f}-{b/30:6.2f}s ({b-a+1:3d}f) edges: {','.join(k)}")
d = np.abs(np.diff(F, axis=0)).mean((1, 2, 3)); dark = (F.mean((1, 2, 3)) < 20).sum()
print(f"frames {n} ({n/30:.2f}s), near-black frames {dark}, frozen stretches >2s:",
      sum(1 for _ in [0]) if False else [round(i / 30, 1) for i in range(60, len(d)) if d[i - 60:i].max() < 0.05][:5])
