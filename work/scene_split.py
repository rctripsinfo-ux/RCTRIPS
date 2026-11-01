# Splits the Day 4-30 scripts into scenes: one sentence = one scene; a 1-2 word sentence joins the one before it
# (a picture must stay at least ~1.5 s on screen).
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts_d4_30 import S
def scenes(d):
    txt = " ".join(x[0] for x in S[d] if x[0]).replace("p.m.", "pm.")
    out = []
    for s in [s.strip() for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]:
        short = len(s.split()) <= 2 and not s.endswith("?") and not re.match(r"^(One|Two|Three|Four):", s)
        if out and (short or s in ("Can you?", "Here's why.")): out[-1] += " " + s
        else: out.append(s)
    return out
if __name__ == "__main__":
    t = 0
    for d in range(4, 31):
        sc = scenes(d); t += len(sc); print(d, len(sc), " | ".join(f"{i+1}:{s[:38]}" for i, s in enumerate(sc)))
    print("TOTAL", t)
