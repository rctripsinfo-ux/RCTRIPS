"""Name normalization and duplicate / similar-group detection."""
import re, unicodedata
from difflib import SequenceMatcher

SUFFIXES = r"\b(official|whatsapp group|whatsapp|group|grp|community|network|updates?|channel)\b"
SUBGROUP = r"\b(?:part|grp|group|no\.?|batch|#)?\s*\d{1,3}\s*$|\b[ivx]{1,4}$"

def strip_emoji(s):
    return "".join(c for c in s if unicodedata.category(c)[0] not in ("S", "C") or c in " ")

def normalize(name):
    s = strip_emoji(name or "").lower().replace("_", " ").replace("&", " and ")
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(SUFFIXES, " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s2 = re.sub(SUBGROUP, "", s).strip()
    return s2 or s

def similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()

def find_duplicate(cand, existing, threshold=0.85):
    """cand/existing records: dicts with invite_code, canonical_url, exact_name,
    parent_community, source_org. Returns (verdict, match_desc) where verdict is
    'duplicate', 'review' or None."""
    code, url = cand.get("invite_code"), cand.get("canonical_url")
    name, norm = cand.get("exact_name", ""), normalize(cand.get("exact_name", ""))
    parent = normalize(cand.get("parent_community", ""))
    org = (cand.get("source_org") or "").strip().lower()
    review = None
    for e in existing:
        label = f"{e.get('exact_name') or e.get('proposed_name','?')} [{e.get('invite_code','?')}]"
        if code and code == e.get("invite_code"):
            return "duplicate", f"Same invite code: {label}"
        if url and url == e.get("canonical_url"):
            return "duplicate", f"Same canonical URL: {label}"
        en = e.get("exact_name", "")
        if not en:
            continue
        if name and name == en:
            return "duplicate", f"Exact name match: {label}"
        if norm and norm == normalize(en):
            return "duplicate", f"Normalized name/subgroup match: {label}"
        if parent and parent == normalize(e.get("parent_community", "")):
            return "duplicate", f"Same parent community: {label}"
        sim = similarity(name, en)
        if sim >= threshold:
            same_org = org and org == (e.get("source_org") or "").strip().lower()
            if same_org:
                return "duplicate", f"Similar name ({sim:.0%}) + same organizer: {label}"
            review = review or ("review", f"Similar name ({sim:.0%}) — manual review: {label}")
    return review or (None, "")
