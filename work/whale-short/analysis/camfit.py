# Camera speed per frame, same classes as references/reports/motion.md: 3x3 tiles at 360x640 (tile bands avoid the
# caption zone), sub-pixel phase correlation per tile, least-squares fit of translation + zoom (+roll), speed =
# |translation| + |zoom| x 734 px (frame-corner radius at 720x1280), in 720p px/frame. Usage: camfit.py video.mp4
import sys, json, subprocess, numpy as np
V = sys.argv[1]; W, Hh = 360, 640
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-vf", f"scale={W}:{Hh},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, Hh, W).astype(np.float32) / 255
bands = [(0.03, 0.29), (0.29, 0.56), (0.80, 0.97)]; cols = [(0.0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.0)]
tiles = [(int(a * Hh), int(b * Hh), int(c * W), int(d * W)) for a, b in bands for c, d in cols]
def pc(a, b):
    w = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1])); A, B = np.fft.fft2(a * w), np.fft.fft2(b * w)
    R = A * np.conj(B); R /= np.abs(R) + 1e-9; r = np.fft.ifft2(R).real; y, x = np.unravel_index(r.argmax(), r.shape)
    def s(i, n, ax):
        l, c, rr = [r[(y + (d if ax == 0 else 0)) % r.shape[0], (x + (d if ax == 1 else 0)) % r.shape[1]] for d in (-1, 0, 1)]
        den = l - 2 * c + rr; o = 0.5 * (l - rr) / den if abs(den) > 1e-9 else 0; v = i + o; return v - n if v > n / 2 else v
    return s(y, r.shape[0], 0), s(x, r.shape[1], 1), r.max()
sp, cut = [], []
for i in range(1, len(F)):
    a, b = F[i - 1], F[i]
    if np.abs(a - b).mean() > 0.10: cut.append(i); sp.append(np.nan); continue
    rows = []
    for y0, y1, x0, x1 in tiles:
        dy, dx, q = pc(a[y0:y1, x0:x1], b[y0:y1, x0:x1])
        if q > 0.05: rows.append(((x0 + x1) / 2 - W / 2, (y0 + y1) / 2 - Hh / 2, dx, dy))
    if len(rows) < 4: sp.append(np.nan); continue
    r = np.array(rows); M = []; y = []
    for cx, cy, dx, dy in r: M += [[1, 0, cx, -cy], [0, 1, cy, cx]]; y += [dx, dy]
    p = np.linalg.lstsq(np.array(M), np.array(y), rcond=None)[0]
    sp.append(np.hypot(p[0], p[1]) * 2 + abs(p[2]) * 734)  # 360 -> 720 px
s = np.array(sp); v = s[~np.isnan(s)]
peaks = [i for i in range(1, len(s) - 1) if s[i] >= 6 and s[i] >= np.nan_to_num(s[i - 1]) and s[i] >= np.nan_to_num(s[i + 1])]
out = dict(frames=len(F), hold=round(float((v < 0.3).mean()), 3), drift=round(float(((v >= 0.3) & (v < 2)).mean()), 3), move=round(float((v >= 2).mean()), 3),
           median=round(float(np.median(v)), 2), p90=round(float(np.percentile(v, 90)), 2), moves_per_10s=round(len(peaks) / (len(F) / 300), 2),
           cuts=len(cut), mean_shot_s=round(len(F) / 30 / (len(cut) + 1), 2))
print(json.dumps(out)); json.dump(dict(summary=out, speed=[None if np.isnan(x) else round(float(x), 3) for x in s], cuts=cut), open(V.rsplit("/", 1)[-1] + ".cam.json", "w"))
