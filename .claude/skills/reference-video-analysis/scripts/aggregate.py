#!/usr/bin/env python3
"""Aggregate many summary.json files (one per reference) into a reference-set profile.

Usage: aggregate.py DIR_OR_SUMMARY [...] --out REFERENCE_SET.json
Each numeric metric gets median / p25 / p75 / min / max / n.
"""
import argparse, json, os
import numpy as np


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict) and k != "source":
            out.update(flatten(v, key + "."))
        elif isinstance(v, (int, float)) and not isinstance(v, bool) and v is not None:
            out[key] = float(v)
    return out


def load(p):
    if os.path.isdir(p):
        p = os.path.join(p, "summary.json")
    with open(p) as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    flats = [flatten(load(p)) for p in a.inputs]
    keys = sorted({k for f in flats for k in f if k not in ("frames", "analysis_fps")})
    prof = {}
    for k in keys:
        v = np.array([f[k] for f in flats if k in f and np.isfinite(f[k])])
        if len(v):
            prof[k] = {"median": float(np.median(v)), "p25": float(np.percentile(v, 25)),
                       "p75": float(np.percentile(v, 75)), "min": float(v.min()), "max": float(v.max()), "n": len(v)}
    with open(a.out, "w") as fh:
        json.dump({"type": "reference_set", "count": len(flats), "inputs": a.inputs, "metrics": prof}, fh, indent=2)
    print(f"{len(flats)} videos, {len(prof)} metrics -> {a.out}")


if __name__ == "__main__":
    main()
