# usage: python3 tools/sticker_ring.py in.png out.png  -> white-background picture to a cut-out with a white sticker ring + soft shadow
# (Mini-H cameo stays readable over a busy picture)
import sys, subprocess
from PIL import Image, ImageFilter
subprocess.run(["python3", "tools/cutout_white.py", sys.argv[1], "/tmp/_ring.png"], check=True, capture_output=True)
im = Image.open("/tmp/_ring.png"); pad = 16; c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); c.paste(im, (pad, pad), im)
a = c.getchannel("A").filter(ImageFilter.MaxFilter(13)); ring = Image.new("RGBA", c.size, (255, 255, 255, 255)); ring.putalpha(a)
sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.25))); sh = sh.filter(ImageFilter.GaussianBlur(6))
out = Image.new("RGBA", c.size, (0, 0, 0, 0)); out.alpha_composite(sh, (4, 6)); out.alpha_composite(ring); out.alpha_composite(c); out.save(sys.argv[2]); print(sys.argv[2], out.size)
