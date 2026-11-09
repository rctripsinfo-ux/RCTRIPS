#!/usr/bin/env python3
"""Compare our render's summary.json against a reference (REFERENCE_SET.json or one summary.json).

Prints every metric worst-first: reference, ours, delta, status. That list is the fix list.
Usage: compare.py REFERENCE.json OURS.json [--tol 0.10] [--md report.md]
"""
import argparse, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aggregate import flatten


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reference")
    ap.add_argument("ours")
    ap.add_argument("--tol", type=float, default=0.10, help="relative tolerance for single-reference compare")
    ap.add_argument("--md", help="also write a markdown report")
    a = ap.parse_args()
    ref = json.load(open(a.reference))
    ours = flatten(json.load(open(a.ours)))
    if ref.get("type") == "reference_set":
        rm = ref["metrics"]
    else:
        rm = {k: {"median": v, "p25": v, "p75": v} for k, v in flatten(ref).items()}
    rows = []
    for k, r in rm.items():
        if k not in ours or k in ("frames", "analysis_fps"):
            continue
        o, mid = ours[k], r["median"]
        lo, hi = r["p25"], r["p75"]
        tol = max(abs(mid) * a.tol, 1e-6)
        lo, hi = min(lo, mid - tol), max(hi, mid + tol)
        spread = max(hi - lo, 1e-6)
        dev = 0.0 if lo <= o <= hi else (o - hi if o > hi else o - lo) / spread
        rows.append((abs(dev), k, mid, o, o - mid, "OK" if dev == 0 else ("TOO HIGH" if dev > 0 else "TOO LOW")))
    rows.sort(reverse=True)
    head = f"{'metric':45} {'reference':>11} {'ours':>11} {'delta':>11}  status"
    lines = [head, "-" * len(head)]
    lines += [f"{k:45} {m:11.4g} {o:11.4g} {d:+11.4g}  {s}" for _, k, m, o, d, s in rows]
    bad = sum(1 for r in rows if r[5] != "OK")
    lines.append(f"\n{bad}/{len(rows)} metrics outside the reference range (worst first = fix first).")
    print("\n".join(lines))
    if a.md:
        with open(a.md, "w") as fh:
            fh.write("| metric | reference | ours | delta | status |\n|---|---|---|---|---|\n")
            for _, k, m, o, d, s in rows:
                fh.write(f"| {k} | {m:.4g} | {o:.4g} | {d:+.4g} | {s} |\n")


if __name__ == "__main__":
    main()
