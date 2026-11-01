# Matches Flow's randomly named downloads to our file names (dNN_sMM[a|b]) by order + filename words (sequence alignment).
# usage: python3 match_flow_images.py <zip> <out_dir>
import csv, re, subprocess, sys, json
zp, out = sys.argv[1], sys.argv[2]
names = [l.split()[-1] for l in subprocess.run(["unzip", "-Z1", zp], capture_output=True, text=True).stdout.split("\n") if l.endswith(".jpg")]
names = names[::-1]  # Flow lists the newest first
rows = list(csv.DictReader(open(sys.argv[3] if len(sys.argv) > 3 else "flow/ALL-PROMPTS.csv")))
STOP = set("muscular man men performing doing the on in at with a an and of his h to is it for".split())
def stem(w): return re.sub(r"(ing|es|s|ed)$", "", w)
def ftok(n): return {stem(w) for w in re.split(r"[_\W]+", re.sub(r"_[0-9a-f]{8}\.jpg$", "", n).lower()) if w and w not in STOP and not w.startswith("u2026")}
def ptok(p):
    a = p.split("SCENE ACTION:", 1)[1].split("CHARACTER", 1)[0].lower()
    return {stem(w) for w in re.findall(r"[a-z]+", a) if w not in STOP}
F = [ftok(n) for n in names]; Pt = [ptok(r["prompt"]) for r in rows]
n, m = len(F), len(Pt)
import numpy as np
from scipy.optimize import linear_sum_assignment
C = np.full((n, m), 1e6)
for i in range(n):
    e = i * m / n
    for j in range(max(0, int(e) - 40), min(m, int(e) + 41)):
        C[i, j] = -len(F[i] & Pt[j]) + 0.02 * abs(j - e)
ri, cj = linear_sum_assignment(C)
pairs = [(names[i], rows[j]["file_name"], len(F[i] & Pt[j])) for i, j in zip(ri, cj) if C[i, j] < 1e5]
used = {p[1] for p in pairs}; got = {p[0] for p in pairs}
missing = [r["file_name"] for r in rows if r["file_name"] not in used]; extra = [x for x in names if x not in got]
pairs.sort(key=lambda p: p[1])
json.dump({"pairs": pairs, "missing": missing, "extra": extra}, open(f"{out}/match.json", "w"), indent=1)
weak = [p for p in pairs if p[2] == 0]
print("images:", n, "prompts:", m, "matched:", len(pairs), "missing:", len(missing), "extra:", len(extra), "zero-overlap:", len(weak))
print("missing:", missing); print("weak:", [(p[0][:38], p[1]) for p in weak])
