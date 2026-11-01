# Builds the plan for one Day 4-30 video from the draft script (scripts_d4_30.py), its scenes (scene_split.py) and the
# owner's scene images (character/scenes, imported with import_scenes.py). One new image per scene; every image
# slides in from one side and leaves to the other (never two H's at once); headings from the script; kinetic bumper;
# anatomy bubble where the script has one; one whoosh per scene, ding on the payoff, no CTA ringtone.
# usage: python3 build_scene_video.py 4   -> dayNN.txt, dayNN.json, dayNN.pauses.json
import json, os, re, sys
from h_kit import *
from scripts_d4_30 import S as SCR
from scene_split import scenes

d = int(sys.argv[1]); name = f"day{d:02d}"
use_preset("beige")
tuples = [t for t in SCR[d] if t[0]]
script = " ".join(t[0] for t in tuples)
open(f"{name}.txt", "w").write(script + "\n")
json.dump({"_gap": 0.05, "fix.": 0.35}, open(f"{name}.pauses.json", "w"))
H_ = {a["id"]: a for a in json.load(open(f"{LIB}/hero/library.json"))["assets"]}
words = " ".join(re.sub(r"[^a-z0-9'\- ]", " ", script.lower()).split())

def anchor(sent):
    """first 2-4 words of a sentence, made unique with #k when the phrase is spoken more than once"""
    w = re.sub(r"[^A-Za-z0-9'\- ]", " ", sent).split()  # keep hyphen words whole (pull-aparts)
    for k in (3, 4, 2, 5):
        ph = " ".join(w[:k]); q = " ".join(ph.lower().split())
        hits = [m.start() for m in re.finditer(rf"(?<![a-z0-9'\-]){re.escape(q)}(?![a-z0-9'\-])", words)]
        if len(hits) == 1: return ph
    # several: find which occurrence this sentence is
    pos = words.find(" ".join(re.sub(r"[^a-z0-9'\- ]", " ", sent.lower()).split()))
    q = " ".join(" ".join(w[:3]).lower().split())
    hits = [m.start() for m in re.finditer(rf"(?<![a-z0-9'\-]){re.escape(q)}(?![a-z0-9'\-])", words)]
    return " ".join(w[:3]) + f"#{[h for h in hits if h <= pos].__len__()}"

sc_list = scenes(d)
imgs = {}
for f in sorted(os.listdir("character/scenes")):
    m = re.match(rf"d{d:02d}_s(\d\d)([ab]?)\.webp$", f)
    if m: imgs.setdefault(int(m.group(1)), []).append(f"sc_{f[:-5]}")

def tuple_of(sent):
    key = sent[:25]
    return next((t for t in tuples if key in t[0]), None)

def place(aid, left=False):
    a = H_[aid]
    if "scene" in a.get("tags", []): return {"autoAlign": False, "width": 0.84, "y": 0.62, "shadow": True}, True  # photo card under the heading
    bx = a.get("bbox", [0, 0, 1, 1]); wide = (bx[2] - bx[0]) * a["size"][0] > (bx[3] - bx[1]) * a["size"][1] * 0.9
    if wide: return {"width": 0.95, "y": 0.6}, False
    return (LEFT if left else BODY), False

anc = [anchor(s) for s in sc_list]
plan_scenes, cues_, seen = [], [], set()
for n, sent in enumerate(sc_list, 1):
    a = anc[n - 1]; nxt = anc[n] if n < len(sc_list) else None
    t = tuple_of(sent); head = t[1] if t and t[1] not in seen else None
    if t: seen.add(t[1])
    ids = imgs.get(n, [])
    if not ids: raise SystemExit(f"day {d} scene {n}: no image yet ({sent})")
    bubble_on = bool(t and t[2].startswith("anat_") and head)
    lay, full = place(ids[0], left=bubble_on)
    side = "flyRight" if n % 2 else "flyLeft"; out = "flyLeft" if n % 2 else "flyRight"
    L = []
    if len(ids) > 1:  # exercise loop: frames a/b swap every 0.5 s
        L.append({**poses(loop(ids[0], ids[1], a, 12, 0.5), **lay), "enter": {"type": side, "duration": 0.25}, "shadow": True,
                  **({"until": nxt, "exit": {"type": out, "duration": 0.25}} if nxt else {})})
    else:
        L.append({**img(ids[0], a, nxt, enter={"type": side, "duration": 0.25}, **lay), "shadow": True,
                  **({"exit": {"type": out, "duration": 0.25}} if nxt else {})})
    if head == "HERE'S THE FIX":
        L[0].update(width=0.7, y=0.72) if not full else None
        L += kinetic([("HERE'S", 0.17, 120, INK, 0), ("THE FIX", 0.27, 220, RED, "the fix")], a)
        cues_ += [(a, "bumper"), ("fix.+0.15", "big")]
    else:
        if head: L.append(title(head, a, nxt, size=125 if len(head) > 14 else 140))
        cues_.append((a, "enter"))
    if bubble_on: L.append(bubble(t[2], f"{a}+0.3", nxt, x=0.8, y=0.66, size=0.28))
    plan_scenes.append(sc(f"s{n}", a if n == 1 else f"{a}-0.05", L))
plan_scenes[0]["start"] = "start"; plan_scenes[0]["layers"][0].update(at="start", enter=ENTER["rise"])
# HOOK PACK (first 2 s, owner 1 Nov): impact frame + heavy whoosh, smash zoom-out 1.7 -> 1.0 in 0.3 s, red heading slams in
# at frame 1 (no typing), speed lines 0-0.7 s, pop at 0.35 s, camera punch-in at ~1 s
h0 = plan_scenes[0]["layers"]
for L in h0:
    if L.get("type") == "text": L.update(color=RED, animation="none", enter={"type": "slam", "duration": 0.3}, at="start")
h0[:0] = [{"type": "pulse", "kind": "impact", "at": "start", "duration": 0.15}]
h0.append(speed_lines("start", "start+0.7"))
plan_scenes[0]["camera"] = [{"at": "start", "zoom": 1.7, "focus": [0.5, 0.42]}, {"at": "start+0.3", "zoom": 1.0},
                            {"at": "start+0.9", "zoom": 1.0}, {"at": "start+1.2", "zoom": 1.1, "focus": [0.5, 0.45]}]
cues_[0:1] = [("start", "big"), ("start+0.35", "info")]
cues_.insert(len(cues_) - 1, (anc[-2], "reveal"))
bump = next((anc[i] for i, s in enumerate(sc_list) if s.startswith("Here's the fix")), None)
plan = {
    "title": f"Day {d}", "canvas": {"background": P["bg"]}, "style": {"accent": YEL}, "audio": {"autoSfx": False},
    "captions": {"mode": "phrase", "look": "clean", "size": 54, "y": P["cap_y"], "maxWords": 3,
                 "hide": [[bump, anc[sc_list.index(next(s for s in sc_list if s.startswith("Here's the fix"))) + 1]]] if bump else []},
    "scenes": plan_scenes,
    "sfx": cues([c for c in cues_ if c[1] != "reveal" or c[0] != anc[-1]]),
}
tidy(plan); validate(plan, script)
json.dump(plan, open(f"{name}.json", "w"), indent=1, ensure_ascii=False)
print(name, "scenes:", len(sc_list), "| anchors:", anc)
