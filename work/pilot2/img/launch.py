import subprocess
from concurrent.futures import ThreadPoolExecutor
jobs = [l.rstrip("\n").split("\t") for l in open("shots.tsv") if l.strip()]
def go(j): r = subprocess.run(["./run.sh", j[0], j[1]], capture_output=True, text=True); print(r.stdout.strip(), flush=True)
with ThreadPoolExecutor(3) as ex: list(ex.map(go, jobs))
print("ALL DONE", flush=True)
