# Removes white left behind by the cutout: enclosed white holes (e.g. between an arm and a leg) and the thin
# white fringe on the outline. The white "H" and the eyes are kept (anything near the face is left alone).
# usage: python3 clean_cutout.py hero_sad_floor [more ids]   (edits ~/reel-engine-tool/public/library/hero/<id>.webp)
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
LIB = os.path.expanduser("~/reel-engine-tool/public/library/hero")
A = {a["id"]: a for a in json.load(open(f"{LIB}/library.json"))["assets"]}
for aid in sys.argv[1:]:
    p = f"{LIB}/{aid}.webp"; im = np.asarray(Image.open(p).convert("RGBA")).copy(); h, w = im.shape[:2]
    rgb, a = im[..., :3].astype(int), im[..., 3]
    white = (rgb.min(-1) > 215) & (a > 0)
    nose = A.get(aid, {}).get("points", {}).get("nose")
    lab, n = ndimage.label(white); removed = 0
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab[sl] == i; area = int(m.sum())
        if area < 120: continue
        cy = (sl[0].start + sl[0].stop) / 2 / h; cx = (sl[1].start + sl[1].stop) / 2 / w
        if nose and abs(cy - nose[1]) < 0.09 and abs(cx - nose[0]) < 0.15: continue  # H letter / eyes
        im[sl][..., 3][m] = 0; removed += area
    a = im[..., 3]; edge = (a > 0) & ndimage.binary_dilation(a == 0, iterations=2)
    fringe = edge & (im[..., :3].min(-1) > 200); im[..., 3][fringe] = 0
    Image.fromarray(im).save(p, "WEBP", quality=90)
    print(aid, "holes removed px:", removed, "fringe px:", int(fringe.sum()))
