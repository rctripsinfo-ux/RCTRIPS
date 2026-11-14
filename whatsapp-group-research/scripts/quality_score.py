"""Quality scoring (0–100). Component scores are assigned by the researcher from
public evidence; this module enforces ranges, totals and tiers."""
LIMITS = {"relevance": 30, "credibility": 25, "activity": 20, "size": 15, "value": 10}

def score(components):
    out = {}
    for k, cap in LIMITS.items():
        v = int(components.get(k, 0) or 0)
        if not 0 <= v <= cap:
            raise ValueError(f"{k}={v} outside 0–{cap}")
        out[k] = v
    out["overall"] = sum(out[k] for k in LIMITS)
    out["tier"] = tier(out["overall"])
    return out

def tier(total):
    return ("Excellent" if total >= 85 else "Strong" if total >= 75 else
            "Acceptable" if total >= 65 else "Weak" if total >= 50 else "Reject")

def linkedin_ok(likes, comments, min_r=500, min_c=500, combine=False):
    """Hidden/unknown engagement (None) always fails. No estimating."""
    if likes is None and comments is None:
        return False
    l, c = likes or 0, comments or 0
    return (l + c >= min_r) if combine else (l >= min_r or c >= min_c)
