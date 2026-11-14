"""Shared paths and JSON helpers."""
import json, os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CONFIG_PATH = os.path.join(ROOT, "config", "research_config.json")
NA = "Not publicly available"

def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)  # atomic: progress is never half-written

def data_path(name):
    return os.path.join(DATA, name)

def config():
    return load_json(CONFIG_PATH, {})

def today():
    return datetime.date.today().isoformat()

def now():
    return datetime.datetime.now().replace(microsecond=0).isoformat()

def load_env():
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
