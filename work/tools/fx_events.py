# usage: python3 -I fx_events.py fx/*.json -> fx_events.json + printed stats (dim, blur, blink, wipe, flash, shake, cut, pan)
import json, sys, numpy as np
ALL = {}
def runs(mask, minlen):
    r = []; s = None
    for k, v in enumerate(list(mask) + [False]):
        if v and s is None: s = k
        if not v and s is not None:
            if k - s >= minlen: r.append((s, k - 1))
            s = None
    return r
for p in sys.argv[1:]:
    F = json.load(open(p))["frames"]; n = len(F); vid = p.split("/")[-1][:3]; E = []
    t = np.array([f["t"] for f in F]); bg = np.array([f["bg"] for f in F]); lu = np.array([f["luma"] for f in F])
    bs = np.array([f["bsharp"] for f in F]); hc = np.array([f.get("hc", 1) for f in F])
    red = np.array([f["red"] for f in F]); grn = np.array([f["grn"] for f in F])
    cuts = [k for k in range(1, n) if hc[k] < 0.5]
    for k in cuts: E.append(dict(kind="cut", t=t[k], f=1))
    seg = [0] + cuts + [n]                       # analyse dim/blur inside shots only (cuts change everything)
    for a, b in zip(seg[:-1], seg[1:]):
        if b - a < 10: continue
        base_bg = np.median(bg[a:a + 6]); base_bs = np.median(bs[a:a + 6])
        ref = np.array([np.median(bg[max(a, k - 20):k]) if k - a >= 6 else base_bg for k in range(a, b)])
        refs = np.array([np.median(bs[max(a, k - 20):k]) if k - a >= 6 else base_bs for k in range(a, b)])
        dim = (bg[a:b] < ref * 0.85) & (ref > 40)
        for s, e in runs(dim, 6):
            s0 = s + a; ramp = 0
            while s0 + ramp + 1 < b and bg[s0 + ramp + 1] < bg[s0 + ramp] - 0.5: ramp += 1
            E.append(dict(kind="dim", t=t[s0], f=e - s + 1, depth=round(1 - bg[s0 + ramp] / ref[s], 2), ramp=ramp + 1))
        bl = (bs[a:b] < refs * 0.4) & (np.abs(bg[a:b] - ref) < ref * 0.2) & (refs > 20)
        for s, e in runs(bl, 6): E.append(dict(kind="bg_blur", t=t[s + a], f=e - s + 1, drop=round(1 - bs[s + a] / refs[s], 2)))
    for k in range(1, n - 6):                    # flash: luma spike up and back
        if lu[k] > lu[k - 1] * 1.25 and min(lu[k + 1:k + 7]) < lu[k] * 0.85: E.append(dict(kind="flash", t=t[k], f=int(np.argmin(lu[k + 1:k + 7])) + 1))
    for name, s_ in (("red", red), ("green", grn)):   # highlight appear + blink count
        on = s_ > 0.004
        for s, e in runs(on, 4):
            w = s_[max(0, s - 2):min(n, s + 45)]; pk = 0; up = False; mx = w.max()
            for v in w:
                if not up and v > mx * 0.6: up = True; pk += 1
                if up and v < mx * 0.25: up = False
            E.append(dict(kind=f"{name}_highlight", t=t[s], f=e - s + 1, area=round(float(s_[s:e + 1].max()) * 100, 2), blinks=pk))
    k = 1                                        # wipes: big band of change sweeping one way
    while k < n - 3:
        f0 = F[k]
        if f0.get("dfrac", 0) > 0.12 and "cy" in f0 and hc[k] > 0.5:
            j = k; xs = [f0["cx"]]; ys = [f0["cy"]]
            while j + 1 < n and F[j + 1].get("dfrac", 0) > 0.08 and "cy" in F[j + 1]: j += 1; xs.append(F[j]["cx"]); ys.append(F[j]["cy"])
            if j - k >= 2:
                dx, dy = xs[-1] - xs[0], ys[-1] - ys[0]
                if max(abs(dx), abs(dy)) > 0.25 and (np.all(np.diff(xs if abs(dx) > abs(dy) else ys) * np.sign(dx if abs(dx) > abs(dy) else dy) > -0.03)):
                    E.append(dict(kind="wipe", t=t[k], f=j - k + 1, dir=("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")))
            k = j + 1
        else: k += 1
    sh = [k for k in range(2, n) if F[k].get("resp", 0) > 0.25 and F[k - 1].get("resp", 0) > 0.25 and
          abs(F[k].get("sx", 0)) + abs(F[k].get("sy", 0)) > 1.5 and np.sign(F[k]["sx"] + F[k]["sy"]) != np.sign(F[k - 1]["sx"] + F[k - 1]["sy"])]
    for s, e in runs([k in set(sh) for k in range(n)], 2): E.append(dict(kind="shake", t=t[s], f=e - s + 1))
    E.sort(key=lambda e: e["t"]); ALL[vid] = dict(dur=float(t[-1]), events=E)
json.dump(ALL, open("comp2/fx_events.json", "w"), default=float)
from collections import Counter, defaultdict
C = Counter(); V = defaultdict(set); D = defaultdict(list)
for v, x in ALL.items():
    for e in x["events"]: C[e["kind"]] += 1; V[e["kind"]].add(v); D[e["kind"]].append(e)
tot = sum(x["dur"] for x in ALL.values())
print(f"{len(ALL)} videos, {tot/60:.1f} min")
for k, c in C.most_common():
    fr = [e["f"] for e in D[k]]; extra = ""
    if k == "dim": extra = f" depth med {np.median([e['depth'] for e in D[k]]):.2f} ramp med {np.median([e['ramp'] for e in D[k]])}f"
    if "highlight" in k: extra = " blinks " + str(Counter(e["blinks"] for e in D[k]).most_common())
    if k == "wipe": extra = " dirs " + str(Counter(e["dir"] for e in D[k]).most_common())
    print(f"{k:16s} {c:4d}  in {len(V[k]):2d}/36 videos  {c/tot*60:5.1f}/min  frames med {np.median(fr):.0f}{extra}")
