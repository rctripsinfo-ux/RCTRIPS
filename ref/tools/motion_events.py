# Finds motion events (slides / pans / zooms of the main content) in every analysed video from frames.csv:
# runs of consecutive frames whose similarity-model motion is above a small threshold.
# Flat backgrounds mean "camera" = dominant tracked content (character/props); camera vs object can't be separated.
# usage: python3 -I ref/tools/motion_events.py <analysis_dir>   -> motion_events.csv + CAMERA_MOTION_RULES.json stats
import csv, json, os, statistics as st, sys
out = sys.argv[1]; ev = []
for vid in sorted(d for d in os.listdir(out) if d.startswith("R") and os.path.isdir(os.path.join(out, d))):
    rows = list(csv.DictReader(open(os.path.join(out, vid, "frames.csv"))))
    def mv(r):
        if not r.get("cam_scale"): return None
        return float(r["cam_tx"]), float(r["cam_ty"]), float(r["cam_scale"])
    run = []
    for r in rows + [{}]:
        m = mv(r)
        active = m and (abs(m[0]) > 0.002 or abs(m[1]) > 0.002 or abs(m[2] - 1) > 0.002)
        if active: run.append((float(r["t"]), m)); continue
        if len(run) >= 3:
            tx = sum(x[1][0] for x in run); ty = sum(x[1][1] for x in run); z = 1
            for x in run: z *= x[1][2]
            sp = [max(abs(x[1][0]), abs(x[1][1])) for x in run]; pk = sp.index(max(sp))
            kind = "zoom" if abs(z - 1) > max(abs(tx), abs(ty)) else ("slide_up" if ty < 0 and abs(ty) >= abs(tx) else
                   "slide_down" if ty > 0 and abs(ty) >= abs(tx) else "slide_left" if tx < 0 else "slide_right")
            ev.append({"video": vid, "start_s": run[0][0], "dur_s": round(run[-1][0] - run[0][0] + 1 / 30, 3), "kind": kind,
                       "travel_x": round(tx, 3), "travel_y": round(ty, 3), "zoom": round(z, 4),
                       "peak_at_frac": round(pk / max(1, len(run) - 1), 2),
                       "vel_profile": " ".join(f"{v:.3f}" for v in sp)})
        run = []
with open(os.path.join(out, "motion_events.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(ev[0])); w.writeheader(); w.writerows(ev)
stats = {}
for k in sorted({e["kind"] for e in ev}):
    E = [e for e in ev if e["kind"] == k]
    stats[k] = {"count": len(E), "dur_s_median": st.median(e["dur_s"] for e in E),
                "dur_s_p25_p75": [round(st.quantiles([e["dur_s"] for e in E], n=4)[0], 3), round(st.quantiles([e["dur_s"] for e in E], n=4)[2], 3)] if len(E) > 3 else None,
                "travel_median": st.median(abs(e["travel_y"]) if "up" in k or "down" in k else abs(e["travel_x"]) if "slide" in k else abs(e["zoom"] - 1) for e in E),
                "peak_at_frac_median": st.median(e["peak_at_frac"] for e in E),
                "per_video": {v: sum(e["video"] == v for e in E) for v in sorted({e["video"] for e in E})}}
json.dump({"source": "motion_events.py over frames.csv (LK+RANSAC similarity at 270x480, 30 fps)",
           "caveat": "first frame of a transition is often a cut frame (not tracked), so travel is a lower bound",
           "events": stats}, open(os.path.join(out, "motion_event_stats.json"), "w"), indent=1)
print(json.dumps(stats, indent=1))
