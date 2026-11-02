# Phase 1: technical inventory of every reference video (ffprobe only, no AI). Cached by sha1.
# usage: python3 -I ref/tools/inventory.py <raw_dir> <out_dir>
import csv, hashlib, json, os, subprocess, sys
raw, out = sys.argv[1:3]
TOOL_VER = "inventory-1"
cache_p = os.path.join(out, "inventory_cache.json")
cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
rows = []
srts = os.listdir(os.path.join(raw, "script")) if os.path.isdir(os.path.join(raw, "script")) else []
for k, fn in enumerate(sorted(f for f in os.listdir(raw) if f.endswith(".mp4"))):
    p = os.path.join(raw, fn); h = sha1(p)
    if cache.get(fn, {}).get("sha1") == h and cache[fn].get("ver") == TOOL_VER:
        rows.append(cache[fn]["row"]); continue
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", p],
                                   capture_output=True, text=True).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next((s for s in pr["streams"] if s["codec_type"] == "audio"), {})
    num, den = map(int, v["avg_frame_rate"].split("/"))
    title = fn[:-4]
    key = title.replace("_", "").replace("?", "").lower()
    srt = [s for s in srts if key[:30] in s.replace("?", "").lower()]
    row = {"id": f"R{k + 1:02d}", "file": fn, "sha1": h[:12], "duration_s": round(float(pr["format"]["duration"]), 2),
           "width": v["width"], "height": v["height"], "fps": round(num / den, 3), "frames": v.get("nb_frames", ""),
           "vcodec": v["codec_name"], "vbitrate_kbps": round(int(v.get("bit_rate", 0)) / 1000),
           "acodec": a.get("codec_name", "none"), "a_channels": a.get("channels", 0), "a_rate": a.get("sample_rate", ""),
           "size_mb": round(os.path.getsize(p) / 1e6, 2), "srt": " | ".join(srt)}
    cache[fn] = {"sha1": h, "ver": TOOL_VER, "row": row}; rows.append(row)
rows.sort(key=lambda r: r["id"])
# view counts from `yt-dlp --flat-playlist -J <channel>/shorts > channel_shorts.json` (optional)
chp = os.path.join(out, "channel_shorts.json")
if os.path.exists(chp):
    views = {e["title"][:25].lower(): e.get("view_count") for e in json.load(open(chp)).get("entries", [])}
    for r in rows: r["views"] = views.get(r["file"][:-4].replace("_", "?")[:25].lower(), "")
with open(os.path.join(out, "REFERENCE_INVENTORY.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
json.dump(cache, open(cache_p, "w"), indent=1)
for r in rows: print(r["id"], r["duration_s"], f'{r["width"]}x{r["height"]}', r["fps"], r["vcodec"], r["vbitrate_kbps"], r["acodec"], "srt" if r["srt"] else "NO-SRT", r["file"][:60])
