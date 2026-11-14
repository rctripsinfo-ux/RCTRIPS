"""One-off import of the user's legacy sheets into the exclusion DB.
Usage: python import_legacy.py <tool-result-file>:<label> ...  (get_values or get_spreadsheet JSON)"""
import json, re, sys, collections
from common import load_json, save_json, data_path, today
from deduplicate import normalize
R = re.compile(r"chat\.whatsapp\.com/(?:invite/)?([A-Za-z0-9]{18,32})")
SKIP = {"join now", "✅  join now", "join", "valid", "invalid", "group", "community"}

def rows_of(obj):
    if "values" in obj:                      # get_values
        return [[(c, None) for c in r] for r in obj["values"]]
    out = []                                 # get_spreadsheet grid
    for sh in obj["content"]["sheets"]:
        for d in sh.get("data", []):
            for r in d.get("rowData", []):
                out.append([(v.get("formattedValue", ""), v.get("hyperlink")) for v in r.get("values", [])])
    return out

prev, rej = load_json(data_path("previous_groups.json"), []), load_json(data_path("rejected_groups.json"), [])
known = {r["invite_code"] for r in prev + rej}
stats, dup_in_legacy, short = collections.Counter(), collections.Counter(), []
for arg in sys.argv[1:]:
    path, label = arg.rsplit(":", 1)
    rows = rows_of(json.load(open(path)))
    hdr = [c.lower() for c, _ in rows[0]] if rows else []
    stcol = next((i for i, h in enumerate(hdr) if h in ("link status", "status")), None)
    qcol = next((i for i, h in enumerate(hdr) if h == "quality status"), None)
    for r in rows:
        code = next((m for c, h in r for m in R.findall((h or "") + " " + c)), None)
        if not code:
            continue
        stats[label] += 1
        if len(code) < 20:
            short.append(code)
        if code in known:
            dup_in_legacy[label] += 1
            continue
        name = next((c for c, h in r if c and not R.search(c) and c.strip().lower() not in SKIP
                     and not c.strip().isdigit() and not c.startswith("●")), "")
        status = r[stcol][0] if stcol is not None and stcol < len(r) else ""
        quality = r[qcol][0] if qcol is not None and qcol < len(r) else ""
        rec = {"invite_code": code, "canonical_url": f"https://chat.whatsapp.com/{code}",
               "exact_name": name, "normalized": normalize(name), "source": f"legacy:{label}",
               "legacy_status": status, "legacy_quality": quality, "imported": today()}
        bad = status.lower() == "invalid" or quality.lower().startswith("excluded")
        (rej if bad else prev).append(rec)
        known.add(code)
save_json(data_path("previous_groups.json"), prev)
save_json(data_path("rejected_groups.json"), rej)
print("rows with links per source:", dict(stats))
print("already-known (cross-sheet duplicates) per source:", dict(dup_in_legacy))
print("unique codes total:", len(known), "| previous:", len(prev), "| rejected:", len(rej))
print("suspicious short codes:", short[:10])
names = collections.Counter(r["normalized"] for r in prev if r["normalized"])
print("most repeated normalized names (different links):", names.most_common(8))
