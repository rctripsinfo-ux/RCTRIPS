# per 0.5 s: foreground (non-set) bbox height / width share, number of separate objects, biggest object share; set colour estimated per frame from the corners
import cv2, glob, json, sys, numpy as np
from scipy import ndimage
res = {}
for f in sorted(glob.glob("comp2/v*.mp4")):
    cap = cv2.VideoCapture(f); fps = cap.get(5); n = int(cap.get(7)); R = []
    for i in range(0, n, int(fps / 2)):
        cap.set(1, i); ok, fr = cap.read()
        if not ok: break
        fr = cv2.resize(fr, (180, 320)).astype(np.int16)
        corners = np.concatenate([fr[:6, :6].reshape(-1, 3), fr[:6, -6:].reshape(-1, 3)]); bg = np.median(corners, 0)
        m = np.abs(fr - bg).sum(-1) > 40
        m = ndimage.binary_opening(m, iterations=1); lab, k = ndimage.label(m)
        if k == 0: R.append((0, 0, 0, 0)); continue
        sizes = ndimage.sum(m, lab, range(1, k + 1)); big = sizes.max() / m.size; objs = int((sizes > m.size * 0.004).sum())
        ys, xs = np.nonzero(lab == (np.argmax(sizes) + 1)); R.append((float((ys.max() - ys.min()) / 320), float((xs.max() - xs.min()) / 180), float(big), objs))
    res[f.split("/")[-1][:3]] = R
json.dump(res, open("comp2/framing.json", "w"))
A = np.array([r for v in res.values() for r in v]); A = A[A[:, 0] > 0]
h = A[:, 0]; print("frames", len(A))
print("main-object height share: median %.2f | p25 %.2f | p75 %.2f" % tuple(np.percentile(h, [50, 25, 75])))
for lo, hi, name in ((0, .45, "small <45%"), (.45, .7, "medium 45-70%"), (.7, .9, "big 70-90%"), (.9, 1.01, "fills frame >90% (close-up)")): print(f"  {name:28s} {((h >= lo) & (h < hi)).mean()*100:5.1f}%")
print("main object area share median %.2f" % np.median(A[:, 2]))
print("separate objects per frame: median %d | p75 %d | share with <=2 objects %.0f%%" % (np.median(A[:, 3]), np.percentile(A[:, 3], 75), (A[:, 3] <= 2).mean() * 100))
