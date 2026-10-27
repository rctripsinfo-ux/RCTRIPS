# Style-D cards exactly like the approved mockup (text-style-options.png, option D, owner 28 Oct): Bebas Neue,
# mockup panel 270x480 scaled x4 to 1080x1920. One transparent PNG per typed letter so the card types in step with
# the voice (a "poses" flip-book, timed by fast_render.py "sync"). Usage: python3 make_cards.py cards.json
import json, os, subprocess, sys
F = "/root/reel-engine-tool/.cache/ui/bebas-neue-latin-400-normal-6RSG64MI.woff2"
LIB = os.path.expanduser("~/reel-engine-tool/public/library/hero")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
cards = json.load(open(sys.argv[1]))
os.makedirs(OUT, exist_ok=True)
# mockup sizes x4: bumper lines 96px -> 384px (line-height .9); move card "#n" 150 -> 600 (lh .85), name 64 -> 256 (lh .9)
html = """<html><head><style>@font-face{font-family:B;src:url(file://%s)}
body{margin:0;width:1080px;height:1920px;background:transparent;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:B;text-align:center}
.l{white-space:nowrap;display:inline-block}.h{opacity:0}</style></head><body>%s
</body></html>"""
jobs = []
for c in cards:
    total = sum(len(l["text"]) for l in c["lines"])
    for k in range(total + 1):
        n, rows = k, []
        for l in c["lines"]:
            shown, hid = l["text"][:max(0, n)], l["text"][max(0, n):]; n -= len(l["text"])
            rows.append(f'<div><div class="l" style="color:{l["color"]};font-size:{l["size"]}px;line-height:{l.get("lh", .9)}">'
                        f'{shown}<span class="h">{hid}</span></div></div>')
        name = f'card_{c["id"]}_{k:02d}'
        jobs.append((name, html % (F, "".join(rows))))
js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});const J=%s;const fs=require('fs');for(const [n,h] of J){fs.writeFileSync('/tmp/_card.html',h);await p.goto('file:///tmp/_card.html');await p.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('.l').forEach(e=>{let s=parseFloat(e.style.fontSize);while(e.scrollWidth>1000&&s>40){s-=4;e.style.fontSize=s+'px'}})});await p.screenshot({path:'%s/'+n+'.png',omitBackground:true});}await b.close();})()" % (json.dumps(jobs), OUT)
subprocess.run(["node", "-e", js], check=True, cwd="/tmp")
lib = json.load(open(os.path.join(LIB, "library.json"))); have = {i["id"] for i in lib["assets"]}
for name, _ in jobs:
    subprocess.run(["cp", f"{OUT}/{name}.png", f"{LIB}/{name}.png"], check=True)
    if name not in have:
        lib["assets"].append({"id": name, "file": f"{name}.png", "kind": "image", "description": "style-D card frame",
                              "tags": ["card"], "size": [1080, 1920], "bbox": [0, 0, 1, 1], "area": 1.0})
json.dump(lib, open(os.path.join(LIB, "library.json"), "w"), indent=1)
print(len(jobs), "card frames")
