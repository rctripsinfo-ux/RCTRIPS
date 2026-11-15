# usage: python3 tools/align_pair.py a.png b.png out_a.png out_b.png [anchor_frac=0.18]
# cut both poses out of their white background, then scale/shift B so its feet (bottom anchor_frac of the figure) match A's feet:
# same feet width, same floor line, same centre. Both saved on one shared transparent canvas -> pose swaps stay in place.
import sys, numpy as np, subprocess
from PIL import Image
a_p, b_p, oa, ob = sys.argv[1:5]; fr = float(sys.argv[5]) if len(sys.argv) > 5 else 0.18
def cut(p):
    subprocess.run(["python3", "tools/cutout_white.py", p, "/tmp/_c.png"], check=True, capture_output=True)
    im = Image.open(p).convert("RGB"); c = Image.open("/tmp/_c.png")
    # cutout_white crops; redo uncropped mask for coordinates
    from scipy import ndimage
    a = np.asarray(im).astype(int); white = a.min(-1) > 238; lab, _ = ndimage.label(white)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}; m = ~np.isin(lab, list(edge))
    rgba = im.convert("RGBA"); rgba.putalpha(Image.fromarray((m * 255).astype(np.uint8))); return rgba, m
def feet(m):
    ys, xs = np.nonzero(m); y0, y1 = ys.min(), ys.max(); band = m[int(y1 - (y1 - y0) * (fr if fr > 0 else 0.18)):y1 + 1]; bx = np.nonzero(band.any(0))[0]
    return bx.min(), bx.max(), y1
A, ma = cut(a_p); B, mb = cut(b_p)
ax0, ax1, ay = feet(ma); bx0, bx1, by = feet(mb); s = (ax1 - ax0) / max(1, bx1 - bx0)
def head(m):  # head width just under the top of the figure (stable between stances)
    ys, xs = np.nonzero(m); y0, y1 = ys.min(), ys.max()
    return max((lambda x: x.max() - x.min() if len(x) else 0)(np.nonzero(m[r])[0]) for r in range(y0, y0 + int((y1 - y0) * 0.35), 4))  # shoulder span
if fr < 0:  # mode "head": scale by head width (stance changes, head does not), floor + centre still matched
    s = head(ma) / max(1, head(mb)); ax0, ax1 = (lambda x: (x.min(), x.max()))(np.nonzero(ma.any(0))[0]); bx0, bx1 = (lambda x: (x.min(), x.max()))(np.nonzero(mb.any(0))[0])
Bs = B.resize((int(B.width * s), int(B.height * s)), Image.LANCZOS)
dx = (ax0 + ax1) / 2 - (bx0 + bx1) / 2 * s; dy = ay - by * s
canvas = (A.width + 400, A.height + 400); oA = Image.new("RGBA", canvas, (0, 0, 0, 0)); oB = Image.new("RGBA", canvas, (0, 0, 0, 0))
oA.alpha_composite(A, (200, 200)); oB.alpha_composite(Bs, (int(200 + dx), int(200 + dy)))
bb = oA.getbbox(); bb2 = oB.getbbox(); box = (min(bb[0], bb2[0]), min(bb[1], bb2[1]), max(bb[2], bb2[2]), max(bb[3], bb2[3]))
oA.crop(box).save(oa); oB.crop(box).save(ob); print(f"scale {s:.3f} shift {dx:.0f},{dy:.0f} -> {oA.crop(box).size}")
