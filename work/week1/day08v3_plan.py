# DAY 8 v3 "Your Birth Month Is Your Workout Challenge" with THE LONG METHOD engine (9:16): every month is a rep loop
from w3 import *
def mon(text, word, short, task, a, b=None, step=0.35, h=0.62, y=0.56, shiver=False):
    lay = act(reps(a, b, 12, step), h=h, y=y, pop=0.02, puppet=False) if b else fig(a, h=h, y=y, puppet=False, shiver=[(0, f"{word}+3")] if shiver else [])
    return S_(text, [lay], [kin(0, short, 0.5, 0.07, 140, TEAL), kin(0.1, task, 0.5, 0.15, 100, INK)], sfx=[(0, "pop", .3)])
ALL = ["sq_a", "d8_plank", "pu_bot", "d8_jacks_b", "d8_wallsit", "d8_lunge", "d8_deadbug", "d8_burpee_b", "d8_climber_a", "d8_bridge_b", "d8_toewalk"]
S = [
 S_("Find your birth month.", [act([("p_count", 0), ("g_point", "month.")], y=0.62, h=0.5)], [kin("birth", "YOUR BIRTH MONTH?", 0.5, 0.08, 100, RED)],
    calendars=[dict(at=0, x=0.5, y=0.24, w=0.9, cols=6, n=12, ticks=[])], keys=HOOK, sfx=[(0, "whoosh_big", .2)]),
 S_("That's your challenge for today.", [act([("g_point", 0), ("g_hips", "today.")])], [kin("challenge", "TODAY'S CHALLENGE", 0.5, 0.1, 110, TEAL)]),
 S_("No excuses.", [act([("g_cross", 0)])], [kin(0, "NO EXCUSES.", 0.5, 0.1, 140, RED)], keys=DRIFT + [("excuses.", 1.04, .5, .45), ("excuses.+0.1", 1.12, .5, .4)], shake=[("excuses.", .05)]),
 M("I was born in a leap year. I'm exempt.", [act([("g_cross", 0), ("g_facepalm", "exempt.")], x=0.4)], "mini_laugh_cut", kinetic=[kin("exempt.", "EXEMPT?", 0.5, 0.1, 140, RED)]),
 mon("January, thirty squats.", "January", "JAN", "30 SQUATS", "sq_a", "sq_b", 0.3),
 mon("February, a one-minute plank.", "February", "FEB", "1-MIN PLANK", "d8_plank", shiver=True, h=0.95),
 mon("March, twenty push-ups.", "March", "MAR", "20 PUSH-UPS", "pu_top", "pu_bot", 0.3, h=0.38, y=0.58),
 mon("April, fifty jumping jacks.", "April", "APR", "50 JUMPING JACKS", "d8_jacks_a", "d8_jacks_b", 0.22),
 mon("May, a one-minute wall sit.", "May", "MAY", "1-MIN WALL SIT", "d8_wallsit", shiver=True),
 mon("June, twenty lunges.", "June", "JUN", "20 LUNGES", "d8_lunge", "d8_lunge_b", 0.4),
 mon("July, thirty-second dead bug.", "July", "JUL", "30-SEC DEAD BUG", "d8_deadbug", "d8_deadbug_b", 0.4, h=0.95),
 mon("August, fifteen burpees.", "August", "AUG", "15 BURPEES", "d8_burpee", "d8_burpee_b", 0.3),
 mon("September, forty mountain climbers.", "September", "SEP", "40 MOUNTAIN CLIMBERS", "d8_climber_a", "d8_climber_b", 0.2, h=0.95),
 mon("October, twenty glute bridges.", "October", "OCT", "20 GLUTE BRIDGES", "d8_bridge_a", "d8_bridge_b", 0.4, h=0.95),
 mon("November, a two-minute walk on your toes.", "November", "NOV", "2-MIN TOE WALK", "d8_toewalk", "d8_toewalk_b", 0.3),
 S_("December, all of the above.", [act([(p, round(i * 0.14, 2)) for i, p in enumerate(ALL)] + [("H_collapse", "above.")], h=0.62, pop=0.02, puppet=False)],
    [kin(0, "DEC", 0.5, 0.07, 140, RED), kin(0.1, "ALL OF THE ABOVE", 0.5, 0.15, 100, RED)], shake=[("above.", .05)], sfx=[(0, "pop", .3), ("above.", "whoosh_short", .3)]),
 M("December people, I'm so sorry.", [fig("H_collapse", h=0.3, y=0.62, puppet=False)], "mini_scared_cut", "l", kinetic=[kin("sorry.", "SO SORRY", 0.5, 0.1, 130, RED)]),
 S_("Do it now, then comment your month and done.", [act([("g_point", 0), ("g_palm", "comment"), ("g_thumbs", "done.")])],
    [kin(0, "DO IT NOW", 0.5, 0.08, 110, TEAL), kin("comment", "COMMENT: MONTH + DONE", 0.5, 0.15, 90, RED)], tr="dip", d=0.4),
]
PLAN = plan(8, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day08_v3.mp4")
