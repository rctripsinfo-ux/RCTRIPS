#!/usr/bin/env python3
"""Analyze a reference video: metadata, shot cuts/pacing, loudness, keyframes + contact sheet,
optional word transcript (caption pacing). Output: <out>/analysis.json, frames/, contact_sheet.jpg"""
import argparse, json, os, re, subprocess, sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    r = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]).stdout)
    v = next((s for s in r["streams"] if s["codec_type"] == "video"), {})
    num, den = (v.get("avg_frame_rate", "0/1").split("/") + ["1"])[:2]
    return {"duration": float(r["format"].get("duration", 0)), "width": v.get("width"), "height": v.get("height"),
            "fps": round(float(num) / float(den or 1), 2) if float(den or 1) else None,
            "has_audio": any(s["codec_type"] == "audio" for s in r["streams"])}


def scene_cuts(path, thr):
    err = run(["ffmpeg", "-hide_banner", "-i", path, "-filter:v", f"select='gt(scene,{thr})',showinfo",
               "-an", "-f", "null", "-"]).stderr
    return [round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", err)]


def loudness(path):
    err = run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"]).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--out", required=True)
    p.add_argument("--threshold", type=float, default=0.3, help="scene-change sensitivity (lower = more cuts)")
    p.add_argument("--every", type=float, default=1.0, help="also grab a frame every N seconds")
    p.add_argument("--transcribe", action="store_true")
    a = p.parse_args()
    fdir = os.path.join(a.out, "frames")
    os.makedirs(fdir, exist_ok=True)

    meta = probe(a.video)
    cuts = scene_cuts(a.video, a.threshold)
    shots = [b - x for x, b in zip([0] + cuts, cuts + [meta["duration"]]) if b - x > 0.05]

    # frames: every N sec (for animations/captions) + just after each cut
    times = sorted({round(t * a.every, 2) for t in range(int(meta["duration"] / a.every) + 1)} |
                   {round(min(c + 0.15, meta["duration"] - 0.05), 2) for c in cuts})
    times = [t for t in times if t < meta["duration"]][:120]
    for t in times:
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", a.video, "-frames:v", "1",
             "-vf", "scale=360:-2", os.path.join(fdir, f"t{t:07.2f}.jpg")])

    # contact sheet (6 columns), sampled evenly, max 36 tiles
    n = min(36, max(1, len(times)))
    rows = (n + 5) // 6
    fps_sample = n / max(meta["duration"], 0.1)
    sheet = os.path.join(a.out, "contact_sheet.jpg")
    run(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-vf",
         f"fps={fps_sample},scale=240:-2,drawtext=text='%{{pts\\:hms}}':x=4:y=4:fontsize=14:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x{rows}",
         "-frames:v", "1", sheet])

    res = {"file": a.video, **meta,
           "aspect": "9:16" if meta["height"] and meta["width"] and meta["height"] > meta["width"] else "16:9/other",
           "cuts": cuts, "num_shots": len(shots),
           "avg_shot_sec": round(sum(shots) / len(shots), 2) if shots else None,
           "cuts_per_10s": round(len(cuts) / max(meta["duration"], 0.1) * 10, 2),
           "loudness_lufs": loudness(a.video) if meta["has_audio"] else None,
           "frames_dir": fdir, "contact_sheet": sheet if os.path.exists(sheet) else None}

    if a.transcribe and meta["has_audio"]:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            from transcribe import transcribe
            tr = transcribe(a.video)
            w = tr["words"]
            res["language"] = tr["language"]
            res["words_per_sec"] = round(len(w) / max(meta["duration"], 0.1), 2)
            res["transcript"] = " ".join(x["w"] for x in w)
            res["words"] = w
        except Exception as e:
            res["transcript_error"] = str(e)[:200]

    json.dump(res, open(os.path.join(a.out, "analysis.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ("words", "transcript", "cuts")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
