#!/usr/bin/env python3
"""Put the reference frame and our frame side by side at given timestamps.

Usage: side_by_side.py REF.mp4 OURS.mp4 --t 1.5 [--t2 1.5] --out cmp.png [--height 540]
--t2 is the timestamp in OURS (defaults to --t).
"""
import argparse, subprocess
import numpy as np
import cv2


def grab(path, t, height):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
                        "-vf", f"scale=-2:{height}", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True, check=True)
    return cv2.imdecode(np.frombuffer(r.stdout, np.uint8), cv2.IMREAD_COLOR)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ref")
    ap.add_argument("ours")
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--t2", type=float)
    ap.add_argument("--out", required=True)
    ap.add_argument("--height", type=int, default=540)
    a = ap.parse_args()
    imgs = [grab(a.ref, a.t, a.height), grab(a.ours, a.t if a.t2 is None else a.t2, a.height)]
    for im, label in zip(imgs, ("REFERENCE", "OURS")):
        cv2.putText(im, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.imwrite(a.out, np.hstack(imgs))
    print(a.out)


if __name__ == "__main__":
    main()
