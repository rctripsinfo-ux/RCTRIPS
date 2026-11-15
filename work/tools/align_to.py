# usage: python3 tools/align_to.py base.png out_dir name1.png [name2.png ...] [--height]
# cut out the base and every variant, match each variant's feet (or overall height with --height) to the base, and save all on the
# BASE's full canvas (same size, transparent) as <out_dir>/<name>_al.png -> any of them can swap in place with any other.
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage
args = [a for a in sys.argv[1:] if not a.startswith("--")]; mode_h = "--height" in sys.argv
base, outd, vars_ = args[0], args[1], args[2:]
def cut(p):
    im = Image.open(p).convert("RGB"); a = np.asarray(im).astype(int); white = a.min(-1) > 238; lab, _ = ndimage.label(white)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}; m = ~np.isin(lab, list(edge))
    m = ndimage.binary_opening(m, iterations=1); rgba = im.convert("RGBA"); rgba.putalpha(Image.fromarray((m * 255).astype(np.uint8))); return rgba, m
def anchor(m):
    ys, xs = np.nonzero(m); y0, y1 = ys.min(), ys.max(); band = m[int(y1 - (y1 - y0) * 0.12):y1 + 1]; bx = np.nonzero(band.any(0))[0]
    return bx.min(), bx.max(), y1, y1 - y0
B, mb = cut(base); bx0, bx1, by, bh = anchor(mb)
for v in [base] + vars_:
    V, mv = cut(v); vx0, vx1, vy, vh = anchor(mv)
    s = bh / vh if mode_h else (bx1 - bx0) / max(1, vx1 - vx0)
    s = min(max(s, 0.85), 1.15)  # Codex keeps scale close; never wildly rescale
    if "--noscale" in sys.argv: s = 1.0  # e.g. jumping jacks: the feet spread, the size does not change
    Vs = V.resize((int(V.width * s), int(V.height * s)), Image.LANCZOS); dx = (bx0 + bx1) / 2 - (vx0 + vx1) / 2 * s; dy = by - vy * s
    out = Image.new("RGBA", B.size, (0, 0, 0, 0)); out.alpha_composite(Vs, (int(dx), int(dy))) if dx >= 0 and dy >= 0 else out.paste(Vs, (int(dx), int(dy)), Vs)
    name = os.path.splitext(os.path.basename(v))[0]; out.save(f"{outd}/{name}_al.png"); print(name, f"scale {s:.3f} shift {dx:.0f},{dy:.0f}")
