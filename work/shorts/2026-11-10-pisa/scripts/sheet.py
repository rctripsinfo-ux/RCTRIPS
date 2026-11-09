# contact sheet: python3 scripts/sheet.py out.jpg img1 img2 ... (cols=4, each scaled to 270x480)
import sys
from PIL import Image, ImageDraw
out, ims = sys.argv[1], sys.argv[2:]
cols = 4; W, Hh = 270, 480; rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (cols * W, rows * Hh), "white"); d = ImageDraw.Draw(sh)
for i, p in enumerate(ims):
    im = Image.open(p).convert("RGB").resize((W, Hh)); x, y = (i % cols) * W, (i // cols) * Hh
    sh.paste(im, (x, y)); d.text((x + 6, y + 6), p.split("_")[-1].split(".")[0], fill="red")
sh.save(out, quality=88)
