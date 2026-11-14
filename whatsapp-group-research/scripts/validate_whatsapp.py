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


# ---- Browser-rendered check (adapted from user's direct_join_checker.py CheckerPane) ----
BROWSER_JS = r"""() => {
  const m = s => (document.querySelector(s) || {}).content || '';
  const h3 = document.querySelector('h3');
  return {title: document.title || '', ogTitle: m('meta[property="og:title"]'),
          ogImage: m('meta[property="og:image"]'), ogDesc: m('meta[property="og:description"]'),
          rendered: h3 ? h3.innerText.trim() : '',
          imgs: Array.from(document.querySelectorAll('img')).map(i => i.src).filter(Boolean),
          body: document.body ? document.body.innerText.slice(0, 3000) : ''};
}"""

def browser_check(link, screenshot_dir=None):
    """Headless Chromium render of the public invite page. Never clicks Join."""
    canon, code = canonicalize(link)
    out = {"ok": False, "name": "", "has_photo": False, "body": "", "screenshot": "", "error": ""}
    if not code:
        out["error"] = "bad format"; return out
    try:
        from playwright.sync_api import sync_playwright
        import os
        exe = os.environ.get("CHROMIUM_PATH") or next((x for x in ("/opt/pw-browsers/chromium",) if os.path.isfile(x)), None)
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
            pg = b.new_context(user_agent=UA, accept_downloads=False).new_page()
            r = pg.goto(canon, timeout=60000, wait_until="domcontentloaded")
            try:
                pg.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass
            info = pg.evaluate(BROWSER_JS)
            if screenshot_dir:
                import os
                os.makedirs(screenshot_dir, exist_ok=True)
                out["screenshot"] = os.path.join(screenshot_dir, f"{code}.png")
                pg.screenshot(path=out["screenshot"], full_page=True)
            b.close()
        name = info["ogTitle"] or info["rendered"]
        out.update(ok=bool(r and r.status < 400), body=info["body"].lower(),
                   name="" if name.strip().lower() in GENERIC_TITLES else name.strip(),
                   has_photo=any("pps.whatsapp.net" in u for u in [info["ogImage"]] + info["imgs"]))
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"[:200]
    return out

def validate(link, cfg=None, use_browser=True, screenshot_dir=None):
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
    if use_browser and (not title or title.lower() in GENERIC_TITLES or not res["has_image"]):
        bc = browser_check(canon, screenshot_dir)
        res["browser"] = {k: bc[k] for k in ("ok", "name", "has_photo", "screenshot", "error")}
        if bc["error"]:
            res["notes"].append(f"Browser check failed: {bc['error']}")
        else:
            if any(mk in bc["body"] for mk in EXPIRED_MARKERS):
                res["status"] = "Revoked" if ("revoked" in bc["body"] or "reset" in bc["body"]) else "Expired"
                return res
            if bc["name"] and (not title or title.lower() in GENERIC_TITLES):
                title = bc["name"]; res["notes"].append("Name from browser-rendered page")
            res["has_image"] = res["has_image"] or bc["has_photo"]
            res["request_to_join"] = res["request_to_join"] or "request to join" in bc["body"]
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
    import os
    shots = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "screenshots")
    print(json.dumps([validate(l, cfg, screenshot_dir=shots) for l in sys.argv[1:]], ensure_ascii=False, indent=2))
