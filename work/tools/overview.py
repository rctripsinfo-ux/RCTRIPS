# usage: python3 -I overview.py vid fps out.jpg [t0 t1]  -> grid of frames with time labels
import cv2, glob, sys
from PIL import Image, ImageDraw
v, fps, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
cap = cv2.VideoCapture(glob.glob(f"comp2/{v}_*.mp4")[0]); dur = cap.get(7) / cap.get(5)
t0, t1 = (float(sys.argv[4]), float(sys.argv[5])) if len(sys.argv) > 5 else (0, dur)
W, H, C = 90, 160, 12; ts = [t0 + k / fps for k in range(int((t1 - t0) * fps))]
R = (len(ts) + C - 1) // C; im = Image.new("RGB", (C * W, R * H), "white"); d = ImageDraw.Draw(im)
for k, t in enumerate(ts):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
    if not ok: continue
    x, y = (k % C) * W, (k // C) * H; im.paste(Image.fromarray(cv2.cvtColor(cv2.resize(f, (W, H)), cv2.COLOR_BGR2RGB)), (x, y))
    d.rectangle([x, y, x + 26, y + 10], fill="black"); d.text((x + 1, y), f"{t:.1f}", fill="yellow")
im.save(out, quality=80); print(out, im.size)
