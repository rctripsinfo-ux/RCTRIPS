# usage: python3 -I fx_detect.py in.mp4 out.json  -- per-frame metrics at 30 fps (360x640) + effect candidates
import cv2, json, sys, numpy as np
src, out = sys.argv[1:3]
cap = cv2.VideoCapture(src); fps = cap.get(5) or 30; step = max(1, round(fps / 30))
M = []; prev = None; ph = None; i = -1
while True:
    ok, f = cap.read(); i += 1
    if not ok: break
    if i % step: continue
    f = cv2.resize(f, (360, 640)); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    sat = (s > 110) & (v > 70)
    red = sat & ((h < 8) | (h > 170)); grn = sat & (h > 40) & (h < 85)
    border = np.concatenate([g[:60].ravel(), g[:, :30].ravel(), g[:, -30:].ravel()])
    lap = cv2.Laplacian(g, cv2.CV_32F)
    hist = cv2.calcHist([f], [0, 1, 2], None, [8, 8, 8], [0, 256] * 3); cv2.normalize(hist, hist)
    m = dict(t=round(i / fps, 3), luma=float(g.mean()), bg=float(np.median(border)), sharp=float(lap.var()),
             bsharp=float(np.concatenate([lap[:60].ravel(), lap[:, :30].ravel(), lap[:, -30:].ravel()]).var()),
             red=float(red.mean()), grn=float(grn.mean()), sat=float(sat.mean()))
    if prev is not None:
        d = np.abs(g - prev); m["d"] = float(d.mean()); mask = d > 25
        m["dfrac"] = float(mask.mean())
        if mask.sum() > 50:
            ys, xs = np.nonzero(mask); m["cx"], m["cy"] = float(xs.mean() / 360), float(ys.mean() / 640)
            m["bw"], m["bh"] = float((xs.max() - xs.min()) / 360), float((ys.max() - ys.min()) / 640)
        m["hc"] = float(cv2.compareHist(ph, hist, cv2.HISTCMP_CORREL))
        (sx, sy), resp = cv2.phaseCorrelate(prev, g); m["sx"], m["sy"], m["resp"] = float(sx), float(sy), float(resp)
    M.append(m); prev = g; ph = hist
json.dump(dict(fps=30, frames=M), open(out, "w")); print(out, len(M))
