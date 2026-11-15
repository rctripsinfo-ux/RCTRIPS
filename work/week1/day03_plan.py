# DAY 3 v2 "Sweat Doesn't Build Muscle. This Does."
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w1 import *
from director import render
P3 = f"{HERE}/pilot3/img"
CURL = [(f"{P3}/curl_a_al.png", 0)]
S = [
 dict(text="Sweat doesn't build muscle.", poses=[], layers=[act([("d3_sweat", 0)])], labels=[lab("Sweat", "SWEAT", x=0.3, y=0.66)],
      insets=[dict(at="muscle.", asset=img("d3_sweat"), crop=(0.5, 0.45, 0.6), x=0.8, y=0.14, r=0.12, mark="x", mark_delay=0.15)],
      keys=hook_keys((.5, .4)), shake=[("muscle.", .04)], sfx=[(0, "whoosh_big", .2), ("Sweat", "pop", .3)]),
 dict(text="Soreness doesn't either. One thing does.", poses=[], tr="squash", d=0.37, layers=[act([("g_facepalm", 0), ("g_one", "One")])],
      labels=[lab("Soreness", "SORENESS", y=0.2), lab("One", "ONE THING DOES", y=0.27)], keys=[(0, 1.0, .5, .5)] + punch("One", 1.0, 1.1, (.5, .45)),
      sfx=[("Soreness", "pop", .3), ("One", "whoosh_short", .3)]),
 dict(text="Protein shakes?", poses=[], tr="cut", layers=[act([("g_one", 0)]), mini("s6_mini_squint_cut")], keys=[(0, 1.1, .5, .45)], sfx=[(0, "pop_soft", .3)]),
 card("Tension.", "#1", "TENSION", "brush"),
 dict(text="When a muscle works hard close to its limit, its fibres get a signal: grow, or this happens again.", poses=[], tr="brush", d=0.3,
      layers=[dict(at=0, w=0.6, x=0.5, y=0.6, enter=("slide_r", 0.5), poses=[(f"{P3}/curl_a_al.png", 0), (f"{P3}/curl_b_al.png", "hard"), (f"{P3}/curl_a_al.png", "close"), (f"{P3}/curl_b_al.png", "limit"),
                   (f"{P3}/curl_a_al.png", "signal"), (f"{P3}/curl_b_al.png", "grow")],
                   ghost=dict(asset=f"{P3}/curl_a_al.png", at="limit", alpha=0.3), highlight=dict(base=f"{P3}/curl_b_al.png", asset=f"{P3}/curl_b_red_al.png", at="fibres"))],
      insets=[dict(at="signal", asset=f"{P3}/anat_biceps.png", crop=(0.45, 0.5, 0.8), x=0.8, y=0.15, r=0.12, bg=(236, 230, 214), mark="tick")],
      labels=[lab("limit", "CLOSE TO YOUR LIMIT", y=0.27)], particles=[dict(at="grow", x=0.5, y=0.45, spread=0.5)],
      keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .55)], sfx=[("limit", "pop", .3), ("signal", "pop", .3), ("grow", "chime", .4)]),
 dict(text="Then two things finish the job.", poses=[], tr="squash", d=0.37, layers=[act([("g_two", 0), ("g_palm", "finish")])], labels=[lab("two", "2 THINGS", y=0.22)],
      keys=[(0, 1.0, .5, .5)], sfx=[("two", "pop", .3)]),
 dict(text="Protein, about one point six grams per kilo of body weight a day.", poses=[], tr="fade", d=0.3, layers=[act([("d3_eat", 0), ("d3_eat_b", "six"), ("d3_eat", "kilo"), ("d3_eat_b", "day.")])],
      labels=[lab("Protein", "PROTEIN", y=0.12), lab("six", "1.6 g PER KG / DAY", y=0.19)], keys=[(0, 1.0, .5, .45), ("E", 1.06, .5, .45)],
      sfx=[("Protein", "pop", .3), ("six", "pop", .3)]),
 dict(text="And sleep, because that's when the repair happens.", poses=[], tr="fade", d=0.3, layers=[full("d3_sleep")],
      labels=[lab("sleep", "SLEEP", y=0.14), lab("repair", "REPAIR TIME", y=0.21)], particles=[dict(at="repair", x=0.5, y=0.45, spread=0.4)],
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("sleep", "pop", .3), ("repair", "chime", .4)]),
 dict(text="So the gym is just... the order form?", poses=[], tr="cut", layers=[full("d3_sleep"), mini("mini_laugh_cut")], keys=[(0, 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Exactly. The gym places the order. Food and sleep deliver it.", poses=[], tr="cut", layers=[act([("g_point", 0), ("g_palm", "order."), ("g_thumbs", "deliver")])],
      labels=[lab("order.", "GYM = ORDER", y=0.2), lab("deliver", "FOOD + SLEEP = DELIVERY", y=0.27)], keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .5)],
      sfx=[("order.", "pop", .3), ("deliver", "pop", .3)]),
 dict(text="Hard sets. Enough protein. Seven to nine hours.", poses=[], tr="fade", d=0.3, layers=[act([("g_one", 0), ("g_two", "Enough"), ("g_flex", "Seven")])],
      labels=stack([("Hard", "HARD SETS"), ("Enough", "ENOUGH PROTEIN"), ("Seven", "7-9 HOURS SLEEP")], y0=0.14, dy=0.065),
      keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .5)], sfx=[("Hard", "pop", .3), ("Enough", "pop", .3), ("Seven", "pop", .3)]),
 dict(text="Which one are you skipping? Be honest below.", poses=[], tr="cut", layers=[act([("g_think", 0), ("g_point", "Be")]), mini("s9_mini_point_cut")], keys=[(0, 1.04, .5, .5)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = plan(3, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day03.mp4")
