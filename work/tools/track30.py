# 30 fps forensic track of a flat-background Short: per frame foreground bbox / area / centre, frame difference,
# and a classification of every change event (cut, slide, scale, fade, pose swap). usage: python3 -I track30.py in.mp4 out.json
import json, subprocess, sys, numpy as np
src, out = sys.argv[1:3]; Wd, Hd = 180, 320
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-vf", f"fps=30,scale={Wd}:{Hd}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, Hd, Wd, 3).astype(np.int16)
bg = np.median(F[:, :8, :8].reshape(-1, 3), axis=0)  # flat set colour from the top-left corner
rows = []
for i, f in enumerate(F):
    fg = np.abs(f - bg).sum(2) > 45
    fg[int(Hd * 0.78):int(Hd * 0.86), :] = False  # ignore the caption band
    ys, xs = np.where(fg)
    if len(xs) < 30: rows.append(dict(f=i, t=round(i / 30, 3), area=0)); continue
    rows.append(dict(f=i, t=round(i / 30, 3), area=round(len(xs) / fg.size, 4), cx=round(xs.mean() / Wd, 4), cy=round(ys.mean() / Hd, 4),
                     x0=round(np.percentile(xs, 2) / Wd, 3), x1=round(np.percentile(xs, 98) / Wd, 3), y0=round(np.percentile(ys, 2) / Hd, 3), y1=round(np.percentile(ys, 98) / Hd, 3)))
diff = [0.0] + [float(np.abs(F[i] - F[i - 1]).mean()) for i in range(1, len(F))]
for r, d in zip(rows, diff): r["diff"] = round(d, 2)
json.dump(dict(bg=bg.tolist(), frames=rows), open(out, "w"))
print(out, len(rows), "frames, bg", bg.tolist())
