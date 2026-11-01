# Owner's Flow images on a BLUE gradient (or white) background -> same image on pure white, so import_scenes.py cuts it out.
# Removes the blue background (flood from the border + big enclosed blue pockets), then keeps only the big pieces
# (H and the props touching him): side labels ("CHIN TUCK"), icons and the Gemini sparkle disappear.
# usage: python3 blue_cutout.py <src.jpg> <out.webp> [min_piece=0.03] [light=195]
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
src, out = sys.argv[1:3]; keep = float(sys.argv[3]) if len(sys.argv) > 3 else 0.03
LIGHT = int(sys.argv[4]) if len(sys.argv) > 4 else 195  # lower (e.g. 120) also removes grey ghost limbs
rgb = np.asarray(Image.open(src).convert("RGB")).astype(int); r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
blue = ((b - r > 18) & (b >= g - 5)) | ((rgb.min(axis=2) > LIGHT) & (np.ptp(rgb, axis=2) < 40))  # blue bg / wall / shadow, or white-light-grey bg, glow, ghost limbs
lab, n = ndimage.label(blue); sz = ndimage.sum(blue, lab, range(1, n + 1))
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, [i + 1 for i in range(n) if (i + 1) in border or sz[i] > 0.0015 * blue.size])
fg = ndimage.binary_opening(~bg, iterations=1)
lab, n = ndimage.label(fg); sz = ndimage.sum(fg, lab, range(1, n + 1))
fg = np.isin(lab, [i + 1 for i in range(n) if sz[i] >= keep * sz.max()])
fg = ndimage.binary_fill_holes(fg) & ~bg | (fg)
a = np.asarray(Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))) / 255.0
o = rgb * a[..., None] + 255 * (1 - a[..., None])
Image.fromarray(o.clip(0, 255).astype(np.uint8)).save(out, "WEBP", quality=92)
