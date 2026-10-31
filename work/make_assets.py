# Our own (royalty-free) extra assets, made in code: sunburst + impact speed-line backgrounds, soft sad sting.
# Run once per container (restore_tool.sh calls it): python3 make_assets.py
import json, math, os, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
LIB = os.path.expanduser("~/reel-engine-tool/public/library")
W, H = 1080, 1920


def rays(name, c1, c2, n, cx=0.5, cy=0.45, blur=0):
    im = Image.new("RGB", (W, H), c1); d = ImageDraw.Draw(im); R = 2600; ox, oy = W * cx, H * cy
    for k in range(n):
        a0 = 2 * math.pi * k / n; a1 = a0 + math.pi / n
        d.polygon([(ox, oy), (ox + R * math.cos(a0), oy + R * math.sin(a0)), (ox + R * math.cos(a1), oy + R * math.sin(a1))], fill=c2)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f"{LIB}/hero/{name}.webp", "WEBP", quality=85)
    return {"id": name, "file": f"{name}.webp", "kind": "image", "description": f"{name} full-screen background", "tags": ["prop", "background"],
            "size": [W, H], "bbox": [0, 0, 1, 1], "area": 1.0}


def impact(name):
    # anime speed lines: warm centre glow, thin dark radial streaks toward the edges
    im = Image.new("RGB", (W, H), "#F2C27B"); d = ImageDraw.Draw(im); rng = np.random.default_rng(3); ox, oy = W / 2, H * 0.45
    for _ in range(170):
        a = rng.uniform(0, 2 * math.pi); r0 = rng.uniform(420, 700); r1 = 2400; w = int(rng.integers(3, 14))
        d.line([(ox + r0 * math.cos(a), oy + r0 * math.sin(a)), (ox + r1 * math.cos(a), oy + r1 * math.sin(a))], fill="#7A4A22", width=w)
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse([ox - 520, oy - 620, ox + 520, oy + 620], fill=255)
    im = Image.composite(Image.new("RGB", (W, H), "#FFE7B8"), im, g.filter(ImageFilter.GaussianBlur(160)))
    im.save(f"{LIB}/hero/{name}.webp", "WEBP", quality=85)
    return {"id": name, "file": f"{name}.webp", "kind": "image", "description": "anime speed-line impact background", "tags": ["prop", "background"],
            "size": [W, H], "bbox": [0, 0, 1, 1], "area": 1.0}


def sad_sting(path):
    # two soft falling piano-like notes (E4 -> C4), 1.3 s, gentle decay; not a meme sound
    sr = 44100; out = np.zeros(int(sr * 1.5))
    for f, t0 in ((329.6, 0.0), (261.6, 0.45)):
        t = np.arange(int(sr * 0.95)) / sr
        tone = sum(a * np.sin(2 * math.pi * f * h * t) for h, a in ((1, 1), (2, 0.35), (3, 0.12)))
        env = np.exp(-t * 3.2) * np.minimum(1, t / 0.01)
        s = int(sr * t0); out[s:s + len(t)] += tone * env
    out = (out / np.abs(out).max() * 0.6 * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(out.tobytes())


lib = json.load(open(f"{LIB}/hero/library.json"))
new = [rays("bg_sunburst", "#FFF3C4", "#F7C548", 28), impact("bg_impact")]
ids = {a["id"] for a in new}
lib["assets"] = sorted([a for a in lib["assets"] if a["id"] not in ids] + new, key=lambda a: a["id"])
json.dump(lib, open(f"{LIB}/hero/library.json", "w"), indent=1)
sad_sting(f"{LIB}/sfx/sad_sting.wav")
sl = json.load(open(f"{LIB}/sfx/library.json"))
sl["assets"] = [a for a in sl["assets"] if a["id"] != "sfx_sad_sting"] + [{"id": "sfx_sad_sting", "file": "sad_sting.wav", "kind": "audio",
    "category": "emotion", "volume": 0.9, "duration": 1.4, "description": "soft sad two-note sting (black sad beat)"}]
json.dump(sl, open(f"{LIB}/sfx/library.json", "w"), indent=1)
print("assets ok")
