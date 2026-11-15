# DAY 7 "5 Boring Habits Killing Your Testosterone"
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w1 import *
from director import render
S = [
 dict(text="Your testosterone isn't low because of bad luck.", poses=[], layers=[full("d7_battery")], labels=[lab("testosterone", "LOW TESTOSTERONE?", y=0.14)],
      keys=hook_keys((.5, .3)), shake=[("luck.", .04)], sfx=[(0, "whoosh_big", .2), ("testosterone", "pop", .3)]),
 dict(text="It's these five boring habits.", poses=[], tr="cut", layers=[full("d7_battery")], labels=[lab("five", "5 BORING HABITS", y=0.14)],
      keys=[(0, 1.0, .5, .5)] + punch("five", 1.0, 1.1, (.5, .45)), sfx=[("five", "pop", .3)]),
 dict(text="Boring? I'm boring. Am I doomed?", poses=[], tr="cut", layers=[full("d7_battery"), mini("mini_scared_cut")], keys=[(0, 1.1, .5, .45)], sfx=[(0, "pop_soft", .3)]),
 dict(text="One. Sleeping five hours. Even one week of short sleep can drop it noticeably.", poses=[], tr="brush", d=0.3, layers=[full("d7_phone")],
      labels=[lab("Sleeping", "1  ONLY 5 HOURS OF SLEEP", y=0.14)], keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)], sfx=[("Sleeping", "pop", .3)]),
 dict(text="Two. Never lifting anything heavy.", poses=[], tr="squash", d=0.37, layers=[full("d7_couch")], labels=[lab("Never", "2  NO HEAVY LIFTING", y=0.14)],
      keys=[(0, 1.0, .5, .5)], sfx=[("Never", "pop", .3)]),
 dict(text="Three. Carrying extra belly fat.", poses=[], tr="squash", d=0.37, layers=[full("d7_belly")], labels=[lab("Carrying", "3  EXTRA BELLY FAT", y=0.14)],
      keys=[(0, 1.0, .5, .5)], sfx=[("Carrying", "pop", .3)]),
 dict(text="Four. Drinking most weekends.", poses=[], tr="squash", d=0.37, layers=[full("d7_beer")], labels=[lab("Drinking", "4  WEEKEND DRINKING", y=0.14)],
      keys=[(0, 1.0, .5, .5)], sfx=[("Drinking", "pop", .3)]),
 dict(text="That's my whole personality.", poses=[], tr="cut", layers=[full("d7_beer"), mini("mini_laugh_cut")], keys=[(0, 1.0, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Five. Sitting all day, no sun, no walking.", poses=[], tr="squash", d=0.37, layers=[full("d7_desk")], labels=[lab("Sitting", "5  SITTING ALL DAY", y=0.14)],
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[("Sitting", "pop", .3)]),
 dict(text="The fix is just as boring. Sleep seven to nine hours. Lift three times a week. Walk outside daily.", poses=[], tr="brush", d=0.3, layers=[full("d7_sunwalk")],
      labels=stack([("Sleep", "SLEEP 7-9 HOURS"), ("Lift", "LIFT 3x / WEEK"), ("Walk", "WALK OUTSIDE DAILY")], y0=0.1),
      particles=[dict(at="daily.", x=0.5, y=0.45, spread=0.5)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)],
      sfx=[("Sleep", "pop", .3), ("Lift", "pop", .3), ("Walk", "pop", .3), ("daily.", "chime", .4)]),
 dict(text="Which habit are you guilty of? Number in the comments.", poses=[], tr="cut", layers=[full("d7_sunwalk"), mini("s9_mini_point_cut")], keys=[(0, 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)]),
]
PLAN = plan(7, S)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day07.mp4")
