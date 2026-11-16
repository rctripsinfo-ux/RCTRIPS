# shots.py Lxx -> Lxx.cuts.json (scene-change times) + Lxx_sheetN.jpg (one thumb per shot, time-stamped)
import sys, subprocess, re, json
from PIL import Image, ImageDraw
v = sys.argv[1]; th = float(sys.argv[2]) if len(sys.argv) > 2 else 0.12
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{v}.mp4", "-vf", f"scale=320:180,select='gt(scene,{th})',showinfo", "-f", "null", "-"], capture_output=True, text=True).stderr
ts = [0.0] + [float(x) for x in re.findall(r"pts_time:([\d.]+)", r)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{v}.mp4"], capture_output=True, text=True).stdout)
json.dump(dict(cuts=ts, dur=dur), open(f"{v}.cuts.json", "w"))
print(v, len(ts), "shots", round(dur / len(ts), 2), "s avg")
if len(sys.argv) > 3:
    cols, rows = 6, 6; per = cols * rows
    for k in range(0, len(ts), per):
        sh = Image.new("RGB", (cols * 320, rows * 180), "black"); d = ImageDraw.Draw(sh)
        for i, t in enumerate(ts[k:k + per]):
            f = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t + 0.25), "-i", f"{v}.mp4", "-frames:v", "1", "-vf", "scale=320:180", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            import io; im = Image.open(io.BytesIO(f)); sh.paste(im, ((i % cols) * 320, (i // cols) * 180)); d.rectangle([(i % cols) * 320, (i // cols) * 180, (i % cols) * 320 + 60, (i // cols) * 180 + 18], fill="black"); d.text(((i % cols) * 320 + 3, (i // cols) * 180 + 3), f"{t:.1f}", fill="yellow")
        sh.save(f"{v}_sheet{k // per}.jpg", quality=80)
