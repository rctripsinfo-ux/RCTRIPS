#!/usr/bin/env python3
"""Remove silences, filler words and chosen ranges using a words.json transcript.
Writes cut video + cut_words.json (word times re-mapped to the new timeline) + cuts.json."""
import argparse, json, os, re, subprocess

FILLERS = {"um", "umm", "uh", "uhh", "uhm", "hmm", "hm", "erm", "ah", "aa", "aah", "mm"}


def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("words")
    p.add_argument("--out", required=True)
    p.add_argument("--max-gap", type=float, default=0.35, help="pauses longer than this are cut (sec)")
    p.add_argument("--pad", type=float, default=0.06, help="padding kept around speech (sec)")
    p.add_argument("--drop", action="append", default=[], help="extra range to remove, e.g. 3.2-7.8 (repeatable)")
    p.add_argument("--keep-fillers", action="store_true")
    a = p.parse_args()

    data = json.load(open(a.words, encoding="utf-8"))
    dur = data.get("duration") or float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
        capture_output=True, text=True).stdout)
    drops = [tuple(map(float, d.split("-"))) for d in a.drop]

    def dropped(w):
        return any(s <= (w["s"] + w["e"]) / 2 <= e for s, e in drops)

    words = [w for w in data["words"] if not dropped(w) and (a.keep_fillers or norm(w["w"]) not in FILLERS)]
    if not words:
        raise SystemExit("No words left to keep.")

    # merge kept words into segments; split where the pause is too long or a drop range sits between
    segs = []
    for w in words:
        s, e = max(0, w["s"] - a.pad), min(dur, w["e"] + a.pad)
        if segs and s - segs[-1][1] <= a.max_gap and not any(segs[-1][1] < ds < s for ds, _ in drops):
            segs[-1][1] = max(segs[-1][1], e)
        else:
            if segs and s < segs[-1][1]:
                s = segs[-1][1]
            segs.append([s, e])

    # remap word times onto new timeline
    out_words, offset, idx = [], 0.0, 0
    for s, e in segs:
        for w in words:
            if s <= w["s"] < e:
                out_words.append({**w, "s": round(w["s"] - s + offset, 3), "e": round(min(w["e"], e) - s + offset, 3)})
        offset += e - s

    fc = "".join(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[a{i}];"
                 for i, (s, e) in enumerate(segs))
    fc += "".join(f"[v{i}][a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]"
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    fcfile = os.path.splitext(a.out)[0] + "_filter.txt"
    open(fcfile, "w").write(fc)
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-filter_complex_script", fcfile,
                        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                        "-c:a", "aac", "-b:a", "192k", a.out], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("ffmpeg failed: " + r.stderr[-500:])

    base = os.path.dirname(os.path.abspath(a.out))
    json.dump({"language": data.get("language"), "duration": round(offset, 3), "words": out_words},
              open(os.path.join(base, "cut_words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    removed = round(dur - offset, 2)
    json.dump({"kept_segments": [[round(s, 3), round(e, 3)] for s, e in segs], "removed_sec": removed},
              open(os.path.join(base, "cuts.json"), "w"), indent=1)
    print(json.dumps({"ok": True, "out": a.out, "original_sec": round(dur, 2), "new_sec": round(offset, 2),
                      "removed_sec": removed, "segments": len(segs)}))


if __name__ == "__main__":
    main()
