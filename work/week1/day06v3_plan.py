# DAY 6 v3 "Why Tendon Pain Takes Forever to Heal" with THE LONG METHOD engine (9:16)
from w3 import *
BLOOD = dict(x=0.5, y=0.8, w=0.4, h=0.18, values=[10, 2], labels=["MUSCLE", "TENDON"], show_values=False, hi_last=True, hi_color=RED, color=TEAL)
WALLP = [dict(at=0, w=130 / 1080, x=0.78, y=0.544, asset=path("prop_wall"), puppet=False, breathe=False), fig("L_wall_a", x=0.4, y=0.6, h=0.45, puppet=False, shiver=[(0, "manageable.+1")])]
S = [
 S_("Your muscle healed in a week.", [act([("p_flexglow", 0), ("g_thumbs", "week.")])], [kin("muscle", "MUSCLE", 0.5, 0.08, 110, TEAL), kin("week.", "1 WEEK", 0.5, 0.15, 120, TEAL)],
    keys=HOOK, sfx=[(0, "whoosh_big", .2)]),
 S_("Your elbow still hurts after three months.", [act([("p_elbow", 0)])], [kin("elbow", "ELBOW", 0.5, 0.08, 110, RED), kin("three", "3 MONTHS", 0.5, 0.15, 120, RED)],
    shake=[("months.", .04)], sfx=[("three", "pop", .3)]),
 S_("Here's why.", [act([("p_temple", 0)])], [kin(0, "HERE'S WHY", 0.5, 0.1, 130)]),
 M("Because I'm old?", [act([("p_offended", 0)], x=0.4)], "mini_shy_cut", kinetic=[kin("old?", "OLD?", 0.5, 0.1, 150, RED)]),
 S_("Muscles have a big blood supply. Tendons have very little. Less blood means slower repair.",
    [act([("p_flexglow", 0), ("p_elbow", "Tendons"), ("g_think", "Less")], y=0.38, h=0.4)],
    [kin(0, "BLOOD SUPPLY", 0.5, 0.08, 110), kin("Less", "SLOWER REPAIR", 0.5, 0.15, 110, RED)], bars=[dict(at=0, stagger=1.9, **BLOOD)], tr="dip", d=0.4),
 S_("And resting completely makes it worse.", [act([("p_sling", 0)])], [kin("resting", "FULL REST", 0.5, 0.08, 110), kin("worse.", "= WORSE", 0.5, 0.15, 120, RED)]),
 S_("Tendons need load to rebuild.", [act([("p_snap", 0), ("g_flex", "rebuild.")])], [kin("load", "NEED LOAD", 0.5, 0.1, 130, TEAL)]),
 M("So... the answer is pain?", [act([("g_shrug", 0)], x=0.4)], "mini_scared_cut", kinetic=[kin("pain?", "PAIN?", 0.5, 0.1, 150, RED)]),
 S_("The answer is gentle holds.", [act([("p_wag", 0), ("g_thumbs", "gentle")])], [kin("gentle", "GENTLE HOLDS", 0.5, 0.1, 130, TEAL)]),
 S_("Push or pull against something for thirty to forty-five seconds, at a level that feels manageable.", WALLP,
    [kin("Push", "PUSH OR PULL", 0.5, 0.08, 110, until="level"), kin("level", "MANAGEABLE", 0.5, 0.08, 110, TEAL)],
    rings=[dict(at="thirty", x=0.5, y=0.2, r=0.08, dur=1.5, max=45, unit="SEC")], tr="dip", d=0.4, sfx=[("thirty", "pop", .3)]),
 S_("Five holds a day.", [act([("p_count", 0)])], counters=[dict(at=0, a=0, b=5, dur=0.5, x=0.5, y=0.1, size=170, color=TEAL, suffix=" HOLDS")]),
 S_("Slow and steady loads rebuild tendons.", [act([("g_thumbs", 0), ("p_flexglow", "rebuild")])], [kin("Slow", "SLOW + STEADY", 0.5, 0.1, 120, TEAL)]),
 S_("If the pain is sharp or getting worse, see a physio.", [act([("p_elbow", 0), ("p_phone", "see")])],
    [kin("sharp", "SHARP PAIN?", 0.5, 0.08, 110, RED), kin("see", "SEE A PHYSIO", 0.5, 0.15, 110, TEAL)], tr="dip", d=0.4),
 M("Which joint hurts? Tell me below.", [act([("p_elbow", 0)], x=0.4)], "s9_mini_point_cut", kinetic=[kin("joint", "WHICH JOINT?", 0.5, 0.1, 130, RED)]),
]
PLAN = plan(6, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day06_v3.mp4")
