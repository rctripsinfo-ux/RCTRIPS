# DAY 8 "Your Birth Month Is Your Fitness Challenge": fast month-by-month montage, every exercise animates (THE METHOD)
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "week1"))
from w1 import *
from director import render
W2 = f"{HERE}/week2/img"; P3 = f"{HERE}/pilot3/img"
def w2(n): return f"{W2}/{n}.png"
def pair(a, b, at=0, step=0.35, n=12, **k):  # in-place reps from an aligned pair
    seq = [(a, at)] + [((b, a)[i % 2], f"{at}+{step * (i + 1):.2f}" if isinstance(at, str) else at + step * (i + 1)) for i in range(n)]
    return dict(at=at, w=0.82, x=0.5, y=0.58, poses=seq, **k)
def one(name, **k): return dict(at=0, w=0.82, x=0.5, y=0.58, asset=w2(name), **k)
def month(text, word, label, layer, tr="squash"):
    return dict(text=text, poses=[], tr=tr, d=0.37 if tr == "squash" else 0.3, layers=[layer], labels=[lab(word, label, y=0.12)],
                keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(word, "pop", .3)])
PU = dict(w=0.92, x=0.5, y=0.6)
S = [
 dict(text="Find your birth month.", poses=[], layers=[one("d8_calendar")], labels=[lab("birth", "YOUR BIRTH MONTH?", y=0.12)],
      keys=hook_keys((.5, .35)), shake=[("month.", .04)], sfx=[(0, "whoosh_big", .2), ("birth", "pop", .3)]),
 dict(text="That's your challenge for today.", poses=[], tr="squash", d=0.37, layers=[act([("g_point", 0), ("g_hips", "today.")])],
      labels=[lab("challenge", "TODAY'S CHALLENGE", y=0.12)], keys=[(0, 1.0, .5, .5)], sfx=[("challenge", "pop", .3)]),
 dict(text="No excuses.", poses=[], tr="cut", layers=[act([("g_cross", 0)])], keys=[(0, 1.0, .5, .5)] + punch("excuses.", 1.0, 1.12, (.5, .4)), shake=[("excuses.", .05)],
      sfx=[("excuses.", "whoosh_short", .3)]),
 dict(text="I was born in a leap year. I'm exempt.", poses=[], tr="cut", layers=[act([("g_cross", 0), ("g_facepalm", "exempt.")]), mini("mini_laugh_cut")], keys=[(0, 1.0, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 month("January, thirty squats.", "January", "JAN  ·  30 SQUATS",
       dict(at=0, w=0.6, x=0.5, y=0.6, poses=[(f"{P3}/sq_a_al.png", 0), (f"{P3}/sq_b_al.png", 0.35), (f"{P3}/sq_a_al.png", 0.7), (f"{P3}/sq_b_al.png", 1.05), (f"{P3}/sq_a_al.png", 1.4)],
            ghost=dict(asset=f"{P3}/sq_b_al.png", at=0.35, alpha=0.3)), tr="brush"),
 month("February, a one-minute plank.", "February", "FEB  ·  1-MIN PLANK", one("d8_plank", shiver=[("plank.", "plank.+0.6")])),
 month("March, twenty push-ups.", "March", "MAR  ·  20 PUSH-UPS", dict(at=0, **PU, poses=[("hero_pushup_pair_b", 0), ("hero_pushup_pair_a", 0.35), ("hero_pushup_pair_b", 0.7), ("hero_pushup_pair_a", 1.05)],
       ghost=dict(asset="hero_pushup_pair_a", at=0, alpha=0.3))),
 month("April, fifty jumping jacks.", "April", "APR  ·  50 JUMPING JACKS", pair(f"{W2}/d8_jacks_a_al.png", f"{W2}/d8_jacks_b_al.png", step=0.25)),
 month("May, a one-minute wall sit.", "May", "MAY  ·  1-MIN WALL SIT", one("d8_wallsit", shiver=[("sit.", "sit.+0.6")])),
 month("June, twenty lunges.", "June", "JUN  ·  20 LUNGES", one("d8_lunge")),
 month("July, thirty-second dead bug.", "July", "JUL  ·  30-SEC DEAD BUG", one("d8_deadbug"), tr="brush"),
 month("August, fifteen burpees.", "August", "AUG  ·  15 BURPEES", one("d8_burpee", enter=("rise", 0.3))),
 month("September, forty mountain climbers.", "September", "SEP  ·  40 MOUNTAIN CLIMBERS", pair(f"{W2}/d8_climber_a_al.png", f"{W2}/d8_climber_b_al.png", step=0.22)),
 month("October, twenty glute bridges.", "October", "OCT  ·  20 GLUTE BRIDGES", pair(f"{W2}/d8_bridge_a_al.png", f"{W2}/d8_bridge_b_al.png", step=0.4)),
 month("November, a two-minute walk on your toes.", "November", "NOV  ·  2-MIN TOE WALK", one("d8_toewalk")),
 dict(text="December, all of the above.", poses=[], tr="squash", d=0.37, layers=[full("s1_collapsed")], labels=[lab("December", "DEC  ·  ALL OF THE ABOVE", y=0.12)],
      keys=[(0, 1.0, .5, .55)] + punch("above.", 1.0, 1.12, (.5, .6)), shake=[("above.", .05)], sfx=[("December", "pop", .3), ("above.", "whoosh_short", .3)]),
 dict(text="December people, I'm so sorry.", poses=[], tr="cut", layers=[full("s1_collapsed"), mini("mini_scared_cut")], keys=[(0, 1.12, .5, .6)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Do it now, then comment your month and done.", poses=[], tr="brush", d=0.3, layers=[act([("g_point", 0), ("g_palm", "comment"), ("g_thumbs", "done.")])],
      labels=[lab("comment", "COMMENT: MONTH + DONE", y=0.12)], particles=[dict(at="done.", x=0.5, y=0.5, spread=0.5)],
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("comment", "pop", .3), ("done.", "chime", .4)]),
]
PLAN = plan(8, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day08.mp4")
