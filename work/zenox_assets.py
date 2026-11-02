# Assets for the "Zenox format" (age tier list, ref/ analysis of R04): our own, made in code, white background (owner, 2 Nov).
# White room with a light-grey floor band, "AGE · N" tags (white box, black border, black text, red number), heavy black
# headings ("15-20 SQUATS"). Run after restore_tool.sh: python3 zenox_assets.py "15-20 SQUATS" ... (headings to make)
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
LIB = os.path.expanduser("~/reel-engine-tool/public/library")
W, H = 1080, 1920
BLACK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
INK, RED = "#15171A", "#E3262E"


def entry(name, size, desc, bbox=(0, 0, 1, 1), area=1.0):
    return {"id": name, "file": f"{name}.png", "kind": "image", "description": desc, "tags": ["prop", "zenox"],
            "size": list(size), "bbox": list(bbox), "area": area}


def floor_bg():
    # R04: flat room, darker floor band over the bottom ~30% (here: white + very light grey, owner wants white)
    im = Image.new("RGB", (W, H), "#FFFFFF"); d = ImageDraw.Draw(im)
    d.rectangle([0, int(H * 0.72), W, H], fill="#EEF0F3"); d.line([0, int(H * 0.72), W, int(H * 0.72)], fill="#DCE0E5", width=4)
    im.save(f"{LIB}/hero/bg_white_floor.png"); return entry("bg_white_floor", (W, H), "white room with a light grey floor band from y 0.72")


def tag(name, parts, size=58, pad=(26, 14), border=5):
    # parts = [(text, colour)], drawn on one line in a white box with a black border
    f = ImageFont.truetype(BLACK, size); widths = [f.getlength(t) for t, _ in parts]
    asc, desc = f.getmetrics(); w = int(sum(widths) + 2 * pad[0]); h = asc + desc + 2 * pad[1]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill="#FFFFFF", outline=INK, width=border)
    x = pad[0]
    for (t, c), tw in zip(parts, widths): d.text((x, pad[1]), t, font=f, fill=c); x += tw
    im.save(f"{LIB}/hero/{name}.png"); return entry(name, (w, h), "tag " + "".join(t for t, _ in parts))


def heading(name, text, size=104):
    f = ImageFont.truetype(BLACK, size); w = int(f.getlength(text)) + 20; asc, desc = f.getmetrics()
    im = Image.new("RGBA", (w, asc + desc + 10), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 5), text, font=f, fill=INK)
    im.save(f"{LIB}/hero/{name}.png"); return entry(name, im.size, "heading " + text)


def slug(t): return "".join(c if c.isalnum() else "_" for c in t.lower()).strip("_")


new = [floor_bg()]
for n in ("10", "20", "30", "40", "50", "60+"):
    new.append(tag(f"tag_age_{slug(n)}", [("AGE · ", INK), (n, RED)]))
new += [tag("tag_age_q", [("AGE?", INK)]), tag("tag_squats_q", [("SQUATS?", INK)])]
for t in sys.argv[1:]: new.append(heading("head_" + slug(t), t))
lib = json.load(open(f"{LIB}/hero/library.json")); ids = {a["id"] for a in new}
lib["assets"] = sorted([a for a in lib["assets"] if a["id"] not in ids] + new, key=lambda a: a["id"])
json.dump(lib, open(f"{LIB}/hero/library.json", "w"), indent=1)
print(" ".join(a["id"] for a in new))
