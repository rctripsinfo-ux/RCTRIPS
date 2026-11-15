# PILOT 3 "The Laziest Way to Build Muscle" (Day 1) in the DEMO 03 style the owner liked (effects library, smooth pose animation),
# now with NEW Codex-generated poses: aligned pose pairs (squat, curl) for in-place rep animation + ghost, full-body reaction poses,
# anatomy close-ups for the inset badges, full-frame close-ups as cut-ins. White set (owner), Mini-H as the commentator cameo.
# usage: LUFS=-20 python3 pilot3_plan.py [t0 t1]
import sys
from director import render, HERE

P3, P2 = f"{HERE}/pilot3/img", f"{HERE}/pilot2/img"
SLATE, SLATE_NUM = (75, 85, 104), (104, 116, 138)
GREEN = (46, 170, 80)
def punch(at, z0, z1, f=(.5, .53)): return [(at, z0, *f), (f"{at}+0.1", z1, *f)]
def full(name, at=0, **k): return dict(at=at, w=1.0, x=0.5, y=0.5, asset=f"{P2}/{name}.png", **k)
def mini(name, side="r"): return dict(at=0, w=0.36, x=0.78 if side == "r" else 0.22, y=0.76, asset=f"{P2}/{name}_cut.png", enter=(f"corner_{side}", 0.4), z=3, focus=True)
def card(text, num, label, tr):
    return dict(text=text, poses=[], tr=tr, d=0.3, set=SLATE, nocap=True, sfx=[(0, "whoosh_short", .3)],
                bgwords=[dict(text=num, at=-0.5, x=0.5, y=0.4, size=640, color=SLATE_NUM, cps=0.001)],
                labels=[dict(text=label, at=0.12, x=0.5, y=0.6, size=62)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .45)])

S = [
 # 1 HOOK: H collapsed on the floor, blurred 2x zoom-out, exhaustion lines, "2 HOURS" label
 dict(text="You don't need two hours in the gym.", poses=[],
      layers=[dict(at=0, w=0.86, x=0.5, y=0.6, asset=f"{P3}/collapsed_cut.png", shiver=[(0, "gym.")])],
      labels=[dict(at="two", text="2 HOURS", x=0.5, y=0.3)],
      keys=[(0, 1.9, .5, .62), (0.4, 1.0, .5, .5), ("E", 1.04, .5, .55)], sfx=[(0, "whoosh_soft", .2)]),
 # 2 squash -> H standing, 3 fingers; labels per number, punch on "three"
 dict(text="You need forty minutes, three times a week.", poses=[], tr="squash", d=0.37,
      layers=[dict(at=0, w=0.6, x=0.5, y=0.6, asset=f"{P3}/a_three_full_cut.png")],
      labels=[dict(at="forty", text="40 MIN", x=0.24, y=0.2), dict(at="three", text="3x / WEEK", x=0.76, y=0.2)],
      keys=[(0, 1.0, .5, .5)] + punch("three", 1.0, 1.12), sfx=[("forty", "pop", .3), ("three", "pop", .3)]),
 # 3 Mini-H cameo, everything behind blurs
 dict(text="That's it? I was promised suffering.", poses=[], tr="cut",
      layers=[dict(at=0, w=0.6, x=0.5, y=0.6, asset=f"{P3}/a_three_full_cut.png"), mini("s3_mini_disappointed")],
      keys=[(0, 1.0, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 card("Lazy rule one.", "#1", "FULL BODY", "brush"),
 # 5 squat pair: in-place reps + ghost, quads badge with tick, dashed arc
 dict(text="Full body, three days a week. Every muscle gets hit three times instead of once.", poses=[], tr="brush", d=0.3,
      layers=[dict(at=0, w=0.62, x=0.5, y=0.6, enter=("slide_r", 0.5),
                   poses=[(f"{P3}/sq_a_al.png", 0), (f"{P3}/sq_b_al.png", "three"), (f"{P3}/sq_a_al.png", "week."), (f"{P3}/sq_b_al.png", "Every"), (f"{P3}/sq_a_al.png", "hit")],
                   ghost=dict(asset=f"{P3}/sq_b_al.png", at="Every", alpha=0.3))],
      insets=[dict(at="muscle", asset=f"{P3}/anat_quads.png", crop=(0.5, 0.62, 0.8), x=0.8, y=0.16, r=0.12, bg=(236, 230, 214), mark="tick")],
      arcs=[dict(at="Every", until="hit", x=0.2, y=0.6, r=0.1, a0=300, a1=420)],
      labels=[dict(at="three#2", text="3 HITS / WEEK", x=0.27, y=0.16)],
      keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .55)], sfx=[("muscle", "pop", .3)]),
 card("Rule two.", "#2", "HARD SETS", "iris:1.0,0.4"),
 # 7 curl pair reps, biceps badge, cut-in to the strained face on "Stop", label 1-2 REPS LEFT
 dict(text="Fewer sets, but hard ones. Stop when you have one or two reps left in the tank.", poses=[], tr="brush", d=0.3,
      layers=[dict(at=0, until="Stop", w=0.6, x=0.5, y=0.6, enter=("slide_r", 0.5),
                   poses=[(f"{P3}/curl_a_al.png", 0), (f"{P3}/curl_b_al.png", "sets,"), (f"{P3}/curl_a_al.png", "but"), (f"{P3}/curl_b_al.png", "hard")],
                   ghost=dict(asset=f"{P3}/curl_a_al.png", at="hard", alpha=0.3)),
              full("s5_last_rep", at="Stop", enter=("fade", 0.2))],
      insets=[dict(at="hard", until="Stop", asset=f"{P3}/anat_biceps.png", crop=(0.45, 0.5, 0.8), x=0.8, y=0.16, r=0.12, bg=(236, 230, 214), mark="tick")],
      labels=[dict(at="one", text="1-2 REPS LEFT", x=0.3, y=0.68)],
      keys=[(0, 1.0, .5, .5), ("Stop", 1.0, .5, .4), ("E", 1.06, .5, .4)], sfx=[("hard", "pop", .3), ("Stop", "whoosh_short", .25)]),
 # 8 Mini-H doubts it over the close-up
 dict(text="So... quit early?", poses=[], tr="cut", layers=[full("s5_last_rep"), mini("s6_mini_squint", "l")],
      keys=[(0, 1.06, .5, .4)], sfx=[(0, "pop_soft", .3)]),
 # 9 H's answer, smirk close-up
 dict(text="Quit smart.", poses=[], tr="cut", layers=[full("s2_three_fingers")], keys=[(0, 1.0, .5, .45)] + punch("smart.", 1.0, 1.08, (.5, .4))),
 card("Rule three.", "#3", "+1 REP", "brush"),
 # 11 add a plate: labels + green plus particles on the secret
 dict(text="Add one rep or a little weight every week. That's the whole secret.", poses=[], tr="brush", d=0.3,
      layers=[full("s7_add_plate")],
      labels=[dict(at="one", text="+1 REP", x=0.25, y=0.62), dict(at="weight", text="OR + WEIGHT", x=0.25, y=0.68)],
      particles=[dict(at="secret.", x=0.6, y=0.55, spread=0.4)],
      keys=[(0, 1.0, .5, .45), ("E", 1.06, .5, .45)], sfx=[("one", "pop", .3), ("weight", "pop", .3), ("secret.", "chime", .4)]),
 # 12 recap on the couch: a stacked list, one label per phrase
 dict(text="Forty minutes. Three days. One more rep each week.", poses=[], tr="fade", d=0.3,
      layers=[full("s8_couch_thumbs")],
      labels=[dict(at="Forty", text="40 MIN", x=0.24, y=0.5), dict(at="Three", text="3 DAYS", x=0.24, y=0.56), dict(at="One", text="+1 REP / WEEK", x=0.24, y=0.62)],
      keys=[(0, 1.0, .5, .45), ("E", 1.05, .5, .45)], sfx=[("Forty", "pop", .3), ("Three", "pop", .3), ("One", "pop", .3)]),
 # 13 Mini-H asks the comment question
 dict(text="Okay, which day are you starting? Tell me below.", poses=[], tr="cut", layers=[full("s8_couch_thumbs"), mini("s9_mini_point")],
      keys=[(0, 1.05, .5, .45)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/pilot2_cut.words.json", voice=f"{HERE}/voice/pilot2_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=(255, 255, 255),
            scenes=S, cap_mode="build", cap_words=3, cap_size=62, cap_stroke=6, cap_y=0.8, cap_mini=(185, 168, 255),
            lead=0.06, tail=0.8, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/pilot3{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
