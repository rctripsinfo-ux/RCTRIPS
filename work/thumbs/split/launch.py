import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
jobs = [l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()]
def go(j): r = subprocess.run(["./run.sh", *j], capture_output=True, text=True); print(r.stdout.strip(), flush=True)
with ThreadPoolExecutor(3) as ex: list(ex.map(go, jobs))
print("ALL DONE", flush=True)
