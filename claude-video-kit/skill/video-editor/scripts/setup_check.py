#!/usr/bin/env python3
"""Check required tools; print JSON with missing items and OS-specific install commands."""
import json, platform, shutil, subprocess, sys

OS = platform.system()  # Darwin / Windows / Linux


def ver(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip().splitlines()[0]
    except Exception:
        return None


def has_module(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False


INSTALL = {
    "ffmpeg": {"Darwin": "brew install ffmpeg", "Windows": "winget install -e --id Gyan.FFmpeg",
               "Linux": "sudo apt-get install -y ffmpeg"},
    "node": {"Darwin": "brew install node", "Windows": "winget install -e --id OpenJS.NodeJS.LTS",
             "Linux": "sudo apt-get install -y nodejs npm"},
    "faster-whisper": {"*": f"{sys.executable} -m pip install -U faster-whisper"},
    "yt-dlp": {"*": f"{sys.executable} -m pip install -U yt-dlp"},
}
if OS == "Darwin" and not shutil.which("brew"):
    INSTALL["homebrew"] = {"Darwin": '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'}

found, missing = {}, []
for tool, cmd in (("ffmpeg", ["ffmpeg", "-version"]), ("node", ["node", "-v"])):
    v = ver(cmd) if shutil.which(cmd[0]) else None
    if v:
        found[tool] = v
    else:
        missing.append(tool)
if found.get("node"):
    try:
        if int(found["node"].lstrip("v").split(".")[0]) < 18:
            missing.append("node")  # Remotion needs Node 18+
    except ValueError:
        pass
for mod, name in (("faster_whisper", "faster-whisper"), ("yt_dlp", "yt-dlp")):
    (found.__setitem__(name, "installed") if has_module(mod) else missing.append(name))
if "homebrew" in INSTALL and any(m in missing for m in ("ffmpeg", "node")):
    missing.insert(0, "homebrew")

cmds = {m: INSTALL[m].get(OS) or INSTALL[m].get("*") for m in missing}
print(json.dumps({"ok": not missing, "os": OS, "python": sys.version.split()[0],
                  "found": found, "missing": missing, "install": cmds,
                  "note": "After installing ffmpeg/node on Windows, restart the terminal/Claude so PATH updates."},
                 indent=2))
