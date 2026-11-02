# Same metrics on the reference material and on our video.
#  stills : reference frames (540x960) vs our frames at the same size -> colour, contrast, edges, detail, sharpness
#  motion : reference contact sheets (60 consecutive frames = 2 s, tiles 180x320) vs 2 s windows of our video at the
#           same tile size -> camera shift (phase correlation), frame activity (micro motion), cuts
# The caption band (58-78 % of the height) is masked in BOTH so burned-in captions do not pollute the statistics.
import sys, os, json, glob, subprocess, numpy as np
from PIL import Image
from scipy import ndimage
REF = "/home/user/RCTRIPS/.claude/skills/cartoon-3d-short/references"
def load(p, size=None):
    im = Image.open(p).convert("RGB")
    if size: im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(np.float32) / 255
def mask_rows(h): m = np.ones(h, bool); m[int(.58 * h):int(.78 * h)] = False; return m
def still_stats(a):
    rows = mask_rows(a.shape[0]); a = a[rows]
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    mx, mn = a.max(-1), a.min(-1); S = np.where(mx > 1e-3, (mx - mn) / np.maximum(mx, 1e-3), 0)
    rg = a[..., 0] - a[..., 1]; yb = 0.5 * (a[..., 0] + a[..., 1]) - a[..., 2]
    colorful = np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
    gx, gy = ndimage.sobel(L, 1), ndimage.sobel(L, 0); G = np.hypot(gx, gy)
    hf = L - ndimage.gaussian_filter(L, 2)
    lap = ndimage.laplace(L)
    ink = (L < 0.12).mean()
    return dict(lum_mean=L.mean(), lum_std=L.std(), p2=np.percentile(L, 2), p98=np.percentile(L, 98), sat=S.mean(), colorful=colorful,
                edge_frac=(G > 0.35).mean(), detail_hf=np.abs(hf).mean(), sharp_lapvar=lap.var(), dark_frac=ink)
def phasecorr(a, b):
    A, B = np.fft.fft2(a), np.fft.fft2(b); R = A * np.conj(B); R /= np.abs(R) + 1e-9
    r = np.fft.ifft2(R).real; y, x = np.unravel_index(np.argmax(r), r.shape); h, w = r.shape
    def sub(c, m, n):  # parabolic subpixel
        l, cc, rr = r[(c[0] - (m == 0)) % h, (c[1] - (m == 1)) % w], r[c], r[(c[0] + (m == 0)) % h, (c[1] + (m == 1)) % w]
        d = l - 2 * cc + rr; return 0 if abs(d) < 1e-9 else 0.5 * (l - rr) / d
    dy, dx = y + sub((y, x), 0, 0), x + sub((y, x), 1, 0)
    if dy > h / 2: dy -= h
    if dx > w / 2: dx -= w
    return dx, dy, r.max()
def pacing_stats(tiles):  # tiles ~1 s apart across a whole video: how often the picture is a NEW shot / framing
    win = np.outer(np.hanning(tiles[0].shape[0]), np.hanning(tiles[0].shape[1]))
    new, same = 0, 0
    for a, b in zip(tiles[:-1], tiles[1:]):
        d = np.abs(a - b).mean(); _, _, pk = phasecorr((a - a.mean()) * win, (b - b.mean()) * win)
        if d > 0.08 or pk < 0.08: new += 1
        else: same += 1
    return dict(new_picture_frac=new / (new + same), mean_tile_diff=float(np.mean([np.abs(a - b).mean() for a, b in zip(tiles[:-1], tiles[1:])])))
def motion_stats(tiles):  # tiles: list of HxW luma (180x320)
    win = np.outer(np.hanning(tiles[0].shape[0]), np.hanning(tiles[0].shape[1]))
    sp, act, cuts = [], [], 0
    for a, b in zip(tiles[:-1], tiles[1:]):
        d = np.abs(a - b).mean()
        if d > 0.12: cuts += 1; continue
        dx, dy, pk = phasecorr(a * win, b * win)
        sp.append(np.hypot(dx, dy) * 4)  # -> 720p pixels/frame
        act.append(d)
    sp = np.array(sp); act = np.array(act)
    return dict(move_frac=float((sp > 0.5).mean()), speed_med=float(np.median(sp)), speed_p90=float(np.percentile(sp, 90)),
                activity=float(np.median(act)), cuts_per_2s=cuts)
def sheet_tiles(p):
    a = load(p); L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    tiles = [L[r * 320:(r + 1) * 320, c * 180:(c + 1) * 180] for r in range(6) for c in range(10)]
    return [t[mask_rows(320)] for t in tiles]
def video_tiles(v, t0, n=60):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-i", v, "-frames:v", str(n), "-vf", "scale=180:320", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 320, 180, 3).astype(np.float32) / 255
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    return [x[mask_rows(320)] for x in L]
def agg(rows):
    keys = rows[0].keys(); return {k: [float(np.percentile([r[k] for r in rows], q)) for q in (25, 50, 75)] for k in keys}
if __name__ == "__main__":
    ours = sys.argv[1]; out = sys.argv[2]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ours], capture_output=True, text=True).stdout)
    ref_st = [still_stats(load(p, (540, 960))) for p in sorted(glob.glob(REF + "/frames/*.jpg"))]
    os.makedirs("/tmp/oursf", exist_ok=True)
    our_st = []
    for i, t in enumerate(np.linspace(1, dur - 1, 38)):
        f = f"/tmp/oursf/o_{i:02d}.png"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", ours, "-frames:v", "1", "-vf", "scale=540:960", f])
        our_st.append(still_stats(load(f)))
    ref_mo = [pacing_stats(sheet_tiles(p)) for p in sorted(glob.glob(REF + "/sheets/*.jpg"))]
    our_tiles = []
    for t in np.linspace(0.3, dur - 0.3, 60): our_tiles += video_tiles(ours, t, 1)
    our_mo = [pacing_stats(our_tiles)] * 3
    res = dict(ref_still=agg(ref_st), our_still=agg(our_st), ref_motion=agg(ref_mo), our_motion=agg(our_mo))
    json.dump(res, open(out, "w"), indent=1)
    for sec in ("still", "motion"):
        print(f"\n{sec:8s} {'metric':14s} {'REF p25/p50/p75':>26s} {'OURS p25/p50/p75':>26s}")
        for k in res["ref_" + sec]:
            r, o = res["ref_" + sec][k], res["our_" + sec][k]
            print(f"{'':8s} {k:14s} {r[0]:8.3f}{r[1]:8.3f}{r[2]:8.3f}  {o[0]:8.3f}{o[1]:8.3f}{o[2]:8.3f}")
