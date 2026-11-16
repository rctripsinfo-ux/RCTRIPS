# uni.py Lxx [t0 t1 n] -> uniform contact sheet (6x6, time-stamped); default whole video
import sys, subprocess, io
from PIL import Image, ImageDraw
v = sys.argv[1]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{v}.mp4"], capture_output=True, text=True).stdout)
t0, t1, n = (float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0.5, dur - 0.5, 36)
cols = 6; rows = (n + cols - 1) // cols; sh = Image.new("RGB", (cols * 320, rows * 180), "black"); d = ImageDraw.Draw(sh)
for i in range(n):
    t = t0 + (t1 - t0) * i / max(1, n - 1)
    f = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", f"{v}.mp4", "-frames:v", "1", "-vf", "scale=320:180", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    x, y = (i % cols) * 320, (i // cols) * 180; sh.paste(Image.open(io.BytesIO(f)), (x, y)); d.rectangle([x, y, x + 52, y + 16], fill="black"); d.text((x + 3, y + 2), f"{t:.1f}", fill="yellow")
sh.save(f"{v}_{'u' if len(sys.argv) <= 4 else f'd{int(t0)}'}.jpg", quality=78)
