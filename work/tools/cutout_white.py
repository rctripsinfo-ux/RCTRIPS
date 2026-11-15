# usage: python3 tools/cutout_white.py in.png out.png -> removes the white background connected to the image border (keeps white inside the drawing)
import sys, numpy as np
from PIL import Image
from scipy import ndimage
im = Image.open(sys.argv[1]).convert("RGB"); a = np.asarray(im).astype(int)
white = (a.min(-1) > 238); lab, _ = ndimage.label(white); edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(edge)); alpha = np.where(bg, 0, 255).astype(np.uint8)
alpha = np.asarray(Image.fromarray(alpha).filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(1.2)))
out = im.convert("RGBA"); out.putalpha(Image.fromarray(alpha)); bb = out.getbbox(); out.crop(bb).save(sys.argv[2]); print(sys.argv[2], out.crop(bb).size)
