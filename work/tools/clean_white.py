# usage: python3 tools/clean_white.py a_al.png [...]  -> removes leftover white BACKGROUND trapped inside cut-outs
# (gaps between arms and body, under tables, inside a pull-up bar frame), keeps real white details:
# a component is removed when it is flat pure white (>= 85% of its pixels >= 247) and is not surrounded by skin (the H on the forehead).
import sys, numpy as np
from PIL import Image
from scipy import ndimage
for f in sys.argv[1:]:
    im = Image.open(f).convert("RGBA"); a = np.array(im); rgb = a[..., :3].astype(int); al = a[..., 3]
    white = (rgb.min(-1) >= 232) & (al > 0)
    lab, k = ndimage.label(white)
    if not k: continue
    idx = np.arange(1, k + 1); size = ndimage.sum(white, lab, idx)
    pure = ndimage.sum((rgb.min(-1) >= 247) & white, lab, idx)
    kill = np.zeros_like(white)
    for i, (sz, pu) in enumerate(zip(size, pure), 1):
        if sz < 120 or pu / sz < 0.85: continue
        comp = lab == i; ring = ndimage.binary_dilation(comp, iterations=4) & ~comp & (al > 0)
        r, g, b = rgb[ring].T if ring.any() else (np.array([0]),) * 3
        skin = ((r > 150) & (r - b > 40) & (r > g)).mean() if ring.any() else 0
        if skin > 0.6 and sz < 6000: continue  # the white H on the forehead
        kill |= comp
    if kill.any():
        grow = ndimage.binary_dilation(kill, iterations=1) & ((rgb.min(-1) >= 215) | kill)
        a[grow, 3] = 0; Image.fromarray(a).save(f); print(f, int(grow.sum()))
