# DAY 5 v2 "Do This 10-Minute Walk After You Eat": pose animation everywhere
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w1 import *
from director import render
def walk(at=0, until=None, **k):  # in-place walk cycle from the aligned stride pair
    seq = [(img("d5_walk_a_al"), at)] + [((img("d5_walk_b_al"), img("d5_walk_a_al"))[i % 2], f"{at}+{0.38 * (i + 1):.2f}" if isinstance(at, str) else at + 0.38 * (i + 1)) for i in range(40)]
    return dict(at=at, until=until, w=0.6, x=0.5, y=0.6, poses=seq, **k)
S = [
 dict(text="You just ate.", poses=[], layers=[act([("d5_meal", 0), ("d5_meal_b", "ate.")])], labels=[lab("ate.", "JUST ATE?", x=0.3, y=0.66)],
      keys=hook_keys((.5, .55)), shake=[("ate.", .04)], sfx=[(0, "whoosh_big", .2), ("ate.", "pop", .3)]),
 dict(text="Don't sit.", poses=[], tr="cut", layers=[act([("g_point", 0)])], labels=[lab(0, "DON'T SIT", y=0.2)],
      keys=[(0, 1.05, .5, .5)] + punch("sit.", 1.05, 1.15, (.5, .4)), shake=[("sit.", .05)], sfx=[("sit.", "whoosh_short", .3)]),
 dict(text="This is the laziest fat-loss trick there is.", poses=[], tr="squash", d=0.37, layers=[walk(0)], labels=[lab("trick", "10-MIN WALK", y=0.14)],
      keys=[(0, 1.0, .5, .5)], sfx=[("trick", "pop", .3)]),
 dict(text="Walking? That's not exercise.", poses=[], tr="cut", layers=[walk(0), mini("s6_mini_squint_cut")], keys=[(0, 1.0, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="A ten-minute walk right after a meal helps your muscles soak up the sugar from that meal, so your blood sugar spikes less.", poses=[], tr="cut",
      layers=[walk(0)], labels=[lab("after", "RIGHT AFTER A MEAL", y=0.12), lab("spikes", "SMALLER SUGAR SPIKE", y=0.18)],
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("after", "pop", .3), ("spikes", "pop", .3)]),
 dict(text="Do it after your biggest meal every day.", poses=[], tr="fade", d=0.3, layers=[act([("g_palm", 0), ("g_one", "biggest"), ("g_thumbs", "every")])], labels=[lab("biggest", "BIGGEST MEAL", y=0.2)],
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("biggest", "pop", .3)]),
 dict(text="That's seventy extra minutes of moving every week, without a single workout.", poses=[], tr="fade", d=0.3, layers=[walk(0)],
      labels=[lab("seventy", "+70 MIN / WEEK", y=0.14)], particles=[dict(at="workout.", x=0.5, y=0.45, spread=0.5)],
      keys=[(0, 1.0, .5, .5)] + punch("seventy", 1.0, 1.08), sfx=[("seventy", "pop", .3), ("workout.", "chime", .4)]),
 dict(text="Can I walk to the fridge?", poses=[], tr="cut", layers=[act([("d5_fridge", 0)]), mini("mini_laugh_cut")], keys=[(0, 1.0, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="You can walk past it.", poses=[], tr="cut", layers=[act([("d5_fridge", 0), ("d5_fridge_b", "past")])], labels=[lab("past", "WALK PAST IT", y=0.14)],
      keys=[(0, 1.0, .5, .5)] + punch("past", 1.0, 1.1, (.5, .5)), sfx=[("past", "pop", .3)]),
 dict(text="Ten minutes. After meals. Every day.", poses=[], tr="fade", d=0.3, layers=[walk(0)],
      labels=stack([("Ten", "10 MINUTES"), ("After", "AFTER MEALS"), ("Every", "EVERY DAY")], y0=0.1), keys=[(0, 1.0, .5, .5)],
      sfx=[("Ten", "pop", .3), ("After", "pop", .3), ("Every", "pop", .3)]),
 dict(text="Which meal are you walking after? Tell me below.", poses=[], tr="cut", layers=[walk(0), mini("s9_mini_point_cut")], keys=[(0, 1.0, .5, .5)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = plan(5, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day05.mp4")
