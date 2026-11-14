"""Validate public WhatsApp invite links from public metadata only. Never joins groups.

Usage: python validate_whatsapp.py <link> [<link> ...]
"""
import re, sys, time, json, html
from urllib.parse import urlparse
import requests
from common import config, now

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
CODE_RE = re.compile(r"chat\.whatsapp\.com/(?:invite/)?([A-Za-z0-9]{18,32})")
GENERIC_TITLES = {"", "whatsapp group invite", "join whatsapp group", "whatsapp",
                  "group invite", "whatsapp group", "whatsapp chat", "general"}
EXPIRED_MARKERS = ["invite link was reset", "link was revoked", "invite link is no longer",
                   "couldn't join", "this invite link is invalid", "link has expired",
                   "group no longer exists", "invite_link_revoked"]
_last = [0.0]

def extract_code(link):
    m = CODE_RE.search(link or "")
    return m.group(1) if m else None

def canonicalize(link):
    """Strip ?mode= ?s= utm etc. Returns (canonical_url, code) or (None, None)."""
    code = extract_code(link)
    return (f"https://chat.whatsapp.com/{code}", code) if code else (None, None)

def _meta(page, prop):
    for pat in (rf'<meta[^>]+(?:property|name)=["\']{prop}["\'][^>]+content=["\']([^"\']*)',
                rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:property|name)=["\']{prop}["\']'):
        m = re.search(pat, page, re.I)
        if m:
            return html.unescape(m.group(1)).strip()
    return ""

def _json_field(page, key):
    m = re.search(rf'"{key}"\s*:\s*"((?:[^"\\]|\\.)*)"', page)
    if not m:
        return ""
    try:
        return json.loads(f'"{m.group(1)}"').strip()
    except json.JSONDecodeError:
        return m.group(1)

def _throttle(min_delay):
    wait = min_delay - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()

def fetch(url, cfg):
    v = cfg.get("validation", {})
    tries, base = v.get("max_retries", 3), v.get("backoff_base_s", 4)
    err = None
    for i in range(tries):
        _throttle(v.get("min_delay_s", 3.0))
        try:
            r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"},
                             timeout=v.get("timeout_s", 15), allow_redirects=True)
            if r.status_code == 429 or r.status_code >= 500:
                err = f"HTTP {r.status_code}"
                time.sleep(base * (2 ** i))
                continue
            return r, None
        except requests.RequestException as e:
            err = type(e).__name__
            time.sleep(base * (2 ** i))
    return None, err

def validate(link, cfg=None):
    cfg = cfg or config()
    canon, code = canonicalize(link)
    res = {"input_link": link, "canonical_url": canon, "invite_code": code, "checked_at": now(),
           "status": "Invalid", "exact_name": "", "og_title": "", "og_description": "",
           "has_image": False, "parent_group_subject": "", "kind": "Not publicly available",
           "request_to_join": False, "final_url": "", "notes": []}
    if not code:
        res["notes"].append("Not a chat.whatsapp.com invite format")
        return res
    r, err = fetch(canon, cfg)
    if r is None:
        res["status"] = "Unknown – Do Not Approve"
        res["notes"].append(f"Fetch failed: {err}")
        return res
    page, low = r.text, r.text.lower()
    res["final_url"] = r.url
    if r.status_code in (403, 429) or "/checkpoint/" in r.url or "unusual traffic" in low:
        res["status"] = "Unknown – Do Not Approve"
        res["notes"].append("Bot-protection page; try browser-rendered check")
        return res
    title = _meta(page, "og:title")
    m = re.search(r"<title>(.*?)</title>", page, re.I | re.S)
    page_title = html.unescape(m.group(1)).strip() if m else ""
    parent = _json_field(page, "parent_group_subject")
    res.update(og_title=title, og_description=_meta(page, "og:description"),
               # static.whatsapp.net/rsrc.php = WhatsApp default placeholder; pps.whatsapp.net = real group photo
               has_image="pps.whatsapp.net" in _meta(page, "og:image"), parent_group_subject=parent,
               page_title=page_title)
    is_community = bool(parent) or '"is_community":true' in low or "join a whatsapp community" in low
    res["request_to_join"] = "request to join" in low or "admin approval" in low or "membership_approval" in low
    if any(mk in low for mk in EXPIRED_MARKERS):
        res["status"] = "Revoked" if "revoked" in low or "reset" in low else "Expired"
        return res
    if r.status_code == 404:
        res["status"] = "Invalid"
        return res
    h3 = re.search(r'<h3 class="_9vd5[^"]*"[^>]*>(.*?)</h3>', page, re.S)
    rendered = html.unescape(re.sub(r"<[^>]+>", "", h3.group(1))).strip() if h3 else ""
    res["rendered_name"] = rendered
    if not title and rendered:
        title = rendered
    name = parent if (parent and is_community) else (title if title.lower() not in GENERIC_TITLES else "")
    res["kind"] = "Community" if is_community else ("Group" if name else "Not publicly available")
    if name and res["has_image"]:
        res["exact_name"] = name
        res["status"] = ("Active – Community" if is_community else
                         "Active – Request to Join" if res["request_to_join"] else "Active – Direct Join")
    elif name:
        res["exact_name"] = name
        res["status"] = "Probable Active – Metadata Partially Available"
        res["notes"].append("Specific title but no group image; needs strong official-source evidence")
    else:
        res["status"] = "Unknown – Do Not Approve"
        res["notes"].append(f"Generic/blank title ('{title or page_title}'); likely expired or needs browser check")
    return res

APPROVABLE = {"Active – Direct Join", "Active – Request to Join", "Active – Community"}

if __name__ == "__main__":
    cfg = config()
    print(json.dumps([validate(l, cfg) for l in sys.argv[1:]], ensure_ascii=False, indent=2))
