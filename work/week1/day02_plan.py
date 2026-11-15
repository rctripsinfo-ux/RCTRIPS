# DAY 2 "How Many Push-Ups Should You Do at Your Age?" (Pilot 3 style, stronger hook)
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w1 import *
from director import render
PU = dict(w=0.92, x=0.5, y=0.6)
S = [
 dict(text="Drop and count.", poses=[], layers=[dict(at=0, **PU, poses=[("hero_pushup_pair_b", 0), ("hero_pushup_pair_a", 0.3), ("hero_pushup_pair_b", 0.6), ("hero_pushup_pair_a", 0.9), ("hero_pushup_pair_b", 1.2)],
      ghost=dict(asset="hero_pushup_pair_a", at=0, alpha=0.3))], labels=[lab("count.", "HOW MANY?", y=0.22)],
      keys=hook_keys((.55, .6)), shake=[("count.", .04)], sfx=[(0, "whoosh_big", .2), ("count.", "pop", .3)]),
 dict(text="Your age decides if your number is weak or strong.", poses=[], tr="squash", d=0.37,
      layers=[body("d2_age20_cut", x=0.28, w=0.42), body("d2_age60_cut", at="weak", x=0.72, w=0.42, enter=("slide_r", 0.4))],
      labels=[lab("weak", "WEAK?", x=0.28, y=0.16), lab("strong.", "STRONG?", x=0.72, y=0.16)], keys=[(0, 1.0, .5, .5)] + punch("strong.", 1.0, 1.08)),
 dict(text="Please don't say it out loud.", poses=[], tr="cut", layers=[body("d2_age20_cut", x=0.28, w=0.42), body("d2_age60_cut", x=0.72, w=0.42), mini("mini_shy_cut")],
      keys=[(0, 1.0, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="In your twenties, around thirty clean push-ups is solid. Thirties, around twenty-five. Forties, twenty. Fifties, fifteen. Sixty plus, ten is already great.",
      poses=[], tr="brush", d=0.3,
      layers=[body("d2_age20_cut", x=0.2, w=0.3, y=0.66, enter=("rise", 0.4)), body("d2_age40_cut", at="Forties", x=0.5, w=0.3, y=0.66, enter=("rise", 0.4)),
              body("d2_age60_cut", at="Sixty", x=0.8, w=0.3, y=0.66, enter=("rise", 0.4))],
      labels=stack([("thirty", "20s  =  30"), ("Thirties", "30s  =  25"), ("Forties", "40s  =  20"), ("Fifties", "50s  =  15"), ("ten", "60+  =  10")], y0=0.1),
      keys=[(0, 1.0, .5, .5), ("E", 1.03, .5, .5)], sfx=[("thirty", "pop", .3), ("Thirties", "pop", .3), ("Forties", "pop", .3), ("Fifties", "pop", .3), ("ten", "pop", .3)]),
 dict(text="Clean means chest close to the floor and body straight like a plank.", poses=[], tr="cut",
      layers=[dict(at=0, **PU, poses=[("hero_pushup_pair_a", 0), ("hero_pushup_pair_b", "chest")], ghost=dict(asset="hero_pushup_pair_a", at="chest", alpha=0.3))],
      labels=[lab("chest", "CHEST TO FLOOR", x=0.3, y=0.2), lab("straight", "BODY STRAIGHT", x=0.7, y=0.26)],
      arcs=[dict(at="floor", x=0.5, y=0.5, r=0.1, a0=250, a1=290)], keys=[(0, 1.0, .5, .55)] + punch("straight", 1.0, 1.08, (.5, .55))),
 dict(text="What if I did eleven... at twenty-two?", poses=[], tr="cut",
      layers=[dict(at=0, **PU, asset="hero_pushup_pair_b"), mini("mini_scared_cut")], keys=[(0, 1.0, .5, .55)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Then do three sets of what you can, every other day. In a month, that number moves.", poses=[], tr="brush", d=0.3,
      layers=[full("a_three_full")], labels=[lab("three", "3 SETS", x=0.28, y=0.62), lab("every", "EVERY OTHER DAY", x=0.3, y=0.68)],
      particles=[dict(at="moves.", x=0.5, y=0.5, spread=0.5)], keys=[(0, 1.0, .5, .45), ("E", 1.05, .5, .45)], sfx=[("three", "pop", .3), ("every", "pop", .3), ("moves.", "chime", .4)]),
 dict(text="These are rough benchmarks, not a test of your worth.", poses=[], tr="fade", d=0.3, layers=[full("d2_age60")],
      labels=[lab("rough", "ROUGH GUIDE", x=0.3, y=0.66)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .45)]),
 dict(text="Your age and your number. Comment it. No lying.", poses=[], tr="cut", layers=[full("d2_age60"), mini("s9_mini_point_cut")],
      keys=[(0, 1.05, .5, .45)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = plan(2, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day02.mp4")
