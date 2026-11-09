#!/usr/bin/env python3
"""Measure a video's visual/audio style frame by frame.

Outputs (in --out):
  contact_sheets/sheet_XXXX.jpg  60 frames per 2 s grid (at 30 fps)
  frames.csv                     per-frame metrics
  summary.json                   aggregated metrics (feed to aggregate.py / compare.py)

Usage: analyze_video.py VIDEO --out DIR [--fps 30] [--width 480] [--no-sheets]
Note: cam_dx/dy are IMAGE shifts (content moving left = camera panning right).
"""
import argparse, csv, json, os, re, subprocess, sys
import numpy as np
import cv2


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,r_frame_rate:format=duration",
                          "-of", "json", path], capture_output=True, text=True, check=True)
    info = json.loads(out.stdout)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {"width": int(v["width"]), "height": int(v["height"]),
            "native_fps": float(num) / float(den or 1),
            "duration": float(info["format"].get("duration", 0)),
            "has_audio": any(s["codec_type"] == "audio" for s in info["streams"])}


def frames(path, fps, w, h):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    size = w * h * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    p.wait()


def loudness(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-filter_complex",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary:"):]
    g = lambda k: (lambda m: float(m.group(1)) if m else None)(re.search(k + r":\s+(-?[\d.]+|-inf)", s))
    try:
        return {"integrated_lufs": g("I"), "loudness_range_lu": g("LRA"), "true_peak_dbfs": g("Peak")}
    except ValueError:
        return {}


class Motion:
    """Camera translation + zoom + roll between two grayscale frames.

    Translation: full-frame phase correlation. Zoom/roll: phase-correlate a grid of
    textured blocks after removing the translation, robust least-squares fit of a
    similarity transform, refined iteratively (warp by estimate, measure residual).
    Validated on synthetic footage: static ~0, pans and zooms down to 0.1%/frame within ~10%.
    """
    def __init__(self, h, w, n=5, iters=3, min_std=6.0, min_resp=0.1):
        self.h, self.w, self.iters, self.min_std, self.min_resp = h, w, iters, min_std, min_resp
        bh, bw = h // n, w // n
        self.blocks = [(y * bh, x * bw, bh, bw) for y in range(n) for x in range(n)]
        self.bwin = cv2.createHanningWindow((bw, bh), cv2.CV_32F)
        self.win = cv2.createHanningWindow((w, h), cv2.CV_32F)
        self.cx, self.cy = w / 2, h / 2

    def _warp(self, g, tx, ty, k, rot):
        s, cx, cy = 1 + k, self.cx, self.cy
        M = np.float32([[s, -rot, (1 - s) * cx + rot * cy + tx], [rot, s, (1 - s) * cy - rot * cx + ty]])
        return cv2.warpAffine(g, M, (self.w, self.h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    def _blocks(self, g0, g1):
        pts = []
        for y, x, bh, bw in self.blocks:
            b0, b1 = g0[y:y + bh, x:x + bw], g1[y:y + bh, x:x + bw]
            if b0.std() < self.min_std or b1.std() < self.min_std:
                continue
            (dx, dy), r = cv2.phaseCorrelate(b0, b1, self.bwin)
            if r >= self.min_resp:
                pts.append((x + bw / 2 - self.cx, y + bh / 2 - self.cy, dx, dy, r))
        return np.array(pts)

    @staticmethod
    def _fit(p):
        # model: d = t + k*p + rot*perp(p); solve for k, rot (t already removed, kept as free term)
        A = np.zeros((2 * len(p), 4)); b = np.zeros(2 * len(p))
        A[0::2] = np.c_[np.ones(len(p)), np.zeros(len(p)), p[:, 0], -p[:, 1]]
        A[1::2] = np.c_[np.zeros(len(p)), np.ones(len(p)), p[:, 1], p[:, 0]]
        b[0::2], b[1::2] = p[:, 2], p[:, 3]
        wt = np.repeat(np.sqrt(p[:, 4]), 2)
        sol = np.linalg.lstsq(A * wt[:, None], b * wt, rcond=None)[0]
        res = np.hypot(*(A @ sol - b).reshape(-1, 2).T)
        return sol, res

    def __call__(self, g0, g1):
        (tx, ty), resp = cv2.phaseCorrelate(g0, g1, self.win)
        k = rot = 0.0
        for _ in range(self.iters):
            p = self._blocks(self._warp(g0, tx, ty, k, rot), g1)
            if len(p) < 4:
                break
            sol, res = self._fit(p)
            keep = res <= max(np.percentile(res, 75), 0.05)
            if keep.sum() >= 4:
                sol, _ = self._fit(p[keep])
            tx += sol[0]; ty += sol[1]; k += sol[2]; rot += sol[3]
        return float(tx), float(ty), float(np.log1p(k)), float(rot), float(resp)


def hist(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h = cv2.calcHist([hsv], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
    return cv2.normalize(h, h).flatten()


def sharp(g):
    return float(cv2.Laplacian(g, cv2.CV_32F).var())


def frame_metrics(rgb):
    f = rgb.astype(np.float32)
    luma = 0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    g8 = luma.astype(np.uint8)
    h, w = g8.shape
    ch, cw = h // 4, w // 4
    center = sharp(g8[ch:h - ch, cw:w - cw])
    border_sharp = sharp(np.concatenate([g8[:ch], g8[h - ch:]]))
    lo, hi = np.percentile(luma, [25, 75])
    shadow = f[luma <= lo].mean(0)
    highlight = f[luma >= hi].mean(0)
    edges = cv2.Canny(g8, 80, 160)
    return {
        "luma_mean": float(luma.mean()), "contrast_std": float(luma.std()),
        "luma_p1": float(np.percentile(luma, 1)), "luma_p99": float(np.percentile(luma, 99)),
        "clip_black_pct": float((luma < 5).mean() * 100), "clip_white_pct": float((luma > 250).mean() * 100),
        "saturation_mean": float(hsv[..., 1].mean()),
        "r_mean": float(f[..., 0].mean()), "g_mean": float(f[..., 1].mean()), "b_mean": float(f[..., 2].mean()),
        "warmth_r_minus_b": float((f[..., 0] - f[..., 2]).mean()),
        "shadow_r": float(shadow[0]), "shadow_g": float(shadow[1]), "shadow_b": float(shadow[2]),
        "highlight_r": float(highlight[0]), "highlight_g": float(highlight[1]), "highlight_b": float(highlight[2]),
        "sharpness": sharp(g8), "center_to_border_sharpness": float(center / (border_sharp + 1e-6)),
        "edge_density_pct": float((edges > 0).mean() * 100),
    }


def ease_frames(speed, start, end, thresh):
    """For each continuous move in a shot, frames to reach / leave 80% of its (p90) peak speed."""
    ins, outs, i = [], [], start
    while i < end:
        if speed[i] > thresh:
            j = i
            while j < end and speed[j] > thresh:
                j += 1
            seg = speed[i:j]
            if len(seg) >= 3:
                pk = np.percentile(seg, 90) * 0.8  # robust to noisy single-frame peaks
                ins.append(int(np.argmax(seg >= pk)))
                outs.append(int(len(seg) - 1 - np.max(np.nonzero(seg >= pk))))
            i = j
        else:
            i += 1
    return ins, outs


def smooth(v, k=5):
    """Median then mean filter: removes per-frame estimator noise, keeps real (smooth) camera moves."""
    if len(v) < k:
        return v
    pad = k // 2
    vp = np.pad(v, pad, mode="edge")
    m = np.array([np.median(vp[i:i + k]) for i in range(len(v))])
    return np.convolve(np.pad(m, pad, mode="edge"), np.ones(k) / k, "valid")


def med(x):
    return float(np.median(x)) if len(x) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--width", type=int, default=480)
    ap.add_argument("--cut-thresh", type=float, default=0.45, help="histogram distance for a hard cut")
    ap.add_argument("--cut-resp", type=float, default=0.03, help="phase response below this (+small hist change) = cut")
    ap.add_argument("--motion-thresh", type=float, default=0.0005,
                    help="per-frame motion (fraction of width, or log-zoom per frame) counted as 'moving'")
    ap.add_argument("--span", type=int, default=10, help="frame span for slow-motion detection")
    ap.add_argument("--no-sheets", action="store_true")
    a = ap.parse_args()

    info = probe(a.video)
    w = a.width - a.width % 2
    h = int(round(info["height"] * w / info["width"])) // 2 * 2
    os.makedirs(a.out, exist_ok=True)
    sheet_dir = os.path.join(a.out, "contact_sheets")
    if not a.no_sheets:
        os.makedirs(sheet_dir, exist_ok=True)

    mot = Motion(h, w)
    per_sheet = int(round(a.fps * 2))
    cols = 10
    tw, th = 160, int(160 * h / w)
    sheet, rows, prev, hist_prev = [], [], None, None
    ring = []  # last `span` gray frames, reset on cuts
    sheet_no = 0

    def flush_sheet():
        nonlocal sheet, sheet_no
        if not sheet or a.no_sheets:
            sheet = []
            return
        r = (len(sheet) + cols - 1) // cols
        grid = np.zeros((r * th, cols * tw, 3), np.uint8)
        for k, im in enumerate(sheet):
            y, x = divmod(k, cols)
            grid[y * th:(y + 1) * th, x * tw:(x + 1) * tw] = im
        t0 = sheet_no * 2
        cv2.putText(grid, f"{t0:.0f}-{t0 + 2:.0f}s", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.imwrite(os.path.join(sheet_dir, f"sheet_{sheet_no:04d}.jpg"), cv2.cvtColor(grid, cv2.COLOR_RGB2BGR))
        sheet_no += 1
        sheet = []

    for i, rgb in enumerate(frames(a.video, a.fps, w, h)):
        m = {"frame": i, "time_s": round(i / a.fps, 4)}
        m.update(frame_metrics(rgb))
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
        hs = hist(rgb)
        cut_score = 0.0 if hist_prev is None else float(1 - cv2.compareHist(hist_prev, hs, cv2.HISTCMP_CORREL))
        dx = dy = dz = rot = 0.0
        resp = 1.0
        if prev is not None:
            dx, dy, dz, rot, resp = mot(prev, gray)
        # hard cut: colour distribution jumps, OR image stops correlating (cut between similar-looking shots)
        is_cut = i > 0 and (cut_score > a.cut_thresh or (resp < a.cut_resp and cut_score > 0.03))
        if is_cut:
            dx = dy = dz = rot = 0.0
            ring = []
        span_speed = None
        if len(ring) >= a.span:
            sdx, sdy, sdz, _, _ = mot(ring[-a.span], gray)
            span_speed = max(np.hypot(sdx, sdy) / w, abs(sdz)) / a.span
        ring.append(gray)
        ring = ring[-a.span:]
        m.update({"cam_dx_px": dx, "cam_dy_px": dy, "cam_logzoom": dz, "cam_roll_rad": rot,
                  "phase_response": resp, "cut_score": cut_score, "is_cut": int(is_cut),
                  "slow_motion_speed": span_speed if span_speed is not None else ""})
        rows.append(m)
        prev, hist_prev = gray, hs
        if not a.no_sheets:
            sheet.append(cv2.resize(rgb, (tw, th), interpolation=cv2.INTER_AREA))
            if len(sheet) == per_sheet:
                flush_sheet()
    flush_sheet()
    if not rows:
        sys.exit("no frames decoded")

    with open(os.path.join(a.out, "frames.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)

    n = len(rows)
    col = lambda k: np.array([r[k] for r in rows], float)
    cuts = [r["frame"] for r in rows if r["is_cut"]]
    bounds = [0] + cuts + [n]
    # smooth each motion channel within shots (never across cuts) before computing stats
    dx, dy, dz, rl = (col(k) for k in ("cam_dx_px", "cam_dy_px", "cam_logzoom", "cam_roll_rad"))
    dx, dy = dx / w, dy / w
    for arr in (dx, dy, dz, rl):
        for s, e in zip(bounds[:-1], bounds[1:]):
            if e - s > 1:
                arr[s + 1:e] = smooth(arr[s + 1:e])
    speed = np.maximum(np.hypot(dx, dy), np.abs(dz))
    shots, jerks, ins, outs = [], [], [], []
    for s, e in zip(bounds[:-1], bounds[1:]):
        shots.append({"start_s": round(s / a.fps, 3), "duration_s": round((e - s) / a.fps, 3)})
        if e - s > 4:
            for comp in (dx[s + 1:e], dy[s + 1:e], dz[s + 1:e]):
                pos = np.cumsum(comp)
                jerks.append(np.abs(np.diff(pos, 3)).mean() * a.fps ** 3 if len(pos) > 3 else 0)
        i_, o_ = ease_frames(speed, s + 1, e, a.motion_thresh)
        ins += i_
        outs += o_
    slow = np.array([r["slow_motion_speed"] for r in rows if r["slow_motion_speed"] != ""], float)
    tot = np.abs(dx).sum() + np.abs(dy).sum() + np.abs(dz).sum() + 1e-12
    summary = {
        "video": os.path.abspath(a.video), "source": info, "analysis_fps": a.fps, "frames": n,
        "camera": {
            # primary: motion measured across `span` frames (codec noise / span); catches slow creeps
            "pct_frames_moving": float((slow > a.motion_thresh / 4).mean() * 100) if len(slow) else None,
            "pct_frames_moving_per_frame": float((speed > a.motion_thresh).mean() * 100),
            "share_pan_x": float(np.abs(dx).sum() / tot), "share_tilt_y": float(np.abs(dy).sum() / tot),
            "share_zoom_dolly": float(np.abs(dz).sum() / tot),
            "pct_frames_zoom_in": float((dz > a.motion_thresh).mean() * 100), "pct_frames_zoom_out": float((dz < -a.motion_thresh).mean() * 100),
            "mean_speed": float(speed.mean()), "p95_speed": float(np.percentile(speed, 95)),
            "mean_jerk": float(np.mean(jerks)) if jerks else None,
            "median_ease_in_frames": med(ins), "median_ease_out_frames": med(outs),
            "low_confidence_pct": float((col("phase_response") < 0.05).mean() * 100),
            "share_roll": float(np.abs(rl).sum() / (tot + np.abs(rl).sum())),
        },
        "edit": {
            "hard_cuts": len(cuts), "cuts_per_min": len(cuts) / (n / a.fps) * 60,
            "median_shot_s": med([s["duration_s"] for s in shots]), "shots": shots,
        },
        "look": {k: float(col(k).mean()) for k in (
            "luma_mean", "contrast_std", "luma_p1", "luma_p99", "clip_black_pct", "clip_white_pct",
            "saturation_mean", "r_mean", "g_mean", "b_mean", "warmth_r_minus_b",
            "shadow_r", "shadow_g", "shadow_b", "highlight_r", "highlight_g", "highlight_b",
            "sharpness", "center_to_border_sharpness", "edge_density_pct")},
        "look_variation": {"luma_std_over_time": float(col("luma_mean").std()),
                           "warmth_std_over_time": float(col("warmth_r_minus_b").std())},
        "audio": loudness(a.video) if info["has_audio"] else {},
    }
    with open(os.path.join(a.out, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"{n} frames, {len(cuts)} cuts, {sheet_no} contact sheets -> {a.out}")


if __name__ == "__main__":
    main()
