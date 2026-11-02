# One overview sheet per video: 1 frame/s, 10 columns, timestamp under each tile. usage: overview.py <raw> <analysis>
import csv, os, subprocess, sys
raw, out = sys.argv[1:3]; os.makedirs(os.path.join(out, "overview"), exist_ok=True)
for r in csv.DictReader(open(os.path.join(out, "REFERENCE_INVENTORY.csv"))):
    o = os.path.join(out, "overview", r["id"] + ".jpg")
    if os.path.exists(o): continue
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", os.path.join(raw, r["file"]), "-vf",
                    "fps=1,scale=108:192,drawtext=text='%{eif\\:t\\:d}':x=2:y=2:fontsize=14:fontcolor=red,tile=10x6",
                    "-frames:v", "1", o])
    print(o)
