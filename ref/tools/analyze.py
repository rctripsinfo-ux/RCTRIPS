# Phase 2: deterministic per-video measurements (no AI). Cached per video by sha1 + TOOL_VER.
# usage: python3 -I ref/tools/analyze.py <raw_dir> <analysis_dir> [video_id ...]
# Writes analysis/<id>/{frames.csv, shots.csv, audio.json, srt.json, summary.json} and sheets/<id>/wNN.jpg
# (consecutive 6 s windows at 2 fps, 12 tiles each), plus ANALYSIS_MANIFEST.json and SCENE_TIMELINE.csv.
import csv, json, os, re, subprocess, sys, wave
import cv2, numpy as np

TOOL_VER = "analyze-2"
AW, AH = 270, 480          # analysis size (keeps 9:16; flow + cuts)
raw, out = sys.argv[1:3]; only = set(sys.argv[3:])
inv = list(csv.DictReader(open(os.path.join(out, "REFERENCE_INVENTORY.csv"))))
man_p = os.path.join(out, "ANALYSIS_MANIFEST.json")
man = json.load(open(man_p)) if os.path.exists(man_p) else {"tool_version": TOOL_VER, "videos": {}}


def frames(path, w, h):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vf", f"scale={w}:{h}", "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)


def camera(prev_g, g):
    """Global similarity motion from sparse LK tracks: (tx, ty in canvas widths/heights per frame, scale, rot, inlier
    ratio, residual = median object motion after removing the camera model, px)."""
    pts = cv2.goodFeaturesToTrack(prev_g, 300, 0.01, 6)
    if pts is None or len(pts) < 12: return None
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_g, g, pts, None, winSize=(21, 21), maxLevel=3)
    ok = st.ravel() == 1
    a, b = pts[ok].reshape(-1, 2), nxt[ok].reshape(-1, 2)
    if len(a) < 12: return None
    M, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=1.0)
    if M is None: return None
    s = float(np.hypot(M[0, 0], M[1, 0])); r = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
    # translation of the frame centre (scale about the centre, not the corner)
    c = np.array([AW / 2, AH / 2]); tc = M[:, :2] @ c + M[:, 2] - c
    pred = a @ M[:, :2].T + M[:, 2]
    resid = float(np.median(np.linalg.norm(b - pred, axis=1)))
    return tc[0] / AW, tc[1] / AH, s, r, float(inl.mean()), resid, float(np.median(np.linalg.norm(b - a, axis=1)))


def analyze_video(row):
    vid, path = row["id"], os.path.join(raw, row["file"])
    vd = os.path.join(out, vid); sd = os.path.join(out, "sheets", vid); os.makedirs(vd, exist_ok=True); os.makedirs(sd, exist_ok=True)
    fps = float(row["fps"]); recs = []; prev = None; prev_hist = None; tiles = []
    for i, f in enumerate(frames(path, AW, AH)):
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY); hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [32, 16], [0, 180, 0, 256]); cv2.normalize(hist, hist)
        r = {"frame": i, "t": round(i / fps, 3), "bright": round(float(hsv[..., 2].mean()), 1),
             "contrast": round(float(g.std()), 1), "sat": round(float(hsv[..., 1].mean()), 1),
             "edges": round(float((cv2.Canny(g, 80, 160) > 0).mean()), 4)}
        if prev is not None:
            r["diff"] = round(float(cv2.absdiff(g, prev).mean()), 2)
            r["hist_corr"] = round(float(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)), 3)
            cm = camera(prev, g) if r["diff"] < 15 else None   # big content change = cut/slide frame, no camera model
            if cm and (cm[4] < 0.5 or abs(cm[2] - 1) > 0.08): cm = None  # unreliable fit (few inliers / absurd jump)
            if cm is None: r["transition"] = 1
            if cm: r.update(dict(zip(["cam_tx", "cam_ty", "cam_scale", "cam_rot", "cam_inliers", "obj_resid_px", "flow_med_px"],
                                     [round(x, 5) for x in cm])))
        recs.append(r); prev, prev_hist = g, hist
        if i % int(round(fps / 2)) == 0: tiles.append((r["t"], cv2.resize(f, (135, 240))))
    # contact sheets: 6 s windows, 2 fps -> 12 tiles (6x2)
    for w0 in range(0, len(tiles), 12):
        chunk = tiles[w0:w0 + 12]; sheet = np.full((2 * 260, 6 * 135, 3), 255, np.uint8)
        for k, (t, im) in enumerate(chunk):
            y, x = (k // 6) * 260, (k % 6) * 135; sheet[y:y + 240, x:x + 135] = im
            cv2.putText(sheet, f"{t:.1f}", (x + 3, y + 255), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.imwrite(os.path.join(sd, f"w{w0 // 12:02d}.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
    keys = sorted({k for r in recs for k in r}, key=lambda k: list(recs[-1]).index(k) if k in recs[-1] else 99)
    with open(os.path.join(vd, "frames.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(recs)

    # hard cuts: histogram break + big pixel change, at least 4 frames apart
    diffs = np.array([r.get("diff", 0) for r in recs]); corr = np.array([r.get("hist_corr", 1) for r in recs])
    med = np.median(diffs[1:]) if len(diffs) > 1 else 0
    cand = [i for i in range(1, len(recs)) if (corr[i] < 0.6 and diffs[i] > max(12, 4 * med)) or diffs[i] > max(35, 8 * med)]
    cuts = []
    for i in cand:
        if not cuts or i - cuts[-1] > 4: cuts.append(i)
    bounds = [0] + cuts + [len(recs)]
    shots = []
    for k in range(len(bounds) - 1):
        a, b = bounds[k], bounds[k + 1]; seg = recs[a + 1:b]
        sc = [r["cam_scale"] for r in seg if "cam_scale" in r]; tx = [r["cam_tx"] for r in seg if "cam_tx" in r]
        ty = [r["cam_ty"] for r in seg if "cam_ty" in r]; rs = [r["obj_resid_px"] for r in seg if "obj_resid_px" in r]
        zoom = float(np.prod(sc)) if sc else 1.0
        shots.append({"video": vid, "shot": k + 1, "start_f": a, "end_f": b - 1, "start_s": round(a / fps, 2),
                      "end_s": round((b - 1) / fps, 2), "dur_s": round((b - a) / fps, 2),
                      "zoom_total": round(zoom, 4), "pan_x_total": round(float(np.sum(tx)), 4), "pan_y_total": round(float(np.sum(ty)), 4),
                      "zoom_per_s": round((zoom ** (fps / max(1, len(sc))) - 1) if sc else 0, 4),
                      "obj_motion_med_px": round(float(np.median(rs)), 3) if rs else 0,
                      "mean_diff": round(float(np.mean([r.get("diff", 0) for r in seg])), 2) if seg else 0,
                      "confidence": "measured (LK+RANSAC similarity, 270x480)"})
    with open(os.path.join(vd, "shots.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(shots[0])); w.writeheader(); w.writerows(shots)

    # audio: 10 ms RMS, silences (< -35 dB under the 95th pct for >= 150 ms), onset candidates (energy rise peaks)
    wav = os.path.join(vd, "audio16k.wav")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", wav])
    with wave.open(wav) as wf: x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
    hop = 160; n = len(x) // hop
    rms = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1) + 1e-10); db = 20 * np.log10(rms)
    ref = np.percentile(db, 95); quiet = db < ref - 35
    sil = []; s0 = None
    for i, q in enumerate(np.append(quiet, False)):
        if q and s0 is None: s0 = i
        if not q and s0 is not None:
            if i - s0 >= 15: sil.append([round(s0 * 0.01, 2), round(i * 0.01, 2)])
            s0 = None
    rise = np.diff(db, prepend=db[0]); thr = np.percentile(rise, 99)
    on = [round(i * 0.01, 2) for i in range(1, n - 1) if rise[i] > thr and rise[i] >= rise[i - 1] and rise[i] >= rise[i + 1] and db[i] > ref - 20]
    onsets = []
    for t in on:
        if not onsets or t - onsets[-1] > 0.08: onsets.append(t)
    integ = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", integ); lra = re.findall(r"LRA:\s+([\d.]+) LU", integ)
    audio = {"lufs_integrated": float(m[-1]) if m else None, "lra": float(lra[-1]) if lra else None,
             "peak_db": round(float(db.max()), 1), "p95_db": round(float(ref), 1),
             "silences": sil, "silence_total_s": round(sum(b - a for a, b in sil), 2), "onset_candidates": onsets,
             "note": "onsets = sharp energy rises (sfx / plosives / music hits), not classified"}
    json.dump(audio, open(os.path.join(vd, "audio.json"), "w"))
    os.remove(wav)

    # SRT: words/min, segment lengths, speech-vs-SRT offset check
    srt = {}
    if row["srt"]:
        sp = os.path.join(raw, "script", row["srt"].split(" | ")[0]); txt = open(sp, encoding="utf-8", errors="ignore").read()
        cues = []
        for blk in re.split(r"\n\s*\n", txt.strip()):
            L = blk.strip().splitlines()
            tm = next((l for l in L if "-->" in l), None)
            if not tm: continue
            a, b = [sum(float(x) * m for x, m in zip(re.split("[:,]", t.strip())[:3], (3600, 60, 1))) + int(re.split("[:,]", t.strip())[3]) / 1000 for t in tm.split("-->")]
            text = " ".join(l for l in L[L.index(tm) + 1:]).strip()
            cues.append({"start": round(a, 3), "end": round(b, 3), "text": text})
        words = sum(len(c["text"].split()) for c in cues)
        span = (cues[-1]["end"] - cues[0]["start"]) if cues else 0
        full = " ".join(c["text"] for c in cues)
        sents = [s for s in re.split(r"(?<=[.!?])\s+", full) if s.strip()]
        srt = {"cues": cues, "words": words, "wpm": round(words / span * 60, 1) if span else None,
               "first_cue_s": cues[0]["start"] if cues else None, "text": full,
               "sentences_detected": len(sents), "note": "auto-generated captions: punctuation unreliable"}
    json.dump(srt, open(os.path.join(vd, "srt.json"), "w"), indent=1)

    cam = [r for r in recs if "cam_scale" in r]
    moving = [r for r in cam if abs(r["cam_scale"] - 1) > 0.0004 or abs(r["cam_tx"]) > 0.0004 or abs(r["cam_ty"]) > 0.0004]
    summ = {"video": vid, "frames": len(recs), "cuts": len(cuts), "shots": len(shots),
            "avg_shot_s": round(len(recs) / fps / len(shots), 2),
            "camera_moving_frac": round(len(moving) / max(1, len(cam)), 3),
            "zoom_in_frac": round(sum(r["cam_scale"] > 1.0004 for r in cam) / max(1, len(cam)), 3),
            "zoom_out_frac": round(sum(r["cam_scale"] < 0.9996 for r in cam) / max(1, len(cam)), 3),
            "changed_frac": round(float(np.mean(diffs[1:] > 1.0)), 3), "mean_diff": round(float(diffs[1:].mean()), 2),
            "bright_mean": round(float(np.mean([r["bright"] for r in recs])), 1),
            "sat_mean": round(float(np.mean([r["sat"] for r in recs])), 1),
            "contrast_mean": round(float(np.mean([r["contrast"] for r in recs])), 1),
            "edges_mean": round(float(np.mean([r["edges"] for r in recs])), 4),
            "lufs": audio["lufs_integrated"], "silence_total_s": audio["silence_total_s"], "onsets": len(onsets),
            "wpm": srt.get("wpm"), "words": srt.get("words")}
    json.dump(summ, open(os.path.join(vd, "summary.json"), "w"), indent=1)
    return summ, shots


timeline = []
for row in inv:
    vid = row["id"]
    if only and vid not in only: continue
    m = man["videos"].get(vid, {})
    if m.get("sha1") == row["sha1"] and m.get("ver") == TOOL_VER and os.path.exists(os.path.join(out, vid, "summary.json")):
        print(vid, "cached"); continue
    summ, shots = analyze_video(row)
    man["videos"][vid] = {"sha1": row["sha1"], "ver": TOOL_VER, "file": row["file"], "summary": summ}
    json.dump(man, open(man_p, "w"), indent=1)
    print(vid, json.dumps(summ))
for vid in sorted(man["videos"]):
    p = os.path.join(out, vid, "shots.csv")
    if os.path.exists(p): timeline += list(csv.DictReader(open(p)))
if timeline:
    with open(os.path.join(out, "SCENE_TIMELINE.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(timeline[0])); w.writeheader(); w.writerows(timeline)
