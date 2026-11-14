"""Research-run pipeline. Claude gathers candidates (web search) into a JSON file,
then this script validates, dedupes, scores, approves/rejects and saves.

  python run_research.py process candidates.json --niche "B2B travel" [--quantity 10] [--no-sheet]
  python run_research.py revalidate [--no-sheet]
  python run_research.py stats

Candidate fields: link, proposed_name, source_platform, source_url, source_post_date,
source_likes, source_comments, source_org, sub_niche, b2b_b2c, region, language,
member_evidence, member_claim, activity_evidence, relevance_note, scores{relevance,
credibility,activity,size,value}, reason, notes, niche_fit (bool), spam (bool),
official_evidence (bool, required for Probable Active).
"""
import argparse, json, sys, uuid
from common import config, load_json, save_json, data_path, today, now, NA
from validate_whatsapp import validate, canonicalize, APPROVABLE
from deduplicate import find_duplicate, normalize
from quality_score import score, linkedin_ok
import google_sheets as gs

def reject(c, reason, v=None, dup="", niche=""):
    return {"date_checked": today(), "proposed_name": c.get("proposed_name") or (v or {}).get("exact_name", ""),
            "link": c.get("link"), "invite_code": (v or {}).get("invite_code") or canonicalize(c.get("link"))[1],
            "canonical_url": canonicalize(c.get("link"))[0], "exact_name": (v or {}).get("exact_name", ""),
            "niche": niche, "source_platform": c.get("source_platform"), "source_url": c.get("source_url"),
            "reason": reason, "validation": (v or {}).get("status", "Not validated"), "duplicate_match": dup,
            "notes": "; ".join(filter(None, [c.get("notes", "")] + (v or {}).get("notes", [])))}

def rej_row(r):
    return [r["date_checked"], r["proposed_name"], r["canonical_url"] or r["link"], r["invite_code"],
            r["niche"], r["source_platform"], r["source_url"], r["reason"], r["validation"],
            r["duplicate_match"], r["notes"]]

def appr_row(a):
    s = a["scores"]
    return [a["record_id"], a["date_found"], a["niche"], a["exact_name"], a["normalized"], a.get("sub_niche"),
            a["canonical_url"], a["invite_code"], a["kind"], a["status"], a["verified_at"],
            a.get("source_platform"), a.get("source_url"), a.get("source_post_date"), a.get("source_likes"),
            a.get("source_comments"), a.get("member_evidence"), a.get("member_claim"),
            a.get("activity_evidence"), a.get("b2b_b2c"), a.get("region"), a.get("language"),
            s["relevance"], s["credibility"], s["activity"], s["size"], s["overall"], s["tier"],
            a.get("reason"), a.get("notes")]

def process(cands, niche, quantity, use_sheet, meta):
    cfg = config(); d = cfg["defaults"]
    prev_p, rej_p = data_path("previous_groups.json"), data_path("rejected_groups.json")
    prev, rej = load_json(prev_p, []), load_json(rej_p, [])
    if use_sheet:  # also compare against live sheet rows
        try:
            gs.import_existing(); prev, rej = load_json(prev_p, []), load_json(rej_p, [])
        except Exception as e:
            print(f"WARNING: sheet read failed ({e}); deduping against local DB only", file=sys.stderr)
    approved, rejected, review = [], [], []
    stats = {"duplicates": 0, "expired": 0, "linkedin_rejected": 0, "validated": 0}
    for c in cands:
        url, code = canonicalize(c.get("link"))
        if not code:
            rejected.append(reject(c, "Invalid link format", niche=niche)); continue
        pre = {"invite_code": code, "canonical_url": url}
        verdict, m = find_duplicate(pre, prev + rej + approved)
        if verdict == "duplicate":
            stats["duplicates"] += 1
            rejected.append(reject(c, "Duplicate invite code", dup=m, niche=niche)); continue
        if c.get("source_platform", "").lower() == "linkedin" and not linkedin_ok(
                c.get("source_likes"), c.get("source_comments"), d["linkedin_min_reactions"],
                d["linkedin_min_comments"], d["linkedin_combine_allowed"]):
            stats["linkedin_rejected"] += 1
            rejected.append(reject(c, "LinkedIn post below the required engagement threshold", niche=niche)); continue
        v = validate(c["link"], cfg); stats["validated"] += 1
        st = v["status"]
        if st in ("Expired", "Revoked", "Invalid"):
            stats["expired"] += 1
            rejected.append(reject(c, "Expired or revoked invite", v, niche=niche)); continue
        if st.startswith("Unknown"):
            reason = "Placeholder WhatsApp title" if "Generic" in " ".join(v["notes"]) else "Unable to validate"
            rejected.append(reject(c, reason, v, niche=niche)); continue
        if st.startswith("Probable") and not c.get("official_evidence"):
            rejected.append(reject(c, "Unable to validate", v, niche=niche)); continue
        if st == "Active – Request to Join" and not d.get("include_request_to_join", False) and not meta.get("include_rtj"):
            rejected.append(reject(c, "Request-to-join excluded by filters", v, niche=niche)); continue
        full = {**pre, "exact_name": v["exact_name"], "parent_community": v["parent_group_subject"],
                "source_org": c.get("source_org", "")}
        verdict, m = find_duplicate(full, prev + rej + approved, d["fuzzy_review_threshold"])
        if verdict == "duplicate":
            stats["duplicates"] += 1
            rejected.append(reject(c, "Same community already supplied", v, m, niche)); continue
        if verdict == "review":
            review.append({"candidate": c, "validation": v, "match": m}); continue
        if c.get("spam"):
            rejected.append(reject(c, "Spam, earning scheme or promotional dump", v, niche=niche)); continue
        if c.get("niche_fit") is False:
            rejected.append(reject(c, c.get("reject_reason") or "Irrelevant niche", v, niche=niche)); continue
        s = score(c.get("scores", {}))
        if s["overall"] < d["min_quality_score"]:
            rejected.append(reject(c, f"Insufficient quality evidence (score {s['overall']})", v, niche=niche)); continue
        if len(approved) >= quantity:
            continue  # surplus qualified candidates are not rejected; available next run
        notes = c.get("notes", "")
        if c.get("proposed_name") and c["proposed_name"] != v["exact_name"]:
            notes = f"Source name '{c['proposed_name']}' differs from WhatsApp name. " + notes
        if st.startswith("Probable"):
            notes = "PROBABLE ACTIVE – metadata partial; approved on official-source evidence. " + notes
        approved.append({**c, **full, "record_id": f"WG-{today().replace('-','')}-{uuid.uuid4().hex[:6]}",
                         "date_found": today(), "niche": niche, "normalized": normalize(v["exact_name"]),
                         "kind": v["kind"], "status": st, "verified_at": v["checked_at"], "scores": s,
                         "notes": notes.strip() or NA})
        # save locally immediately so progress survives a later failure
        save_json(prev_p, prev + approved)
        save_json(rej_p, rej + rejected)
    save_json(prev_p, prev + approved); save_json(rej_p, rej + rejected)
    sheet_rows = {"approved": 0, "rejected": 0, "error": None}
    if use_sheet:
        sc = cfg["sheet"]
        try:
            sheet_rows["approved"] = gs.append_verified(sc["approved_ws"], [appr_row(a) for a in approved])
            sheet_rows["rejected"] = gs.append_verified(sc["rejected_ws"], [rej_row(r) for r in rejected])
        except Exception as e:
            sheet_rows["error"] = f"{type(e).__name__}: {e} — rows queued in data/pending_uploads.json"
    sid = f"S-{now().replace(':','').replace('-','')}"
    hist = {"search_id": sid, "datetime": now(), "niche": niche, "sub_niche": meta.get("sub_niche", ""),
            "region": meta.get("region", ""), "requested": quantity, "candidates": len(cands),
            "validated": stats["validated"], "approved": len(approved), "rejected": len(rejected),
            "queries": meta.get("queries", ""), "platforms": meta.get("platforms", ""),
            "notes": f"{len(review)} sent to manual review. " + meta.get("notes", "")}
    h = load_json(data_path("search_history.json"), []); h.append(hist)
    save_json(data_path("search_history.json"), h)
    if use_sheet and not sheet_rows["error"]:
        try:
            gs.append_verified(cfg["sheet"]["history_ws"], [list(hist.values())])
        except Exception as e:
            sheet_rows["error"] = f"history write failed: {e}"
    cfg["last_run"] = {"niche": niche, "sub_niche": meta.get("sub_niche", ""), "region": meta.get("region", ""), "filters": meta}
    save_json(__import__("common").CONFIG_PATH, cfg)
    return {"approved": approved, "rejected": rejected, "review": review, "stats": stats, "sheet": sheet_rows, "history": hist}

def revalidate(use_sheet):
    """Recheck approved links; flag renames/expiry. Updates only Status (J), Verification
    Date (K) and appends to Research Notes (AD). Never deletes rows."""
    cfg = config(); out = []
    if use_sheet:
        ws = gs.spreadsheet().worksheet(cfg["sheet"]["approved_ws"])
        rows = ws.get_all_values()
        for i, row in enumerate(rows[1:], start=2):
            if len(row) < 10 or not row[7]:
                continue
            v = validate(row[6] or row[7], cfg)
            flag = []
            if v["exact_name"] and v["exact_name"] != row[3]:
                flag.append(f"RENAMED {today()}: '{row[3]}' -> '{v['exact_name']}'")
            if v["status"] != row[9]:
                flag.append(f"STATUS {today()}: {row[9]} -> {v['status']}")
            ws.update(f"J{i}:K{i}", [[v["status"], v["checked_at"]]], value_input_option="RAW")
            if flag:
                ws.update_acell(f"AD{i}", ((row[29] + " | ") if len(row) > 29 and row[29] != NA else "") + "; ".join(flag))
            out.append((row[3], v["status"], flag))
    else:
        prev = load_json(data_path("previous_groups.json"), [])
        for r in prev:
            v = validate(r["canonical_url"], cfg)
            flag = [f"RENAMED -> {v['exact_name']}"] if v["exact_name"] and r.get("exact_name") and v["exact_name"] != r["exact_name"] else []
            r.setdefault("status_history", []).append({"date": v["checked_at"], "status": v["status"]})
            r["status"] = v["status"]
            out.append((r.get("exact_name"), v["status"], flag))
        save_json(data_path("previous_groups.json"), prev)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["process", "revalidate", "stats"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--niche", default="")
    ap.add_argument("--quantity", type=int, default=None)
    ap.add_argument("--no-sheet", action="store_true")
    ap.add_argument("--meta", default="{}", help="JSON: sub_niche, region, queries, platforms, include_rtj, notes")
    a = ap.parse_args()
    if a.cmd == "process":
        res = process(load_json(a.file, []), a.niche or config()["last_run"]["niche"],
                      a.quantity or config()["defaults"]["quantity"], not a.no_sheet, json.loads(a.meta))
        print(json.dumps({k: res[k] for k in ("stats", "sheet", "history")}, ensure_ascii=False, indent=2))
        for x in res["approved"]:
            print(f"APPROVED {x['scores']['overall']:>3} {x['exact_name']} | {x['canonical_url']} | {x['status']}")
        for x in res["review"]:
            print(f"REVIEW   {x['validation']['exact_name']} | {x['match']}")
        for x in res["rejected"]:
            print(f"REJECTED {x['proposed_name'] or x['invite_code']} | {x['reason']}")
    elif a.cmd == "revalidate":
        for n, s, f in revalidate(not a.no_sheet):
            print(s, "|", n, "|", "; ".join(f))
    else:
        print(len(load_json(data_path("previous_groups.json"), [])), "approved,",
              len(load_json(data_path("rejected_groups.json"), [])), "rejected,",
              len(load_json(data_path("search_history.json"), [])), "runs")
