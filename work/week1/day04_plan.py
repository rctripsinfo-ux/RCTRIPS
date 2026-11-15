# DAY 4 "Be Honest: What's Your Arm Level?"
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w1 import *
from director import render
P3 = f"{HERE}/pilot3/img"
S = [
 dict(text="Every arm on Earth fits one of five levels.", poses=[], layers=[full("d4_door")], labels=[lab("five", "5 LEVELS", x=0.3, y=0.66)],
      keys=hook_keys((.5, .4)), shake=[("levels.", .04)], sfx=[(0, "whoosh_big", .2), ("five", "pop", .3)]),
 dict(text="Find yours.", poses=[], tr="squash", d=0.37, layers=[body("d4_arms_cut", w=0.96, x=0.5, y=0.48)], keys=[(0, 1.0, .5, .5)] + punch("yours.", 1.0, 1.06)),
 dict(text="Can we skip the first one?", poses=[], tr="cut", layers=[body("d4_arms_cut", w=0.96, x=0.5, y=0.48), mini("mini_shy_cut")], keys=[(0, 1.06, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Level one, the noodle. Level two, the beginner bump. Level three, the sleeve-filler. Level four, the shirt-stretcher. Level five, the doorframe problem.",
      poses=[], tr="cut", layers=[body("d4_arms_cut", w=0.96, x=0.5, y=0.48), full("d4_door", at="doorframe", enter=("fade", 0.25))],
      labels=stack([("noodle.", "1  NOODLE"), ("bump.", "2  BEGINNER BUMP"), ("sleeve-filler.", "3  SLEEVE-FILLER"), ("shirt-stretcher.", "4  SHIRT-STRETCHER")], y0=0.1)
             + [lab("doorframe", "5  DOORFRAME PROBLEM", y=0.12)],
      keys=[(0, 1.0, .5, .5), ("doorframe", 1.0, .5, .5), ("E", 1.06, .5, .45)],
      sfx=[("noodle.", "pop", .3), ("bump.", "pop", .3), ("sleeve-filler.", "pop", .3), ("shirt-stretcher.", "pop", .3), ("doorframe", "whoosh_short", .3)]),
 dict(text="I'm at one point five.", poses=[], tr="cut", layers=[body("d4_arms_cut", w=0.96, x=0.5, y=0.48), mini("mini_laugh_cut")], keys=[(0, 1.0, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Most guys get stuck at three because they only curl.", poses=[], tr="brush", d=0.3,
      layers=[dict(at=0, w=0.6, x=0.5, y=0.6, enter=("slide_r", 0.5), poses=[(f"{P3}/curl_a_al.png", 0), (f"{P3}/curl_b_al.png", "stuck"), (f"{P3}/curl_a_al.png", "three"), (f"{P3}/curl_b_al.png", "curl.")])],
      labels=[lab("curl.", "ONLY CURLS", y=0.14)], keys=[(0, 1.0, .5, .5)], sfx=[("curl.", "pop", .3)]),
 dict(text="The back of the arm is two-thirds of the size.", poses=[], tr="squash", d=0.37,
      layers=[dict(at=0, w=1.0, x=0.5, y=0.5, asset=img("d4_triceps"), highlight=dict(base=img("d4_triceps"), asset=img("d4_triceps_red"), at="back"))],
      labels=[lab("two-thirds", "2/3 OF YOUR ARM", x=0.3, y=0.7)], keys=[(0, 1.0, .5, .45)] + punch("two-thirds", 1.0, 1.1, (.55, .4)), sfx=[("back", "pop", .3), ("two-thirds", "pop", .3)]),
 dict(text="Train both, and add one rep a week.", poses=[], tr="fade", d=0.3, layers=[full("s7_add_plate")],
      labels=[lab("both", "TRAIN BOTH", x=0.28, y=0.62), lab("one", "+1 REP / WEEK", x=0.28, y=0.68)], particles=[dict(at="week.", x=0.55, y=0.5, spread=0.4)],
      keys=[(0, 1.0, .5, .45), ("E", 1.05, .5, .45)], sfx=[("both", "pop", .3), ("one", "pop", .3)]),
 dict(text="Levels change. Mirrors don't lie, but they do update.", poses=[], tr="fade", d=0.3, layers=[body("d4_arms_cut", w=0.96, x=0.5, y=0.48)],
      particles=[dict(at="update.", x=0.5, y=0.5, spread=0.6)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("update.", "chime", .4)]),
 dict(text="What level are you right now? Comment the number.", poses=[], tr="cut", layers=[body("d4_arms_cut", w=0.96, x=0.5, y=0.48), mini("s9_mini_point_cut")], keys=[(0, 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = plan(4, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day04.mp4")
