"""Audit a build.py: elements cut by the frame edge, text contrast, and pacing."""
import sys, json, importlib.util, numpy as np
spec = importlib.util.spec_from_file_location("b", sys.argv[1]); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
W, H, FPS = b.W, b.H, b.FPS
frame = np.zeros((H, W, 3), np.uint8)
cut = {}                                         # (beat, kind) -> list of times
for i in range(int(b.TOTAL * FPS)):
    t = i / FPS; b.REG.clear(); k = b.render_frame(t, frame)
    k = max(j for j, s in enumerate(b.STARTS) if s <= t or j == 0)
    for kind, x0, y0, x1, y1, al in b.REG:
        if al < 0.5 or x1 - x0 < 30:
            continue
        m = 2
        out = x0 < -m or y0 < -m or x1 > W + m or (y1 > H + m and kind != "character")
        if kind == "character" and (x0 < -m or x1 > W + m or y0 < -m):
            out = True
        if out:
            cut.setdefault((k, kind, round((x1-x0)/40)*40, round((y1-y0)/40)*40), []).append((t, round(x0), round(y0), round(x1), round(y1)))
persist = {key: v for key, v in cut.items() if len(v) >= 6}           # cut for 0.2 s or more (not a passing entrance)
print("ELEMENTS CUT BY THE FRAME EDGE (beat, kind): seconds cut, first time")
for key, v in sorted(persist.items()):
    k, kind = key[0], key[1]; t, x0, y0, x1, y1 = v[-1]
    print(f"  beat {k:2d} {kind:10s} {len(v)/FPS:5.2f}s from {v[0][0]:.2f}s  box=({x0},{y0})-({x1},{y1}) size {x1-x0}x{y1-y0}")
print("total:", len(persist))
# pacing
st = b.STARTS; gaps = np.diff(st)
print("scene gaps < 0.8 s:", [(round(st[j], 2), round(g, 2)) for j, g in enumerate(gaps) if g < 0.8])
print("entrance durations (frames):", [x.get("dur") for x in b.BEATS if "dur" in x])
