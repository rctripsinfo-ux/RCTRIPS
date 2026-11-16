# strip.py out.jpg "Lxx:t0:n[:step]" ... -> rows of consecutive 30 fps frames (each row = one event), labelled
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw
out = sys.argv[1]; rows = []
for spec in sys.argv[2:]:
    p = spec.split(":"); v, t0, n = p[0], float(p[1]), int(p[2]); step = int(p[3]) if len(p) > 3 else 1
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", f"{v}.mp4", "-vf", "fps=30,scale=240:135", "-frames:v", str(n * step), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, 135, 240, 3)[::step][:n]
    row = Image.new("RGB", (240 * n, 135), "black"); d = ImageDraw.Draw(row)
    for k, f in enumerate(F):
        row.paste(Image.fromarray(f), (240 * k, 0)); d.rectangle([240 * k, 0, 240 * k + 70, 13], fill="black"); d.text((240 * k + 2, 1), f"{v} {t0 + k * step / 30:.2f}", fill="yellow")
    rows.append(row)
W = max(r.width for r in rows); im = Image.new("RGB", (W, 135 * len(rows)), "black")
for k, r in enumerate(rows): im.paste(r, (0, 135 * k))
im.save(out, quality=82)
