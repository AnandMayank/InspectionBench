#!/usr/bin/env python3
"""compare_runs.py RUN_A RUN_B -- per-episode agreement between two runs of the A pool (and E, per visit).
RUN_x is a run directory laid out as <run>/<model_label>/<shard>/A.jsonl (and E.jsonl), e.g. the released
v1__main_merged and your re-run. Read-only; prints one row per model. No network, no model calls."""
import json, glob, sys
from pathlib import Path
def load(run, m, name):
    out = {}
    for f in glob.glob(str(Path(run) / m / "*" / name)):
        for l in open(f):
            r = json.loads(l)
            if name == "A.jsonl":
                out[r["episode_id"]] = (r.get("verdict"), bool(r["metric"]["TDA"]), bool(r["metric"]["GSR"]))
            else:
                for i, e in enumerate(r["episodes"]):
                    out[f'{r["sequence_id"]}#{i}'] = (e.get("verdict"), bool(e.get("CC")), bool(e.get("CC_grounded")))
    return out
a, b = sys.argv[1], sys.argv[2]
models = sorted({Path(p).name for p in glob.glob(str(Path(a) / "*")) if Path(p).is_dir()} &
                {Path(p).name for p in glob.glob(str(Path(b) / "*")) if Path(p).is_dir()})
print("pool,model,shared_episodes,same_verdict,same_TDA,same_GSR")
for pool in ("A.jsonl", "E.jsonl"):
    for m in models:
        x, y = load(a, m, pool), load(b, m, pool); k = x.keys() & y.keys()
        if not k: continue
        print(f'{pool[0]},{m},{len(k)},' + ",".join(str(sum(x[e][j] == y[e][j] for e in k)) for j in range(3)))
