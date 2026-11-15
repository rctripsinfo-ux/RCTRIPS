# DAY 6 v2 "Why Tendon Pain Takes Forever to Heal": pose animation everywhere
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w1 import *
from director import render
S = [
 dict(text="Your muscle healed in a week.", poses=[], layers=[act([("g_flex", 0), ("g_thumbs", "week.")])], labels=[lab("week.", "MUSCLE: 1 WEEK", y=0.2)],
      keys=hook_keys((.5, .45)), sfx=[(0, "whoosh_big", .2), ("week.", "pop", .3)]),
 dict(text="Your elbow still hurts after three months.", poses=[], tr="squash", d=0.37, layers=[act([("d6_elbow", 0), ("d6_elbow_b", "months.")])], labels=[lab("months.", "ELBOW: 3 MONTHS?!", x=0.36, y=0.68)],
      keys=[(0, 1.0, .5, .45)] + punch("months.", 1.0, 1.15, (.45, .5)), shake=[("months.", .05)], sfx=[("months.", "whoosh_short", .3)]),
 dict(text="Here's why.", poses=[], tr="squash", d=0.37, layers=[full("d6_anat")], keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .5)]),
 dict(text="Because I'm old?", poses=[], tr="cut", layers=[full("d6_anat"), mini("mini_scared_cut")], keys=[(0, 1.04, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Muscles have a big blood supply. Tendons have very little. Less blood means slower repair.", poses=[], tr="cut", layers=[full("d6_anat")],
      labels=[lab("blood", "MUSCLE = LOTS OF BLOOD", y=0.12), lab("Tendons", "TENDON = VERY LITTLE", y=0.18), lab("slower", "SLOWER REPAIR", y=0.24)],
      keys=[(0, 1.04, .5, .5), ("E", 1.1, .5, .5)], sfx=[("blood", "pop", .3), ("Tendons", "pop", .3), ("slower", "pop", .3)]),
 dict(text="And resting completely makes it worse. Tendons need load to rebuild.", poses=[], tr="fade", d=0.3, layers=[full("d6_sling", until="Tendons"), act([("g_palm", 0), ("g_flex", "rebuild.")], at="Tendons")],
      labels=[lab("worse.", "FULL REST = WORSE", y=0.12), lab("load", "LOAD = REBUILD", y=0.18)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)],
      sfx=[("worse.", "pop", .3), ("load", "pop", .3)]),
 dict(text="So... the answer is pain?", poses=[], tr="cut", layers=[act([("g_shrug", 0)]), mini("s6_mini_squint_cut")], keys=[(0, 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="The answer is gentle holds. Push or pull against something for thirty to forty-five seconds, at a level that feels manageable. Five holds a day.",
      poses=[], tr="brush", d=0.3, layers=[full("d6_hold", until="Five"), act([("g_one", 0)], at="Five")],
      labels=[lab("gentle", "GENTLE HOLDS", y=0.12), lab("thirty", "30-45 SEC", y=0.18), lab("Five", "5 HOLDS / DAY", y=0.24)],
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("gentle", "pop", .3), ("thirty", "pop", .3), ("Five", "pop", .3)]),
 dict(text="Slow and steady loads rebuild tendons. If the pain is sharp or getting worse, see a physio.", poses=[], tr="cut", layers=[act([("g_thumbs", 0), ("g_palm", "If"), ("g_point", "physio.")])],
      labels=[lab("sharp", "SHARP PAIN? SEE A PHYSIO", y=0.2)], particles=[dict(at="rebuild", x=0.5, y=0.45, spread=0.4)],
      keys=[(0, 1.05, .5, .5)], sfx=[("rebuild", "chime", .4), ("sharp", "pop", .3)]),
 dict(text="Which joint hurts? Tell me below.", poses=[], tr="cut", layers=[act([("g_think", 0)]), mini("s9_mini_point_cut")], keys=[(0, 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = plan(6, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day06.mp4")
