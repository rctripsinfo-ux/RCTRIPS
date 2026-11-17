# DAY 5 v3 "Do This 10-Minute Walk After You Eat" with THE LONG METHOD engine (9:16)
from w3 import *
WALK = lambda **k: loop("d5_walk_a", "d5_walk_b", 30, 0.32, **k)
SIT = dict(x=0.5, y=0.84, w=0.5, h=0.2, labels=["0", "30", "60", "90"], show_values=False)
S = [
 S_("You just ate.", [act([("d5_meal", 0)] + reps("d5_meal_b", "d5_meal", 6, 0.22, 0.2), h=0.7)], [kin(0, "YOU JUST ATE.", 0.5, 0.1, 120)], keys=HOOK, sfx=[(0, "whoosh_big", .2)]),
 S_("Don't sit.", [act([("p_wag", 0)])], [kin(0, "DON'T SIT.", 0.5, 0.1, 150, RED)], keys=DRIFT + [("sit.", 1.04, .5, .45), ("sit.+0.1", 1.1, .5, .42)], shake=[("sit.", .04)], sfx=[("sit.", "pop", .3)]),
 S_("This is the laziest fat-loss trick there is.", [act([("g_point", 0), ("p_ominous", "laziest"), ("g_thumbs", "trick")])],
    [kin("laziest", "THE LAZIEST", 0.5, 0.08, 100, INK), kin("fat-loss", "FAT-LOSS TRICK", 0.5, 0.15, 110, TEAL)], sfx=[("laziest", "pop", .3)]),
 M("Walking? That's not exercise.", [act([("p_offended", 0)], x=0.4)], "s6_mini_squint_cut", kinetic=[kin("not", "NOT EXERCISE?", 0.5, 0.1, 120, RED)]),
 S_("A ten-minute walk right after a meal", [WALK()], [kin("ten-minute", "10-MIN WALK", 0.5, 0.1, 120, TEAL)],
    rings=[dict(at="ten-minute", x=0.82, y=0.25, r=0.08, dur=0.8, max=10, unit="MIN")], tr="dip", d=0.4, sfx=[("ten-minute", "pop", .3)]),
 S_("helps your muscles soak up the sugar from that meal,", [act([("g_flex", 0), ("p_flexglow", "muscles")])], [kin("muscles", "MUSCLES", 0.5, 0.08, 110, TEAL), kin("sugar", "SOAK UP SUGAR", 0.5, 0.15, 110, RED)]),
 S_("so your blood sugar spikes less.", [act([("g_think", 0), ("g_thumbs", "less.")], x=0.5, y=0.38, h=0.4)],
    [kin(0, "BLOOD SUGAR", 0.5, 0.08, 110), kin("less.", "SPIKES LESS", 0.5, 0.15, 110, TEAL)],
    bars=[dict(at=0, until="less.", values=[3, 10, 7, 4], stagger=0.12, color=RED, **SIT), dict(at="less.+0.2", values=[3, 6, 5, 4], stagger=0.06, color=TEAL, **SIT)]),
 S_("Do it after your biggest meal every day.", [act([("p_full", 0), ("g_thumbs", "every")])], [kin("biggest", "AFTER YOUR", 0.5, 0.08, 100), kin("biggest", "BIGGEST MEAL", 0.5, 0.15, 120, RED)], tr="dip", d=0.4),
 S_("That's seventy extra minutes of moving every week, without a single workout.", [WALK(y=0.6, h=0.55)],
    [kin("without", "0 WORKOUTS", 0.5, 0.18, 100, TEAL)], counters=[dict(at=0, a=0, b=70, dur=0.9, x=0.5, y=0.08, size=150, color=INK, suffix=" MIN", stroke=8)]),
 M("Can I walk to the fridge?", [world("bk_kitchen"), act([("d5_fridge", 0), ("d5_fridge_b", "walk"), ("d5_fridge", "fridge?")], x=0.4, h=0.7)], "mini_laugh_cut",
   kinetic=[kin("fridge?", "THE FRIDGE?", 0.5, 0.1, 120, WHITE, stroke=10, stroke_fill=INK)]),
 S_("You can walk past it.", [world("bk_kitchen"), WALK(y=0.58, h=0.62)], [kin("past", "WALK PAST IT", 0.5, 0.1, 120, WHITE, stroke=10, stroke_fill=INK)], sfx=[("past", "pop", .3)]),
 S_("Ten minutes. After meals. Every day.", [act([("g_one", 0), ("p_timer", "After"), ("g_thumbs", "Every")])],
    [kin(0, "10 MIN", 0.5, 0.07, 100, TEAL), kin("After", "AFTER MEALS", 0.5, 0.13, 100, INK), kin("Every", "EVERY DAY", 0.5, 0.19, 100, RED)], tr="dip", d=0.4,
    sfx=[(0, "pop", .3), ("After", "pop", .3), ("Every", "pop", .3)]),
 M("Which meal are you walking after? Tell me below.", [act([("g_point", 0)], x=0.4)], "s9_mini_point_cut", kinetic=[kin("meal", "WHICH MEAL?", 0.5, 0.1, 130, RED)]),
]
PLAN = plan(5, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day05_v3.mp4")
