# "How Many Squats Should You Do Based on Your AGE?" in the Zenox age-tier format (ref/ analysis of R04, 3.1M views):
# close-up hook -> exercise on the floor -> per age: AGE tag + H standing (rise-in) -> exercise loop + heavy black heading
# -> one sunburst reveal beat -> rule -> "AGE? / SQUATS?" comment bait. Our own script, our H, WHITE room (owner, 2 Nov).
# Assets: zenox_assets.py. Motion: enter "rise" (tool-patches/motion.js, measured from the reference).
import json

FEET = 0.84  # floor line where H stands (floor band starts at 0.72)


def H(w):  # centre y so the feet land on FEET (hero images are 768x1376, figure fills ~97%)
    return round(FEET - w * 1.0078 * 0.485, 3)


def img(a, at, until=None, enter="rise", **kw):
    d = {"type": "image", "asset": a, "at": at, "enter": enter, "shadow": a.startswith("hero_"), "autoPlace": False, **kw}
    if until: d["until"] = until
    return d


def bg(at, a="bg_white_floor"): return img(a, at, enter="cut", width=1.0, x=0.5, y=0.5)


def squat(at, w=0.62, n=24):
    # side-view squat: top / mid drawings swapped every 0.35 s (pose loop, no clips)
    fr = [{"asset": ("hero_squat_top", "hero_squat_mid")[k % 2], "at": at if k == 0 else f"{at}+{round(k * 0.35, 2)}"} for k in range(n)]
    return {"type": "poses", "frames": fr, "at": at, "enter": "rise", "shadow": True, "autoPlace": False, "width": w, "x": 0.5, "y": H(w)}


def head(slug, at): return img("head_" + slug, at, enter="up", width=0.78, x=0.5, y=0.14)
def tag(a, at, x=0.21, y=0.075, w=0.34): return img(a, at, enter="pop", width=w, x=x, y=y)
def sc(id, start, layers, camera=None):
    d = {"id": id, "start": start, "backdrop": "none", "layers": layers}
    if camera: d["camera"] = camera
    return d


def punch(at, z=1.04): return [{"at": at, "zoom": 1}, {"at": f"{at}+0.2", "zoom": z}]


AGES = [  # (scene id, start phrase, tag, H width standing, range phrase, heading slug)
    ("a10", "At age ten", "tag_age_10", 0.40, "fifteen to twenty", "15_20_squats"),
    ("a20", "At twenty", "tag_age_20", 0.56, "forty to fifty", "40_50_squats"),
    ("a30", "In your thirties", "tag_age_30", 0.56, "thirty to forty", "30_40_squats"),
    ("a40", "At forty", "tag_age_40", 0.56, "twenty five to", "25_35_squats"),
    ("a50", "At fifty", "tag_age_50", 0.56, "twenty to thirty", "20_30_squats"),
    ("a60", "over sixty", "tag_age_60", 0.56, "ten to twenty", "10_20_squats"),
]

scenes = [
    sc("hook", "start", [bg("start", "bg_white_floor"),
                         img("hero_point_viewer", "start", "based on your", enter="cut", width=1.5, x=0.5, y=0.78),
                         ], camera=punch("start", 1.05)),
    sc("hook2", "based on your-0.05", [bg("based on your"), squat("based on your")]),
    sc("find", "Let's find out-0.05", [bg("Let's find out"), img("hero_count_1", "Let's find out", width=1.0, x=0.5, y=0.66)]),
]
for i, (sid, start, t, w, rng, slug) in enumerate(AGES):
    L = [bg(f"{start}-0.05"), tag(t, f"{start}-0.05"),
         img("hero_stand", f"{start}-0.05", rng, width=w, x=0.5, y=H(w)),
         squat(rng), head(slug, rng)]
    scenes.append(sc(sid, f"{start}-0.05", L, camera=punch(rng)))
    if sid == "a20":  # reveal beat on the peak age (R04 did it after age 15/20): sunburst + sunglasses
        scenes.append(sc("peak", "Your legs are-0.05", [bg("Your legs are", "bg_sunburst"),
                                                       img("gag_sunglasses_thumbs", "Your legs are", width=0.9, x=0.5, y=0.6)],
                         camera=punch("strongest", 1.05)))
    if sid == "a60":
        scenes.append(sc("beat", "you're beating-0.05", [bg("you're beating"),
                                                         img("hero_arms_crossed", "you're beating", width=0.95, x=0.5, y=0.66)]))
scenes += [
    sc("rule", "Remember-0.05", [bg("Remember"), img("hero_count_1", "Remember", width=1.0, x=0.5, y=0.66)], camera=punch("one deep slow")),
    sc("cta", "Now be honest-0.05", [bg("Now be honest"),
                                     img("hero_confused_scratch", "Now be honest", width=0.66, x=0.5, y=H(0.66)),  # smaller: tags stay clear of the head
                                     tag("tag_age_q", "How old", x=0.42, y=0.07, w=0.3),
                                     tag("tag_squats_q", "squats can you", x=0.6, y=0.13, w=0.36)]),
]

whoosh = [s["start"] for s in scenes if s["id"] != "hook"]
plan = {
    "title": "How Many Squats Should You Do Based on Your AGE?",
    "canvas": {"background": "#FFFFFF"},
    "captions": {"mode": "phrase", "look": "clean", "size": 50, "y": 0.6, "maxWords": 1, "keywords": []},
    "scenes": scenes,
    "sfx": [{"at": a, "src": "sfx_whoosh_soft"} for a in whoosh] +
           [{"at": f"{a[1]}-0.05", "src": "sfx_pop_soft"} for a in AGES] +
           [{"at": a[4], "src": "sfx_pop_soft"} for a in AGES] +
           [{"at": "Your legs are", "src": "sfx_ding"}, {"at": "How old", "src": "sfx_pop_soft"}, {"at": "squats can you", "src": "sfx_pop_soft"}],
}
json.dump(plan, open("zenox.json", "w"), indent=1, ensure_ascii=False)
