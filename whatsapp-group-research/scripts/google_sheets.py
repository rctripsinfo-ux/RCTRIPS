"""Google Sheets I/O via service account (gspread). Append-only; never overwrites
or deletes. Usage: python google_sheets.py test | setup | import"""
import os, sys, time
from common import config, load_env, load_json, save_json, data_path, NA

APPROVED_HEADERS = ["Record ID", "Date Found", "Search Niche", "Exact Group Name",
    "Normalized Group Name", "Industry / Sub-Niche", "WhatsApp Invite Link", "Invite Code",
    "Group or Community", "Current Status", "Verification Date", "Source Platform", "Source URL",
    "Source Post Date", "Source Likes", "Source Comments", "Public Member Evidence",
    "Member Count Claimed", "Activity Evidence", "B2B / B2C", "Country / Region",
    "Primary Language", "Relevance Score", "Credibility Score", "Activity Score",
    "Size Evidence Score", "Overall Quality Score", "Quality Tier", "Reason Approved",
    "Research Notes"]
REJECTED_HEADERS = ["Date Checked", "Proposed Group Name", "WhatsApp Link", "Invite Code",
    "Requested Niche", "Source Platform", "Source URL", "Rejection Reason", "Validation Result",
    "Duplicate Match", "Notes"]
HISTORY_HEADERS = ["Search ID", "Date and time", "Niche requested", "Sub-niche requested",
    "Location requested", "Number requested", "Number of candidates found", "Number validated",
    "Number approved", "Number rejected", "Search queries used", "Platforms searched", "Notes"]
CONFIG_HEADERS = ["Setting", "Value"]

def safe(v):
    """Escape formula-like content; fill blanks honestly."""
    if v is None or v == "":
        return NA
    s = str(v)
    return "'" + s if s[:1] in ("=", "+", "-", "@") else s

def client():
    load_env()
    import gspread
    path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "credentials/service_account.json")
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), path)
    return gspread.service_account(filename=path)

def spreadsheet():
    cfg = config()
    load_env()
    sid = cfg.get("sheet", {}).get("sheet_id") or os.environ.get("GOOGLE_SHEET_ID")
    if not sid:
        raise RuntimeError("No sheet_id configured")
    return client().open_by_key(sid)

def ensure_worksheets(ss, create=False):
    """Report missing/mismatched worksheets. Creates missing ones only if create=True.
    Never rewrites headers of an existing non-empty sheet."""
    s = config()["sheet"]
    plan = {s["approved_ws"]: APPROVED_HEADERS, s["rejected_ws"]: REJECTED_HEADERS,
            s["history_ws"]: HISTORY_HEADERS, s["config_ws"]: CONFIG_HEADERS}
    titles = {w.title: w for w in ss.worksheets()}
    report = []
    for name, hdr in plan.items():
        ws = titles.get(name)
        if ws is None:
            if create:
                ws = ss.add_worksheet(name, rows=1000, cols=len(hdr))
                ws.append_row(hdr, value_input_option="RAW")
                report.append(f"created {name}")
            else:
                report.append(f"MISSING {name}")
            continue
        cur = ws.row_values(1)
        if not cur and create:
            ws.append_row(hdr, value_input_option="RAW")
            report.append(f"headers added to empty {name}")
        elif cur != hdr:
            report.append(f"HEADER MISMATCH {name}: {cur}")
        else:
            report.append(f"ok {name}")
    return report

def append_verified(ws_name, rows, retries=3):
    """Append rows and re-read to confirm. Returns count verified. On failure,
    rows are queued in data/pending_uploads.json and the exception is re-raised."""
    if not rows:
        return 0
    rows = [[safe(c) for c in r] for r in rows]
    try:
        ss = spreadsheet()
        ws = ss.worksheet(ws_name)
        for i in range(retries):
            try:
                resp = ws.append_rows(rows, value_input_option="RAW", insert_data_option="INSERT_ROWS")
                rng = resp["updates"]["updatedRange"].split("!")[1]
                got = ws.get(rng)
                if len(got) != len(rows):
                    raise RuntimeError(f"verify mismatch: wrote {len(rows)}, read {len(got)}")
                return len(rows)
            except Exception as e:  # rate limit etc.
                if "PERMISSION" in str(e).upper() or i == retries - 1:
                    raise
                time.sleep(5 * 2 ** i)
    except Exception:
        q = load_json(data_path("pending_uploads.json"), [])
        q.append({"worksheet": ws_name, "rows": rows})
        save_json(data_path("pending_uploads.json"), q)
        raise

def flush_pending():
    q = load_json(data_path("pending_uploads.json"), [])
    save_json(data_path("pending_uploads.json"), [])
    done = 0
    for item in q:
        done += append_verified(item["worksheet"], item["rows"])  # re-queues on failure
    return done

def read_records(ws_name):
    return spreadsheet().worksheet(ws_name).get_all_records(default_blank="")

def import_existing():
    """Pull all links already in the sheet into the local exclusion DB. Reports duplicates."""
    from validate_whatsapp import canonicalize
    from deduplicate import normalize
    s = config()["sheet"]
    prev = load_json(data_path("previous_groups.json"), [])
    rej = load_json(data_path("rejected_groups.json"), [])
    known = {r.get("invite_code") for r in prev + rej}
    dups, added = [], 0
    ss = spreadsheet()
    for ws in ss.worksheets():
        vals = ws.get_all_values()
        for i, row in enumerate(vals[1:], start=2):
            for cell in row:
                url, code = canonicalize(cell)
                if not code:
                    continue
                if code in known:
                    dups.append(f"{ws.title}!row{i}: {code}")
                    continue
                known.add(code)
                rec = {"invite_code": code, "canonical_url": url, "source": f"sheet:{ws.title}!{i}"}
                if ws.title == s["approved_ws"] and len(row) > 4:
                    rec.update(exact_name=row[3], normalized=row[4] or normalize(row[3]))
                elif ws.title == s["rejected_ws"] and len(row) > 1:
                    rec.update(proposed_name=row[1])
                (rej if ws.title == s["rejected_ws"] else prev).append(rec)
                added += 1
    save_json(data_path("previous_groups.json"), prev)
    save_json(data_path("rejected_groups.json"), rej)
    return added, dups

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    ss = spreadsheet()
    if cmd == "test":
        print("Spreadsheet:", ss.title)
        for w in ss.worksheets():
            print(f"- {w.title} ({w.row_count}x{w.col_count}) headers={w.row_values(1)}")
        print("\n".join(ensure_worksheets(ss, create=False)))
    elif cmd == "setup":
        print("\n".join(ensure_worksheets(ss, create=True)))
    elif cmd == "import":
        n, d = import_existing()
        print(f"Imported {n} links; {len(d)} duplicates in sheet:", *d, sep="\n")
    elif cmd == "flush":
        print("Uploaded", flush_pending(), "pending rows")
