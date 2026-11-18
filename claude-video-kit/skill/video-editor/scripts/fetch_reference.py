#!/usr/bin/env python3
"""Download a reference video (Instagram/YouTube/TikTok link) into references/."""
import argparse, json, os, sys

p = argparse.ArgumentParser()
p.add_argument("url")
p.add_argument("--out", default="references")
p.add_argument("--cookies-from-browser", help="e.g. chrome, firefox (helps with Instagram)")
a = p.parse_args()

try:
    import yt_dlp
except ImportError:
    sys.exit(json.dumps({"ok": False, "error": "yt-dlp not installed. Run: pip install -U yt-dlp"}))

os.makedirs(a.out, exist_ok=True)
opts = {"outtmpl": os.path.join(a.out, "%(uploader_id|ref)s_%(id)s.%(ext)s"),
        "format": "mp4/bestvideo*+bestaudio/best", "merge_output_format": "mp4",
        "quiet": True, "noprogress": True}
if a.cookies_from_browser:
    opts["cookiesfrombrowser"] = (a.cookies_from_browser,)
try:
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(a.url, download=True)
        path = y.prepare_filename(info)
        if not path.endswith(".mp4") and os.path.exists(os.path.splitext(path)[0] + ".mp4"):
            path = os.path.splitext(path)[0] + ".mp4"
    print(json.dumps({"ok": True, "file": path, "title": info.get("title"), "duration": info.get("duration")}))
except Exception as e:
    print(json.dumps({"ok": False, "error": str(e)[:300],
                      "hint": "Retry with --cookies-from-browser chrome, or ask the user to download the reel and drop it in references/."}))
