# Re-masters finished videos to a new loudness WITHOUT re-rendering (uses the tool's raw render in ~/reel-engine-tool/out).
# usage: LUFS=-13 python3 relouden.py day04 day07 ...
import json, os, subprocess, sys
LUFS = os.environ.get("LUFS", "-13"); OUT = os.path.expanduser("~/reel-engine-tool/out")
for n in sys.argv[1:]:
    raw, final = f"{OUT}/{n}.mp4", f"final/{n}.mp4"
    J = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", raw, "-af", f"loudnorm=I={LUFS}:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(J[J.rindex("{"):J.rindex("}") + 1])
    af = (f"loudnorm=I={LUFS}:TP=-1.0:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
          f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", raw, "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-af", af,
                    "-ar", "48000", "-c:a", "aac", "-b:a", "192k", final], check=True)
    I = subprocess.run(["ffmpeg", "-nostdin", "-i", final, "-af", "ebur128", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
    print(n, "->", [l.strip() for l in I.splitlines() if l.strip().startswith("I:")][-1])
