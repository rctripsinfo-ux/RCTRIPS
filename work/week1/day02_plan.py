# DAY 2 v2 "How Many Push-Ups Is Normal for Your Age?": pose animation in every scene, labels placed automatically off faces
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w1 import *
from director import render
PU = dict(w=0.92, x=0.5, y=0.6)
S = [
 dict(text="Drop and count.", poses=[], layers=[dict(at=0, **PU, poses=[("hero_pushup_pair_b", 0), ("hero_pushup_pair_a", 0.3), ("hero_pushup_pair_b", 0.6), ("hero_pushup_pair_a", 0.9), ("hero_pushup_pair_b", 1.2)],
      ghost=dict(asset="hero_pushup_pair_a", at=0, alpha=0.3))], labels=[lab("count.", "HOW MANY?", y=0.2)],
      keys=hook_keys((.55, .6)), shake=[("count.", .04)], sfx=[(0, "whoosh_big", .2), ("count.", "pop", .3)]),
 dict(text="Your age decides if your number is weak or strong.", poses=[], tr="squash", d=0.37,
      layers=[act([("g_point", 0), ("g_palm", "number"), ("g_one", "weak"), ("g_flex", "strong.")])],
      labels=[lab("weak", "WEAK?", x=0.25, y=0.3), lab("strong.", "STRONG?", x=0.75, y=0.3)], keys=[(0, 1.0, .5, .5)] + punch("strong.", 1.0, 1.06)),
 dict(text="Please don't say it out loud.", poses=[], tr="cut", layers=[act([("g_flex", 0)]), mini("mini_shy_cut")], keys=[(0, 1.06, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="In your twenties, around thirty clean push-ups is solid. Thirties, around twenty-five.", poses=[], tr="brush", d=0.3,
      layers=[body("d2_age20_cut", x=0.5, w=0.5, y=0.58, enter=("rise", 0.4))],
      labels=[lab("twenties", "20s  =  30", y=0.12), lab("Thirties", "30s  =  25", y=0.19)], keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .5)],
      sfx=[("thirty", "pop", .3), ("Thirties", "pop", .3)]),
 dict(text="Forties, twenty. Fifties, fifteen.", poses=[], tr="squash", d=0.37, layers=[body("d2_age40_cut", x=0.5, w=0.5, y=0.58)],
      labels=[lab("Forties", "40s  =  20", y=0.12), lab("Fifties", "50s  =  15", y=0.19)], keys=[(0, 1.0, .5, .5)], sfx=[("Forties", "pop", .3), ("Fifties", "pop", .3)]),
 dict(text="Sixty plus, ten is already great.", poses=[], tr="squash", d=0.37, layers=[body("d2_age60_cut", x=0.5, w=0.5, y=0.58)],
      labels=[lab("Sixty", "60+  =  10", y=0.12)], keys=[(0, 1.0, .5, .5)] + punch("great.", 1.0, 1.06), sfx=[("Sixty", "pop", .3), ("great.", "chime", .4)]),
 dict(text="Clean means chest close to the floor and body straight like a plank.", poses=[], tr="cut",
      layers=[dict(at=0, **PU, poses=[("hero_pushup_pair_a", 0), ("hero_pushup_pair_b", "chest"), ("hero_pushup_pair_a", "body"), ("hero_pushup_pair_b", "plank.")],
                   ghost=dict(asset="hero_pushup_pair_a", at="chest", alpha=0.3))],
      labels=[lab("chest", "CHEST TO FLOOR", y=0.2), lab("straight", "BODY STRAIGHT", y=0.27)], keys=[(0, 1.0, .5, .55)]),
 dict(text="What if I did eleven... at twenty-two?", poses=[], tr="cut", layers=[dict(at=0, **PU, asset="hero_pushup_pair_b"), mini("mini_scared_cut")], keys=[(0, 1.0, .5, .55)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Then do three sets of what you can, every other day. In a month, that number moves.", poses=[], tr="brush", d=0.3,
      layers=[act([("g_palm", 0), ("g_base", "three"), ("g_think", "every"), ("g_thumbs", "moves.")])],
      labels=[lab("three", "3 SETS", y=0.2), lab("every", "EVERY OTHER DAY", y=0.27)], particles=[dict(at="moves.", x=0.5, y=0.5, spread=0.5)],
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("three", "pop", .3), ("every", "pop", .3), ("moves.", "chime", .4)]),
 dict(text="These are rough benchmarks, not a test of your worth.", poses=[], tr="fade", d=0.3, layers=[act([("g_shrug", 0), ("g_hips", "test")])],
      labels=[lab("rough", "ROUGH GUIDE", y=0.2)], keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .5)]),
 dict(text="Your age and your number. Comment it. No lying.", poses=[], tr="cut", layers=[act([("g_point", 0), ("g_cross", "No")]), mini("s9_mini_point_cut")],
      keys=[(0, 1.04, .5, .5)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = plan(2, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day02.mp4")
