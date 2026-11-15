import json, sys, statistics as st
def events(path):
    R = json.load(open(path))["frames"]; n = len(R); ev = []; i = 1
    while i < n:
        if R[i]["diff"] > 0.5:
            j = i
            while j + 1 < n and R[j + 1]["diff"] > 0.5: j += 1
            a, b = R[i - 1], R[j]; dur = j - i + 1; peak = max(R[k]["diff"] for k in range(i, j + 1))
            A, B = a.get("area", 0), b.get("area", 0)
            dx = (b.get("cx", 0.5) - a.get("cx", 0.5)) if A and B else 0; dy = (b.get("cy", 0.5) - a.get("cy", 0.5)) if A and B else 0
            ha = (a["y1"] - a["y0"]) if A else 0; hb = (b["y1"] - b["y0"]) if B else 0
            # velocity profile of the centre over the run
            path = [R[k].get("cx", 0) for k in range(i - 1, j + 1)] if A and B else []
            prof = ""
            if len(path) > 4 and abs(dx) > 0.05:
                half = len(path) // 2; first = abs(path[half] - path[0]); tot = abs(path[-1] - path[0]) or 1
                over = max(abs(p - path[0]) for p in path) > tot * 1.08
                prof = ("ease-out" if first / tot > 0.65 else "ease-in" if first / tot < 0.35 else "linear/ease-in-out") + (" +overshoot" if over else "")
            if dur <= 2 and peak > 12: kind = "cut/swap"
            elif not A or not B: kind = "enter" if not A else "exit"
            elif abs(dx) > 0.08 or abs(dy) > 0.08: kind = "slide/move"
            elif ha and hb and (max(ha, hb) / max(1e-3, min(ha, hb)) > 1.15): kind = "scale/zoom"
            elif dur >= 4 and abs(B - A) / max(A, 1e-3) > 0.25: kind = "fade/grow-layer"
            elif dur >= 8 and peak < 4: kind = "idle/shiver"
            else: kind = "small change"
            ev.append(dict(t=round(R[i]["t"], 2), frames=dur, ms=round(dur / 30 * 1000), kind=kind, peak=round(peak, 1), dx=round(dx, 3), dy=round(dy, 3),
                           size=round(hb / ha, 2) if ha and hb else None, profile=prof))
            i = j + 1
        else: i += 1
    holds = []; run = 0
    for r in R[1:]:
        if r["diff"] <= 0.5: run += 1
        else:
            if run: holds.append(run)
            run = 0
    return ev, holds, n
allk = {}
for v in sys.argv[1:]:
    ev, holds, n = events(v); name = v.split("/")[-1][:3]
    ks = {}
    for e in ev: ks.setdefault(e["kind"], []).append(e)
    print(f"\n## {name}: {n} frames, {len(ev)} change events, still frames {sum(holds)/n*100:.0f}%, median hold {st.median(holds)/30:.2f}s, longest hold {max(holds)/30:.1f}s")
    for k, L in sorted(ks.items(), key=lambda x: -len(x[1])):
        allk.setdefault(k, []).extend(L)
        prof = [e["profile"] for e in L if e["profile"]]
        print(f"  {k:16} x{len(L):3}  median {st.median([e['frames'] for e in L]):.0f} frames ({st.median([e['ms'] for e in L]):.0f} ms)" + (f"  curves: {dict((p, prof.count(p)) for p in set(prof))}" if prof else ""))
    json.dump(ev, open(v.replace(".track30.json", ".events30.json"), "w"), indent=0)
print("\n## ALL 6 SHORTS")
for k, L in sorted(allk.items(), key=lambda x: -len(x[1])):
    fr = sorted(e["frames"] for e in L)
    print(f"  {k:16} x{len(L):3}  frames: median {st.median(fr):.0f}, 25-75% {fr[len(fr)//4]}-{fr[3*len(fr)//4]}")
sl = [e for e in allk.get("slide/move", []) if e["profile"]]
print("  slide curves:", {p: [e["profile"] for e in sl].count(p) for p in set(e["profile"] for e in sl)})
sz = [e["size"] for e in allk.get("scale/zoom", []) if e["size"]]
print("  zoom size ratios:", sorted(sz))
