# DAY 7 v3 "5 Boring Habits Killing Your Testosterone" with THE LONG METHOD engine (9:16)
from w3 import *
def pr(a, n=8, step=0.4, **k): return act(reps(a, a + "_b", n, step), h=k.pop("h", 0.7), **k)
def hab(n, title, color=RED): return [kin(0, f"#{n}", 0.5, 0.06, 130, color), kin(0.1, title, 0.5, 0.14, 100, INK)]
S = [
 S_("Your testosterone isn't low because of bad luck.", [pr("d7_battery", 8, 0.35)], [kin("testosterone", "LOW", 0.5, 0.07, 130, RED), kin("testosterone", "TESTOSTERONE?", 0.5, 0.14, 120, RED)], keys=HOOK, sfx=[(0, "whoosh_big", .2)]),
 S_("It's these five boring habits.", [act([("p_count", 0), ("g_point", "habits.")])], [kin("five", "5 BORING HABITS", 0.5, 0.1, 120, INK)], sfx=[("five", "pop", .3)]),
 M("Boring? I'm boring. Am I doomed?", [act([("p_yawn", 0)], x=0.4)], "mini_scared_cut", kinetic=[kin("doomed?", "DOOMED?", 0.5, 0.1, 140, RED)]),
 S_("One. Sleeping five hours.", [act([("bed_base", 0), ("bed_wake", "five")], h=0.36, y=0.5, puppet=False)], hab(1, "5 HOURS SLEEP"), tr="dip", d=0.4, sfx=[(0, "pop", .3)]),
 S_("Even one week of short sleep can drop it noticeably.", [pr("d7_phone", 8, 0.45)], [kin("week", "1 WEEK", 0.5, 0.08, 110), kin("drop", "= NOTICEABLE DROP", 0.5, 0.15, 100, RED)]),
 S_("Two. Never lifting anything heavy.", [pr("d7_couch", 6, 0.45)], hab(2, "NO HEAVY LIFTING"), sfx=[(0, "pop", .3)]),
 S_("Three. Carrying extra belly fat.", [act([("p_belly", 0)])], hab(3, "BELLY FAT"), sfx=[(0, "pop", .3)]),
 S_("Four. Drinking most weekends.", [pr("d7_beer", 6, 0.4)], hab(4, "WEEKEND DRINKS"), sfx=[(0, "pop", .3)]),
 M("That's my whole personality.", [pr("d7_beer", 6, 0.4, x=0.4)], "mini_laugh_cut"),
 S_("Five. Sitting all day, no sun, no walking.", [pr("d7_desk", 8, 0.45)], hab(5, "SITTING ALL DAY"), sfx=[(0, "pop", .3)]),
 S_("The fix is just as boring.", [act([("p_snap", 0)])], [kin("fix", "THE FIX", 0.5, 0.1, 150, TEAL)], tr="dip", d=0.4),
 S_("Sleep seven to nine hours.", [act([("bed_base", 0)], h=0.36, y=0.5, puppet=False)], [kin(0, "SLEEP 7-9 H", 0.5, 0.1, 130, TEAL)], sfx=[(0, "pop", .3)]),
 S_("Lift three times a week.", [loop("curl_a", "curl_b", 8, 0.3, h=0.6)], [kin(0, "LIFT 3x / WEEK", 0.5, 0.1, 120, TEAL)], sfx=[(0, "pop", .3)]),
 S_("Walk outside daily.", [loop("d5_walk_a", "d5_walk_b", 8, 0.3)], [kin(0, "WALK OUTSIDE", 0.5, 0.1, 130, TEAL)], sfx=[(0, "pop", .3)]),
 M("Which habit are you guilty of? Number in the comments.", [act([("g_point", 0)], x=0.4)], "s9_mini_point_cut",
   kinetic=[kin("habit", "WHICH ONE?", 0.5, 0.1, 130, INK, until="Number"), kin("Number", "COMMENT 1-5", 0.5, 0.1, 130, RED)]),
]
PLAN = plan(7, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day07_v3.mp4")
