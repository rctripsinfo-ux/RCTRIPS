# usage: python3 -I strips.py out.jpg "vid:t0:step:n[:label]" ...  -> one row per spec, frames from comp2/<vid>_*.mp4
import cv2, glob, sys
from PIL import Image, ImageDraw
out, specs = sys.argv[1], sys.argv[2:]; W, H = 108, 192; rows = []
for sp in specs:
    v, t0, st, n, *lab = sp.split(":"); t0, st, n = float(t0), float(st), int(n)
    cap = cv2.VideoCapture(glob.glob(f"comp2/{v}_*.mp4")[0]); row = []
    for k in range(n):
        cap.set(cv2.CAP_PROP_POS_MSEC, max(0, t0 + k * st) * 1000); ok, f = cap.read()
        row.append(Image.fromarray(cv2.cvtColor(cv2.resize(f, (W, H)), cv2.COLOR_BGR2RGB)) if ok else Image.new("RGB", (W, H)))
    rows.append((f"{v} {t0:.2f}+{st}s {' '.join(lab)}", row))
n = max(len(r) for _, r in rows); im = Image.new("RGB", (n * W, len(rows) * (H + 12)), "white"); d = ImageDraw.Draw(im)
for i, (lab, r) in enumerate(rows):
    d.text((2, i * (H + 12)), lab, fill="black")
    for j, f in enumerate(r): im.paste(f, (j * W, i * (H + 12) + 12))
im.save(out, quality=82); print(out, im.size)
