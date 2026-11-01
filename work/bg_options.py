# 10 background options for H (owner, 1 Nov): each tile = background + H + heading + caption, as in a real frame.
# The CSS of each option goes into the plan's canvas.background (BG below). usage: python3 bg_options.py
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H = 540, 960
BG = {  # name: (css, top colour, bottom colour, spotlight colour or None, texture, heading colour)
 1: ("Sand beige (now)", "#E2D3B9", "#E2D3B9", "#FFF6E6", False, "#1E2228"),
 2: ("Slate blue-grey", "linear-gradient(#9AA6B2,#B0BAC3)", "#9AA6B2", "#B0BAC3", None, False, "#1E2228"),
 3: ("Clean white", "#FFFFFF", "#FFFFFF", None, False, "#1E2228"),
 4: ("Studio light grey", "#D9DCE0", "#C9CDD3", "#F4F5F7", False, "#1E2228"),
 5: ("Charcoal spotlight", "#1E2228", "#14171C", "#4A515C", False, "#FFFFFF"),
 6: ("Night navy", "linear-gradient(#1E2A44,#2F4A7A)", "#1E2A44", "#2F4A7A", "#4B6EA8", False, "#FFFFFF"),
 7: ("Sunset orange", "linear-gradient(#F6A04D,#F7D08A)", "#F6A04D", "#F7D08A", None, False, "#1E2228"),
 8: ("Soft mint", "linear-gradient(#BFE3D8,#E6F4EF)", "#BFE3D8", "#E6F4EF", None, False, "#1E2228"),
 9: ("Power red", "linear-gradient(#7F1D1D,#DC2626)", "#7F1D1D", "#DC2626", "#F87171", False, "#FFFFFF"),
 10: ("Concrete gym wall", "#8E9196", "#7D8086", "#9A9DA2", "#B5B8BC", True, "#FFFFFF"),
}
def hexc(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)
def bg(spec):
    name, css, top, bot, *rest = spec if len(spec) == 7 else (spec[0], spec[1], spec[1], spec[2], spec[3], spec[4], spec[5])
    spot, tex = rest[0], rest[1]
    y = np.linspace(0, 1, H)[:, None, None]; a = hexc(top) * (1 - y) + hexc(bot) * y; a = np.repeat(a, W, 1)
    if spot:
        yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (0.6 * W)) ** 2 + ((yy - 0.52 * H) / (0.55 * H)) ** 2)
        k = (np.clip(1 - d, 0, 1) ** 1.5 * 0.55)[..., None]; a = a * (1 - k) + hexc(spot) * k
    if tex:
        rng = np.random.default_rng(1); n = rng.normal(0, 9, (H // 4, W // 4)); n = np.kron(n, np.ones((4, 4)))[:H, :W]
        a = a + n[..., None] + rng.normal(0, 4, (H, W, 1))
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
font = ImageFont.truetype("/root/reel-engine-tool/.cache/ui/bebas-neue-latin-400-normal-6RSG64MI.woff2", 70)
cap = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 26)
lab = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 30)
hero = Image.open("/root/reel-engine-tool/public/library/hero/sc_d04_x08.webp").convert("RGBA")
hero = hero.crop(hero.getbbox()); hero.thumbnail((int(W * 0.78), int(H * 0.66)))
tiles = []
for k, spec in BG.items():
    norm = (spec[0], spec[1], spec[1], spec[2], spec[3], spec[4], spec[5]) if len(spec) == 6 else (spec[0], spec[1], spec[2], spec[3], spec[4], spec[5], spec[6])
    im = bg(norm).convert("RGBA"); dr = ImageDraw.Draw(im)
    sh = Image.new("RGBA", (hero.width, 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([hero.width * 0.15, 5, hero.width * 0.85, 35], fill=(0, 0, 0, 60))
    x, y = (W - hero.width) // 2, int(H * 0.25); im.alpha_composite(sh, (x, y + hero.height - 22)); im.alpha_composite(hero, (x, y))
    dr.text((W / 2, H * 0.15), "STIFF NECK?", font=font, fill=norm[6], anchor="mm")
    dr.text((W / 2, H * 0.82), "your neck feels", font=cap, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    dr.rectangle([0, 0, W, 52], fill=(0, 0, 0, 170)); dr.text((14, 26), f"{k}. {norm[0]}", font=lab, fill="#FACC15", anchor="lm")
    tiles.append(im.convert("RGB"))
sheet = Image.new("RGB", (W * 5 + 40, H * 2 + 30), "white")
for i, t in enumerate(tiles): sheet.paste(t, ((i % 5) * (W + 10), (i // 5) * (H + 30)))
sheet.save("backgrounds/bg-10-options.jpg", quality=82)
import json; json.dump({k: {"name": v[0], "css": v[1]} for k, v in BG.items()}, open("backgrounds/bg-10-options.json", "w"), indent=1)
