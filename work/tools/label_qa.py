# usage: python3 tools/label_qa.py <plan.py> [sheet.jpg]
# every 0.25 s while labels are on screen: where each label sits (engine placement) vs what is under it on the stage WITHOUT labels
# (face zone = top 30 % of each big figure). Flags: on a face, over the figure, over another label, outside the frame.
import importlib.util, sys, copy, numpy as np
sys.path.insert(0, ".")
from director import Renderer, W, H
from PIL import Image, ImageDraw
spec = importlib.util.spec_from_file_location("p", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = Renderer(copy.deepcopy(m.PLAN)); bare = copy.deepcopy(m.PLAN)
for s in bare["scenes"]: s["labels"] = []
rb = Renderer(bare); flags = []; seen = set()
for i, s in enumerate(r.tl.sc):
    if not s.get("labels"): continue
    t = s["T"] + 0.05
    while t < s["E"]:
        r.frame(t)
        live = [e for e in s["labels"] if "_xy" in e and r._live(e, s, t) and not e.get("style")]
        if live:
            st = rb.scene(i, t).convert("RGBA"); occ, face = rb.occupancy(st, rb.tl.sc[i]); boxes = []
            for e in live:
                bw, bh = e["_im"].width / 8, e["_im"].height / 8; x0, y0 = e["_xy"][0] / 8 - bw / 2, e["_xy"][1] / 8 - bh / 2
                sl = (slice(max(0, int(y0)), int(y0 + bh) + 1), slice(max(0, int(x0)), int(x0 + bw) + 1))
                fo, oo = face[sl].mean(), occ[sl].mean(); out = x0 < 0 or y0 < 0 or x0 + bw > W / 8 or y0 + bh > H / 8
                lo = max([max(0, min(x0 + bw, b[2]) - max(x0, b[0])) * max(0, min(y0 + bh, b[3]) - max(y0, b[1])) / (bw * bh) for b in boxes] + [0])
                boxes.append((x0, y0, x0 + bw, y0 + bh))
                bad = [k for k, v in (("FACE", fo > 0.02), ("FIGURE", oo > 0.25 and not s.get("_textmode")), ("LABEL", lo > 0.02), ("OUTSIDE", out)) if v]
                if bad and (e["text"], tuple(bad)) not in seen:
                    seen.add((e["text"], tuple(bad))); flags.append((round(t, 2), e["text"], bad, round(float(fo), 3), round(float(oo), 3)))
        t += 0.25
for f in flags: print("FLAG", *f)
print(f"{sys.argv[1]}: {len(flags)} problems")
if len(sys.argv) > 2 and flags:
    ims = [r.frame(f[0]).resize((216, 384)) for f in flags[:12]]; sh = Image.new("RGB", (216 * len(ims), 400), "black"); d = ImageDraw.Draw(sh)
    for k, (im, f) in enumerate(zip(ims, flags)): sh.paste(im, (k * 216, 16)); d.text((k * 216 + 2, 2), f"{f[0]} {f[1][:14]} {','.join(f[2])}", fill="yellow")
    sh.save(sys.argv[2])
