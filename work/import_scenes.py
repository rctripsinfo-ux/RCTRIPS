# Imports scene images (character/scenes/dNN_*.webp) into the Reel Engine library:
# WHITE ones -> cutout + body points (tools/import_one.py) + clean_cutout.py; SCENE ones -> full-frame image entry.
# usage: python3 import_scenes.py 4 [5 ...]
import csv, json, os, subprocess, sys
W = os.path.dirname(os.path.abspath(__file__)); T = os.path.expanduser("~/reel-engine-tool"); LIB = f"{T}/public/library/hero"
kind = {r["file_name"][:-4]: r["type"] for r in csv.DictReader(open(f"{W}/flow/ALL-PROMPTS.csv"))}
for d in map(int, sys.argv[1:]):
    ids = sorted(f[:-5] for f in os.listdir(f"{W}/character/scenes") if f.startswith(f"d{d:02d}_") and f.endswith(".webp"))
    from PIL import Image
    import numpy as np
    def is_white(i):  # decide from the picture itself (border pixels), not from the prompt version
        a = np.asarray(Image.open(f"{W}/character/scenes/{i}.webp").convert("L")).astype(int)
        return np.concatenate([a[:8].ravel(), a[-8:].ravel(), a[:, :8].ravel(), a[:, -8:].ravel()]).mean() > 235
    white = [i for i in ids if is_white(i)]; full = [i for i in ids if not is_white(i)]
    for i in white:
        subprocess.run(["python3", "tools/import_one.py", f"{W}/character/scenes/{i}.webp", "public/library/hero", f"sc_{i}", "character", f"H scene {i}"],
                       cwd=T, check=True, capture_output=True)
    if white: subprocess.run(["python3", f"{W}/clean_cutout.py", *[f"sc_{i}" for i in white]], check=True, capture_output=True)
    lib = json.load(open(f"{LIB}/library.json")); have = {a["id"] for a in lib["assets"]}
    from PIL import Image
    for i in full:
        im = Image.open(f"{W}/character/scenes/{i}.webp"); im.save(f"{LIB}/sc_{i}.webp", "WEBP", quality=88)
        lib["assets"] = [a for a in lib["assets"] if a["id"] != f"sc_{i}"] + [{"id": f"sc_{i}", "file": f"sc_{i}.webp", "kind": "image",
            "description": f"H full scene {i}", "tags": ["scene"], "size": list(im.size), "bbox": [0, 0, 1, 1], "area": 1.0}]
    json.dump(lib, open(f"{LIB}/library.json", "w"), indent=1)
    print(f"day {d}: {len(white)} cutouts, {len(full)} full scenes")
