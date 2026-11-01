# One new image per scene for Days 4-30: writes SCENE-PROMPTS-DAY4-30.md and replaces tabs 5/6 of MASTER-30-DAYS.xlsx.
import os, re, sys, io, contextlib
W = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, W)
with contextlib.redirect_stdout(io.StringIO()):
    import make_master_sheet as M          # rebuilds the workbook first (tabs 1-4, 7) and gives P / COMMON texts
from scene_split import scenes
from scene_prompts_d4_30 import D, PX
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
CLEAN = [(", a padlock icon-free pose", ""), (", a friend-less empty gym behind", ", empty gym behind"), (", jeans-less (black shorts)", ""),
         ("lifting his shirt-less side to look at", "turning his side to look at"), (" showing (no numbers)", ""),
         ("a big '92%' banner on the wall behind (no other text)", "big gym lights behind him")]
def txt(spec):
    spec = spec.strip()
    if spec.startswith("P:"):
        k = spec[2:].strip(); t = PX.get(k) or M.P.get(k)
        if not t: raise SystemExit(f"no pose text for {k}")
        return t
    for a, b in CLEAN: spec = spec.replace(a, b)
    return spec
rows, md = [], ["# Scene images for Days 4-30: one NEW image per scene\n",
    "Scene = one sentence of the DRAFT script (very short answers stay with their question). Attach "
    "`work/character/H-standing-front-white.png` to EVERY prompt. Save each image with the exact file name (PNG). "
    "WHITE = pure white background (it gets cut out); SCENE = keep the full background. Two files (a/b) = the two frames of one exercise loop: "
    "same camera view, same size.\n"]
for d in range(4, 31):
    sc = scenes(d)
    if len(sc) != len(D[d]): raise SystemExit(f"day {d}: {len(sc)} scenes but {len(D[d])} prompts")
    md.append(f"\n## Day {d}: {M.T[d]['title']}\n")
    for n, (line, spec) in enumerate(zip(sc, D[d]), 1):
        kind, body = spec.split("|", 1); full = kind == "B"
        parts = [p for p in body.split("||")]
        for j, p in enumerate(parts):
            fid = f"d{d:02d}_s{n:02d}" + ("" if len(parts) == 1 else "ab"[j])
            prompt = (M.COMMON_SCENE if full else M.COMMON) + " " + txt(p)
            rows.append((d, n, line, fid, "SCENE (full background)" if full else "WHITE (cutout)", "NEW (generate)", prompt))
            md.append(f"**{fid}.png** ({'SCENE' if full else 'WHITE'}) — says: *{line}*\n```\n{prompt}\n```\n")
open(f"{W}/SCENE-PROMPTS-DAY4-30.md", "w").write("\n".join(md))
wb = load_workbook(f"{W}/MASTER-30-DAYS.xlsx")
for name in ("5 Image Requirements", "6 Generation Prompts"): del wb[name]
H = Font(bold=True, color="FFFFFF"); F = PatternFill("solid", fgColor="16191D")
def tab(name, head, data, widths, pos):
    ws = wb.create_sheet(name, pos); ws.append(head)
    for c in ws[1]: c.font = H; c.fill = F
    for r in data: ws.append(list(r))
    for i, w in enumerate(widths): ws.column_dimensions["ABCDEFG"[i]].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
done = [(d, 0, "Finished video", M.DONE[d]["video"], "video", "DONE", M.DONE[d]["status"]) for d in (1, 2, 3)]
tab("5 Image Requirements", ["Day", "Scene", "Narration (scene)", "File name", "Type", "Status", "Note"],
    done + [r[:6] + ("one new pose per scene",) for r in rows], [6, 7, 50, 16, 22, 16, 22], 4)
tab("6 Generation Prompts", ["Day", "Scene", "File name", "Type", "Copy-paste prompt (attach H-standing-front-white.png)"],
    [(r[0], r[1], r[3], r[4], r[6]) for r in rows], [6, 7, 16, 22, 120], 5)
wb.save(f"{W}/MASTER-30-DAYS.xlsx")
n_scene = sum(1 for r in rows if r[4].startswith("SCENE"))
print("scenes:", sum(len(scenes(d)) for d in range(4, 31)), "| images:", len(rows), "| white:", len(rows) - n_scene, "| full scene:", n_scene)
