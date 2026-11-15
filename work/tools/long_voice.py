# usage: python3 tools/long_voice.py <name> <script.txt>
# Long videos: the script has "## CHAPTER" headers. Each chapter is voiced by dialogue_voice.py on its own
# (a short TTS call stays stable), then all chapters are joined into voice/<name>_cut.wav + words.json.
import json, os, subprocess, sys, wave, numpy as np
from concurrent.futures import ThreadPoolExecutor
name, script = sys.argv[1:3]; W = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(W)
chs, cur = [], None
for l in open(script):
    l = l.strip()
    if l.startswith("## "): cur = []; chs.append(cur)
    elif l[:3] in ("H: ", "M: ") and cur is not None: cur.append(l)
os.makedirs(f"voice/{name}_ch", exist_ok=True)
def go(i):
    n = f"{name}_ch{i:02d}"; txt = f"voice/{name}_ch/{n}.txt"; open(txt, "w").write("\n".join(chs[i]))
    if not os.path.exists(f"voice/{n}_cut.wav"):
        for k in range(3):
            if subprocess.run(["python3", "tools/dialogue_voice.py", n, txt]).returncode == 0: break
    return n
subprocess.run(["python3", "-c", "import urllib.request;urllib.request.urlopen('http://127.0.0.1:3011/',timeout=3)"], capture_output=True)
with ThreadPoolExecutor(3) as ex: names = list(ex.map(go, range(len(chs))))
out, words, t, rate = [], [], 0.0, None
for n in names:
    f = wave.open(f"voice/{n}_cut.wav"); rate = f.getframerate(); a = np.frombuffer(f.readframes(f.getnframes()), np.int16)
    words += [dict(w, start=round(w["start"] + t, 3), end=round(w["end"] + t, 3)) for w in json.load(open(f"voice/{n}_cut.words.json"))["words"]]
    out += [a, np.zeros(int(0.45 * rate), np.int16)]; t += len(a) / rate + 0.45
f = wave.open(f"voice/{name}_cut.wav", "w"); f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate); f.writeframes(np.concatenate(out).tobytes()); f.close()
json.dump({"words": words}, open(f"voice/{name}_cut.words.json", "w")); print(f"{name}: {t:.1f} s, {len(words)} words, {len(chs)} chapters")
