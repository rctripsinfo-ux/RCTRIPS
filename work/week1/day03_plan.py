# DAY 3 "What Actually Makes Muscles Grow"
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w1 import *
from director import render
P3 = f"{HERE}/pilot3/img"
S = [
 dict(text="Sweat doesn't build muscle.", poses=[], layers=[full("d3_sweat")],
      insets=[dict(at="build", asset=img("d3_sweat"), crop=(0.5, 0.45, 0.6), x=0.8, y=0.14, r=0.12, mark="x", mark_delay=0.2)],
      labels=[lab("Sweat", "SWEAT", x=0.3, y=0.66)], keys=hook_keys((.5, .4)), shake=[("muscle.", .04)], sfx=[(0, "whoosh_big", .2), ("Sweat", "pop", .3)]),
 dict(text="Soreness doesn't either. One thing does.", poses=[], tr="squash", d=0.37, layers=[full("s1_collapsed")],
      labels=[lab("Soreness", "SORENESS", x=0.27, y=0.14), lab("One", "ONE THING DOES", y=0.24)],
      keys=[(0, 1.0, .5, .6)] + punch("One", 1.0, 1.15, (.5, .6)), sfx=[("Soreness", "pop", .3), ("One", "whoosh_short", .3)]),
 dict(text="Protein shakes?", poses=[], tr="cut", layers=[full("s1_collapsed"), mini("s6_mini_squint_cut")], keys=[(0, 1.15, .5, .6)], sfx=[(0, "pop_soft", .3)]),
 card("Tension.", "#1", "TENSION", "brush"),
 dict(text="When a muscle works hard close to its limit, its fibres get a signal: grow, or this happens again.", poses=[], tr="brush", d=0.3,
      layers=[dict(at=0, w=0.6, x=0.5, y=0.6, enter=("slide_r", 0.5), poses=[(f"{P3}/curl_a_al.png", 0), (f"{P3}/curl_b_al.png", "hard"), (f"{P3}/curl_a_al.png", "close"), (f"{P3}/curl_b_al.png", "limit")],
                   ghost=dict(asset=f"{P3}/curl_a_al.png", at="limit", alpha=0.3), highlight=dict(base=f"{P3}/curl_b_al.png", asset=f"{P3}/curl_b_red_al.png", at="fibres"))],
      insets=[dict(at="signal", asset=f"{P3}/anat_biceps.png", crop=(0.45, 0.5, 0.8), x=0.8, y=0.15, r=0.12, bg=(236, 230, 214), mark="tick")],
      labels=[lab("limit", "CLOSE TO YOUR LIMIT", y=0.26)], particles=[dict(at="grow", x=0.5, y=0.45, spread=0.5)],
      keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .55)], sfx=[("limit", "pop", .3), ("signal", "pop", .3), ("grow", "chime", .4)]),
 dict(text="Then two things finish the job. Protein, about one point six grams per kilo of body weight a day.", poses=[], tr="fade", d=0.3, layers=[full("d3_eat")],
      labels=[lab("Protein", "PROTEIN", x=0.27, y=0.12), lab("six", "1.6 g PER KG / DAY", x=0.5, y=0.2)], keys=[(0, 1.0, .5, .45), ("E", 1.06, .5, .45)],
      sfx=[("Protein", "pop", .3), ("six", "pop", .3)]),
 dict(text="And sleep, because that's when the repair happens.", poses=[], tr="fade", d=0.3, layers=[full("d3_sleep")],
      labels=[lab("sleep", "SLEEP", x=0.25, y=0.14), lab("repair", "REPAIR TIME", x=0.7, y=0.2)], particles=[dict(at="repair", x=0.5, y=0.45, spread=0.4)],
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("sleep", "pop", .3), ("repair", "chime", .4)]),
 dict(text="So the gym is just... the order form?", poses=[], tr="cut", layers=[full("d3_sleep"), mini("mini_laugh_cut")], keys=[(0, 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Exactly. The gym places the order. Food and sleep deliver it.", poses=[], tr="cut", layers=[full("s7_add_plate")],
      labels=[lab("order.", "GYM = ORDER", x=0.28, y=0.62), lab("deliver", "FOOD + SLEEP = DELIVERY", x=0.4, y=0.68)], keys=[(0, 1.0, .5, .45), ("E", 1.05, .5, .45)],
      sfx=[("order.", "pop", .3), ("deliver", "pop", .3)]),
 dict(text="Hard sets. Enough protein. Seven to nine hours.", poses=[], tr="fade", d=0.3, layers=[full("s8_couch_thumbs")],
      labels=stack([("Hard", "HARD SETS"), ("Enough", "ENOUGH PROTEIN"), ("Seven", "7-9 HOURS SLEEP")], x=0.28, y0=0.5, dy=0.06),
      keys=[(0, 1.0, .5, .45), ("E", 1.05, .5, .45)], sfx=[("Hard", "pop", .3), ("Enough", "pop", .3), ("Seven", "pop", .3)]),
 dict(text="Which one are you skipping? Be honest below.", poses=[], tr="cut", layers=[full("s8_couch_thumbs"), mini("s9_mini_point_cut")], keys=[(0, 1.05, .5, .45)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = plan(3, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day03.mp4")
