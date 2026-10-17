import sys
sys.path.insert(0, "/root/.claude/skills/synced/370a525f-40ff-4b1d-a196-a1258fe281e4_33be9e93-4a60-43f2-9228-8bfef809efb4/reel-video-maker/scripts")
from plan_lib import *


def outline(t, at, until=None, y=0.19, size=None, c=B):
    d = {"type": "text", "text": t, "look": "outline", "behind": True, "x": 0.5, "y": y, "size": size or 200, "color": c,
         "align": "center", "maxWidth": 1, "animation": "none", "untype": False, "tilt": 0, "at": at}
    if until: d["until"] = until
    return d

# text looks rotate so no two beats in a row use the same style (owner, 17 Oct)
make("skinnyfat", "Skinny arms but a soft belly? That's skinny fat",
     ["skinny", "fat", "belly", "neither", "maintenance", "protein", "push-ups", "squats", "rows", "rep", "three", "arms"],
     ["Dieting makes you", "Send this to"], [
    auto("hook", "start", "none", [
        b("start", "SKINNY FAT", "marquee", clip="clip_pushup", rate=1.3),
        b("but a soft belly", "SOFT BELLY", "echo", c=R, img="hero_beginner", impact_=True, size=200),
        b("That's skinny fat", None, img="hero_measuring_waist", tape="SKINNY FAT", tapec=R),
    ], hook=True, shakes=["but a soft belly"]),
    auto("myth", "Dieting makes you-0.1", "red", [
        b("Dieting makes you", "SKINNIER", c=R, img="hero_beginner_v2"),
        b("Bulking makes you", "FATTER", "echo", c=R, img="hero_eating", impact_=True),
        b("Do neither", None, img="hero_stop_palm", tape="DO NEITHER"),
    ]),
    auto("eat", "Eat at maintenance-0.1", "green", [
        b("Eat at maintenance", None, img="hero_cooking", pos="stand",
          extra=[outline("MAINTENANCE", "Eat at maintenance", "with protein in every meal", size=150)]),
        b("with protein in every meal", "PROTEIN", "echo", c=G, img="hero_eating_v2", prop="prop_protein_food"),
        b("eggs, dal or chicken", "EGGS • DAL • CHICKEN", "marquee", c=G, img="hero_cooking", prop="prop_eggs", y=0.2, pos="stand"),
    ]),
    auto("do", "Train full body-0.1", "none", [
        b("Train full body", "3X A WEEK", clip="clip_pushup", rate=1.0),
        b("push-ups, squats", "PUSH-UPS", "marquee", clip="clip_pushup", rate=1.3),
        b("squats and rows", None, clip="clip_squat", rate=1.3,
          extra=[outline("SQUATS", "squats and rows", "rows", size=220)]),
        b("rows", "ROWS", clip="clip_inverted_row", rate=1.2),
        b("three sets of eight", None, clip="clip_inverted_row", rate=1.2,
          extra=[outline("8-12", "three sets of eight", y=0.17, size=280)]),
    ]),
    auto("plan", "Add one rep-0.1", "grid", [
        b("Add one rep", "+1 REP", "echo", c=G, img="hero_clipboard", size=230),
        b("In three months", "3 MONTHS", img="hero_counting_fingers"),
        b("your belly shrinks", None, img="hero_measuring_waist", tape="BELLY SHRINKS"),
        b("while your arms grow", "ARMS UP", "echo", c=G, img="hero_double_biceps", impact_=True, size=220),
    ], tr="zoom"),
    cta("hero_beginner", "skinny friend with a belly", "SKINNY + BELLY", "SKINNY FAT...", echo_at="Because skinny fat"),
], [("but a soft belly", "sfx_hammer"), ("Bulking makes you", "sfx_bruh"), ("Do neither", "sfx_get_out"),
    ("with protein in every meal", "sfx_ding"), ("push-ups, squats", "sfx_whip"), ("rows", "sfx_click"),
    ("eight to twelve", "sfx_counter"), ("every week", "sfx_coin"), ("In three months", "sfx_few_moments_later"),
    ("while your arms grow", "sfx_fahhh_pump")],
    "skinny friend with a belly", "Because skinny fat")
