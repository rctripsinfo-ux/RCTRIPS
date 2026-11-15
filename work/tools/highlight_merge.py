# usage: python3 tools/highlight_merge.py base.png highlight.png out.png [mask_preview.png]
# Codex redraws the whole picture for a "muscle in red" variant, so take ONLY the red muscle from it:
# align the variant to the base (bounding box of the figure), keep pixels that are clearly red AND differ from the base,
# clean + feather that mask, paste onto the untouched base. The rest of the body stays pixel-identical -> clean blink.
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
base = Image.open(sys.argv[1]).convert("RGB"); hl = Image.open(sys.argv[2]).convert("RGB").resize(base.size, Image.LANCZOS)
def fig(im):
    a = np.asarray(im).astype(int); m = a.min(-1) < 235; ys, xs = np.nonzero(m); return xs.min(), ys.min(), xs.max(), ys.max()
bx0, by0, bx1, by1 = fig(base); hx0, hy0, hx1, hy1 = fig(hl); s = ((bx1 - bx0) / (hx1 - hx0) + (by1 - by0) / (hy1 - hy0)) / 2
hl2 = Image.new("RGB", base.size, "white"); t = hl.resize((int(hl.width * s), int(hl.height * s)), Image.LANCZOS)
hl2.paste(t, (int(bx0 - hx0 * s), int(by0 - hy0 * s)))
A, B = np.asarray(base).astype(int), np.asarray(hl2).astype(int)
red = (B[..., 0] - np.maximum(B[..., 1], B[..., 2]) > 45) & (B[..., 0] > 110)
diff = np.abs(A - B).sum(-1) > 60
G = int(sys.argv[5]) if len(sys.argv) > 5 else 4  # grow: larger when Codex moved the muscle outline a little
m = ndimage.binary_opening(red, iterations=2) & ndimage.binary_dilation(diff, iterations=3); m = ndimage.binary_closing(m, iterations=G); m = ndimage.binary_fill_holes(m)
if G > 4: m = ndimage.binary_dilation(m, iterations=G // 3)
lab, k = ndimage.label(m); sizes = ndimage.sum(m, lab, range(1, k + 1)) if k else []
keep = [i + 1 for i, v in enumerate(sizes) if v > m.size * 0.0015]; m = np.isin(lab, keep)
M = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
out = Image.composite(hl2, base, M); out.save(sys.argv[3]); print(sys.argv[3], f"scale {s:.3f}", f"muscle area {m.mean()*100:.2f}%")
if len(sys.argv) > 4: M.save(sys.argv[4])
