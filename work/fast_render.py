# Owner rule (28 Oct): voice at 1.3x and NO silences. The tool's TTS leaves ~0.3-0.5 s pauses between sentences,
# so after `check` makes the voice, this cuts every gap between words down to GAP seconds (voice.wav, words.json and
# segments shifted together), re-sends the plan so its word anchors use the new times, then renders and encodes.
# Usage: python3 fast_render.py <name> <script.txt> <plan.json> [speed] [cover.jpg]  (cover = thumbnail for the first 0.1 s)
import json, os, subprocess, sys, time, urllib.request, wave
MAKER = "/root/.claude/skills/synced/370a525f-40ff-4b1d-a196-a1258fe281e4_33be9e93-4a60-43f2-9228-8bfef809efb4/reel-video-maker/scripts/make_video.py"
TOOL = os.path.expanduser("~/reel-engine-tool"); PORT = 3011; GAP = 0.05
name, script, plan = sys.argv[1:4]; speed = sys.argv[4] if len(sys.argv) > 4 else "1.3"
r = subprocess.run(["python3", MAKER, "check", "--script", script, "--plan", plan, "--name", name, "--speed", speed],
                   capture_output=True, text=True)
if "ERROR" in r.stdout or r.returncode: sys.exit(r.stdout[-2000:])
pdir = os.path.join(TOOL, "public/projects", name)

# --- cut the gaps
wj = json.load(open(os.path.join(pdir, "words.json"))); words = wj["words"]
w = wave.open(os.path.join(pdir, "voice.wav")); prm = w.getparams(); rate = w.getframerate()
audio = w.readframes(w.getnframes()); w.close(); bpf = prm.sampwidth * prm.nchannels
cuts = []  # (start, end) seconds to remove
lead = words[0]["start"]
if lead > GAP: cuts.append((0, lead - GAP))
for a, b in zip(words, words[1:]):
    if b["start"] - a["end"] > 2 * GAP: cuts.append((a["end"] + GAP, b["start"] - GAP))
def shift(t): return t - sum(min(e, t) - s for s, e in cuts if t > s)
out = bytearray(); pos = 0
for s, e in cuts:
    out += audio[int(pos * rate) * bpf:int(s * rate) * bpf]; pos = e
out += audio[int(pos * rate) * bpf:]
w = wave.open(os.path.join(pdir, "voice.wav"), "wb"); w.setparams(prm); w.writeframes(bytes(out)); w.close()
for x in words: x["start"], x["end"] = round(shift(x["start"]), 3), round(shift(x["end"]), 3)
json.dump(wj, open(os.path.join(pdir, "words.json"), "w"))
sp = os.path.join(pdir, "voice.wav.segments.json"); sg = json.load(open(sp))
for x in sg["segments"]:
    x["start"], x["end"] = round(shift(x["start"]), 3), round(shift(x["end"]), 3)
    x["pauses"] = []
json.dump(sg, open(sp, "w"))
print(f"cut {len(cuts)} gaps, {sum(e - s for s, e in cuts):.1f} s removed, voice now {len(out) / bpf / rate:.1f} s")

# --- volumes, plan again, render
pj = os.path.join(pdir, "project.json"); d = json.load(open(pj)); d.update(musicVolume=0.025, sfxVolume=0.35); json.dump(d, open(pj, "w"), indent=1)
def api(path, body=None):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=body, method="POST" if body is not None else "GET",
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read() or b"{}")
if len(sys.argv) > 5:
    cv = sys.argv[5]; api(f"/api/projects/{name}/cover?filename=cover{os.path.splitext(cv)[1]}", open(cv, "rb").read())
res = api(f"/api/projects/{name}/timeline", open(plan, "rb").read())
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
