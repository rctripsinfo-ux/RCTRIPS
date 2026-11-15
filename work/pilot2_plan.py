# PILOT 2 "The Laziest Way to Build Muscle" (Day 1 of the 30-day plan), STYLE V2 (research/STYLE-V2-PLAN.md):
# H first (Codex-generated full-frame shots, mostly close-ups), max 2 things on screen (H + Mini-H), plain white set,
# small competitor-size captions (Mini-H lines light purple), smooth motion only: slow drift, breathing, soft dissolves.
# usage: LUFS=-20 python3 pilot2_plan.py [t0 t1]
import sys
from director import render, HERE

IMG = f"{HERE}/pilot2/img"
def shot(name, at=0): return dict(at=at, w=1.0, x=0.5, y=0.5, asset=f"{IMG}/{name}.png")
def mini(name, at=0, side="r"):  # Mini-H grows out of a bottom corner, small, says one line
    return dict(at=at, w=0.3, x=0.8 if side == "r" else 0.2, y=0.79, asset=f"{IMG}/{name}_cut.png", enter=(f"corner_{side}", 0.4), z=2, breathe=True)

S = [
 dict(text="You don't need two hours in the gym.", poses=[], layers=[shot("s1_collapsed")],
      keys=[(0, 1.0, .5, .7), ("E", 1.14, .5, .7)], sfx=[(0, "whoosh_soft", .15)]),
 dict(text="You need forty minutes, three times a week.", poses=[], tr="cut", layers=[shot("s2_three_fingers")],
      keys=[(0, 1.0, .5, .45), ("E", 1.05, .5, .45)]),
 dict(text="That's it? I was promised suffering.", poses=[], tr="cut", layers=[shot("s2_three_fingers"), mini("s3_mini_disappointed")],
      keys=[(0, 1.05, .5, .45), ("E", 1.07, .5, .45)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Lazy rule one. Full body, three days a week. Every muscle gets hit three times instead of once.", poses=[], tr="fade", d=0.3,
      layers=[shot("s4_goblet_squat")], keys=[(0, 1.0, .5, .55), ("E", 1.06, .5, .55)]),
 dict(text="Rule two. Fewer sets, but hard ones. Stop when you have one or two reps left in the tank.", poses=[], tr="cut",
      layers=[shot("s5_last_rep")], keys=[(0, 1.0, .5, .4), ("E", 1.06, .5, .4)]),
 dict(text="So... quit early?", poses=[], tr="cut", layers=[shot("s5_last_rep"), mini("s6_mini_squint", side="l")],
      keys=[(0, 1.06, .5, .4), ("E", 1.07, .5, .4)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Quit smart. Rule three. Add one rep or a little weight every week. That's the whole secret.", poses=[], tr="fade", d=0.3,
      layers=[shot("s7_add_plate")], keys=[(0, 1.0, .5, .45), ("E", 1.06, .5, .45)]),
 dict(text="Forty minutes. Three days. One more rep each week.", poses=[], tr="fade", d=0.3,
      layers=[shot("s8_couch_thumbs")], keys=[(0, 1.0, .5, .45), ("E", 1.05, .5, .45)]),
 dict(text="Okay, which day are you starting? Tell me below.", poses=[], tr="cut", layers=[shot("s8_couch_thumbs"), mini("s9_mini_point")],
      keys=[(0, 1.05, .5, .45), ("E", 1.07, .5, .45)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/pilot2_cut.words.json", voice=f"{HERE}/voice/pilot2_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=18, duck=False, set=(255, 255, 255), breathe=True,
            scenes=S, cap_mode="build", cap_words=3, cap_size=54, cap_stroke=5, cap_y=0.78, cap_mini=(185, 168, 255),
            lead=0.06, tail=0.8, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/pilot2{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
