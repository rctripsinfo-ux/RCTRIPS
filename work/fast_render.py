# Owner rule (28 Oct): voice at 1.3x and NO silences. The tool's TTS leaves ~0.3-0.5 s pauses between sentences,
# so after `check` makes the voice, this cuts every gap between words down to GAP seconds (voice.wav, words.json and
# segments shifted together), re-sends the plan so its word anchors use the new times, then renders and encodes.
# Usage: python3 fast_render.py <name> <script.txt> <plan.json> [speed] [cover.jpg]  (cover = thumbnail for the first 0.1 s)
import json, os, subprocess, sys, time, urllib.request, wave
MAKER = (__import__("glob").glob("/root/.claude/skills/*/*/reel-video-maker/scripts/make_video.py") + [__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "reel-video-maker/scripts/make_video.py")])[0]  # any account, else work/reel-video-maker
TOOL = os.path.expanduser("~/reel-engine-tool"); PORT = 3011; GAP = 0.05
name, script, plan = sys.argv[1:4]; speed = sys.argv[4] if len(sys.argv) > 4 else "1.3"
r = subprocess.run(["python3", MAKER, "check", "--script", script, "--plan", plan, "--name", name, "--speed", speed],
                   capture_output=True, text=True)
if "ERROR" in r.stdout or r.returncode: sys.exit(r.stdout[-2000:])
pdir = os.path.join(TOOL, "public/projects", name)

# --- re-time the gaps: never dead air, but a short natural breath at sentence ends, and longer holds where the
# plan asks for them (<plan>.pauses.json, e.g. {"fix.": 0.7}) so bumper cards and their typing sound finish cleanly.
wj = json.load(open(os.path.join(pdir, "words.json"))); words = wj["words"]
w = wave.open(os.path.join(pdir, "voice.wav")); prm = w.getparams(); rate = w.getframerate()
audio = w.readframes(w.getnframes()); w.close(); bpf = prm.sampwidth * prm.nchannels
pp = os.path.splitext(plan)[0] + ".pauses.json"
HOLD = json.load(open(pp)) if os.path.exists(pp) else {}
def want(word):
    t = word["text"]
    if "_gap" in HOLD: return HOLD["_gap"]  # Day-1 (forearms V1) format: every gap cut to the same tiny gap
    if t in HOLD: return HOLD[t]
    if t[-1:] in ".?!:": return 0.22
    if t[-1:] in ",;": return 0.1
    return 0.04
def chunk(t0, t1): return audio[int(t0 * rate) * bpf:int(t1 * rate) * bpf]
def silence(sec): return bytes(int(sec * rate) * bpf)
out = bytearray(silence(0.05)); new = []; t = 0.05
for i, x in enumerate(words):
    s0, e0 = x["start"], x["end"]
    out += chunk(s0, e0); new.append((t, t + e0 - s0)); t += e0 - s0
    nxt = words[i + 1]["start"] if i + 1 < len(words) else e0 + 0.3
    g = nxt - e0
    gw = 0.3 if i + 1 == len(words) else (HOLD[x["text"]] if x["text"] in HOLD else min(g, want(x)))  # only holds add time
    if gw <= g: out += chunk(e0, e0 + gw)
    else: out += chunk(e0, nxt) + silence(gw - g)
    t += gw
old_len = len(audio) / bpf / rate
for x, (s1, e1) in zip(words, new): x["start"], x["end"] = round(s1, 3), round(e1, 3)
w = wave.open(os.path.join(pdir, "voice.wav"), "wb"); w.setparams(prm); w.writeframes(bytes(out)); w.close()
json.dump(wj, open(os.path.join(pdir, "words.json"), "w"))
# segments: rebuild from the words (one per sentence)
sp = os.path.join(pdir, "voice.wav.segments.json"); sg = json.load(open(sp)); k = 0
for x in sg["segments"]:
    n = len(x["text"].split()); x["start"], x["end"] = words[k]["start"], words[min(k + n, len(words)) - 1]["end"]; x["pauses"] = []; k += n
json.dump(sg, open(sp, "w"))
print(f"voice {old_len:.1f} s -> {len(out) / bpf / rate:.1f} s (holds: {HOLD})")

# --- volumes, plan again, render
pj = os.path.join(pdir, "project.json"); d = json.load(open(pj)); d.update(musicVolume=0.025, sfxVolume=0.35); json.dump(d, open(pj, "w"), indent=1)
def api(path, body=None):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=body, method="POST" if body is not None else "GET",
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read() or b"{}")
if len(sys.argv) > 5:
    cv = sys.argv[5]; api(f"/api/projects/{name}/cover?filename=cover{os.path.splitext(cv)[1]}", open(cv, "rb").read())
# typed cards in sync with the voice: a text layer with "sync": "<spoken words>" types its letters over exactly the
# time those words are spoken, with a typing sound of the same length (sfx_typing_03 .. _25 = 0.3 .. 2.5 s).
import re as _re
def norm(t): return _re.sub(r"[^a-z0-9']", "", t.lower())
toks = [norm(x["text"]) for x in words]
def span(phrase):
    q = [norm(t) for t in phrase.split()]
    for i in range(len(toks) - len(q) + 1):
        if toks[i:i + len(q)] == q: return words[i]["start"], words[i + len(q) - 1]["end"]
    sys.exit(f"sync phrase not found: {phrase}")
P = json.load(open(plan))
for sc_ in P["scenes"]:
    for L in sc_["layers"]:
        ph = L.pop("sync", None)
        if not ph: continue
        if L.get("type") == "poses":
            # style-D card flip-book: frame k shows k letters; each line types while its own words are spoken
            cid, steps = L.pop("card"), L.pop("steps"); fr = []; k = 0
            for phrase, nlet in zip(ph, steps):
                a, b = span(phrase); dur = max(0.3, b - a)
                for j in range(nlet):
                    k += 1; fr.append({"asset": f"card_{cid}_{k:02d}", "at": round(a - 0.03 + 0.8 * dur * j / nlet, 3)})  # done typing at 80% so the full card is seen
                P.setdefault("sfx", []).append({"at": round(a - 0.03, 3), "src": f"sfx_typing_{min(25, max(3, round(dur * 10))):02d}", "volume": 1.0})
            L.update(frames=fr, at=fr[0]["at"])
            continue
        a, b = span(ph); dur = max(0.3, b - a)
        L.update(at=round(a - 0.03, 3), animation="typewriter", cps=round(max(2, len(L["text"].replace(" ", "")) / dur), 2))
        P.setdefault("sfx", []).append({"at": round(a - 0.03, 3), "src": f"sfx_typing_{min(25, max(3, round(dur * 10))):02d}", "volume": 1.0})
res = api(f"/api/projects/{name}/timeline", json.dumps(P).encode())
if not res.get("ok"): sys.exit(f"plan refused: {res}")
api(f"/api/projects/{name}/render", b"{}")
while True:
    s = api(f"/api/projects/{name}/render")
    if s.get("state") in ("done", "error"): break
    time.sleep(8)
if s["state"] != "done": sys.exit(f"render failed: {s.get('error')}")
final = os.path.abspath(f"final/{name}.mp4")
raw = os.path.join(TOOL, "out", f"{name}.mp4")
J = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
j = json.loads(J[J.rindex("{"):J.rindex("}") + 1])
af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", raw, "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-af", af,
                "-ar", "48000", "-c:a", "aac", "-b:a", "192k", final], check=True)
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", final, "-vf", "fps=1,scale=216:-1,tile=8x6", "-frames:v", "1",
                f"final/{name}-frames.jpg"], check=True)
print("DONE", final)
