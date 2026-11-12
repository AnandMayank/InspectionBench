#!/usr/bin/env python3
"""Read-only: derives the Appendix J tables (episode accounting, tokens/time/cost, repeat stability,
full-pool capability scores) from the frozen run records. Writes only next to this file; refuses to overwrite.
No network, no model calls. Prices are provider list prices (fetched 2026-11-08), NOT invoices."""
import json, glob, csv, collections, datetime, hashlib, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
RB = HERE.parent / "results"              # released run records (see REPRODUCE.md)
# usage: build_repro_tables.py [OUT_DIR]   (default: next to this file; OUT_DIR must be new or empty of CSVs)
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE
OUT.mkdir(parents=True, exist_ok=True)
V1 = RB / "expanded_evaluation_v1"; V2 = RB / "expanded_evaluation_v2_attribution"
MODELS = ["Claude_Opus_5.5", "GPT-6-Astra", "DeepSeek_V4_Pro_0813", "Gemini_3.1_Pro_Preview", "Qwen3.5-397B-A17B"]
DISPLAY = dict(zip(MODELS, ["Claude Opus 5.5", "GPT-6-Astra", "DeepSeek V4 Pro 0813", "Gemini 3.1 Pro Preview", "Qwen3.5-397B-A17B"]))
PRICE = {"Claude_Opus_5.5": (4, 20), "GPT-6-Astra": (10, 50), "DeepSeek_V4_Pro_0813": (1.32, 3.96),
         "Gemini_3.1_Pro_Preview": (2, 12), "Qwen3.5-397B-A17B": (0.60, 3.60)}  # USD per 1M in/out, list price
# v1__main_merged usage ledgers and worker logs are byte-identical to v1__main
RUNS = {"V1 full pool": [V1 / "runs/v1__main_merged", V1 / "runs/v1__infra_rerun1"], "V1 repeat (stability)": [V1 / "runs/v1__repeat1"],
        "V2 attribution": [V2 / "runs/v2__main"], "smoke tests": [*map(Path, glob.glob(str(V1 / "runs/smoke_*"))), V2 / "runs/v2_smoke_r1__micro"]}
VALID = {"COMMIT", "ESCALATE", "ABORT", "DISPATCH"}
def P(t): return datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S%z")
def write(name, header, rows):
    p = OUT / name
    if p.exists(): sys.exit(f"refusing to overwrite {p}")
    with open(p, "w", newline="") as f: w = csv.writer(f); w.writerow(header); w.writerows(rows)

# 1. tokens, time, cost
rows = []
for run, dirs in RUNS.items():
    for m in MODELS:
        c = i = o = r = 0; el = 0.0
        for d in dirs:
            ts = []
            for f in glob.glob(str(d / m / "**/usage_ledger.jsonl"), recursive=True):
                for l in open(f):
                    x = json.loads(l); c += 1; i += x.get("input_tokens") or 0; o += x.get("output_tokens") or 0
                    r += x.get("reasoning_tokens") or 0; ts.append(P(x["ts"]))
            if ts: el += (max(ts) - min(ts)).total_seconds() / 3600  # elapsed summed per run directory
        if not c: continue
        shards = {Path(f).parent.name for d in dirs for f in glob.glob(str(d / m / "*/usage_ledger.jsonl"))}
        wh = 0.0
        for d in dirs:
            for f in glob.glob(str(d / m / "**/worker_log.jsonl"), recursive=True):
                for l in open(f):
                    x = json.loads(l)
                    if "finished" in x: wh += (P(x["finished"]) - P(x["started"])).total_seconds() / 3600
        cost = i / 1e6 * PRICE[m][0] + o / 1e6 * PRICE[m][1]
        rows.append([run, DISPLAY[m], c, i, o, r, round(el, 2), round(wh if wh else el, 2), max(1, len(shards)), round(cost, 2)])
write("compute_tokens_cost.csv", ["run", "model", "llm_calls", "input_tokens", "output_tokens(billed,incl_reasoning)",
      "reasoning_tokens_reported", "elapsed_h", "worker_h", "parallel_workers", "list_price_usd_estimate"], rows)

# 2. episode accounting (V1 full pool) per model x pool
elig = {}
for line in open(V1 / "eligibility_report.md"):
    p = [s.strip() for s in line.split("|")]
    if len(p) > 7 and p[1] in ("A", "E", "B_acq", "B_legacy", "C", "D_enterprise", "D_physical"):
        elig[p[1]] = dict(constructed=int(p[2]), valid=int(p[3]), executable=int(p[4]), excluded=int(p[5]), to_eval=int(p[6]))
def R(m, pat): return [json.loads(l) for f in glob.glob(str(V1 / "runs/v1__main_merged" / m / "*" / pat)) for l in open(f)]
acc = []
for m in MODELS:
    for pool, pat in [("A", "A.jsonl"), ("E", "E.jsonl"), ("B_acq", "B_acq/*.jsonl"), ("C", "C/*.jsonl"),
                      ("D_physical", "D_physical/*.jsonl"), ("D_enterprise", "D_enterprise/*.jsonl"), ("B_legacy", "B_legacy/*.jsonl")]:
        rs = R(m, pat)
        if pool == "E":
            eps = [e for r in rs for e in r["episodes"]]; att = len(eps)
            infra = sum(len(r["episodes"]) for r in rs if r.get("infra_failure"))
            valid = sum(1 for e in eps if (e.get("verdict") or "").upper() in VALID)
        else:
            att = len(rs); infra = sum(1 for r in rs if r.get("infra_failure") or r.get("is_apparatus_failure"))
            if pool == "A": valid = sum(1 for r in rs if r.get("verdict_present"))
            elif pool == "B_acq": valid = sum(1 for r in rs if r.get("error") is None and r.get("response") is not None)
            elif pool == "D_physical": valid = sum(1 for r in rs if r.get("error") is None and r.get("parsed_response"))
            elif pool == "B_legacy": valid = att - infra
            else: valid = sum(1 for r in rs if (r.get("verdict") or "").upper() in VALID)
        e = elig[pool]; to_eval = e["to_eval"] * (1 if pool != "E" else 1)
        acc.append([DISPLAY[m], pool, e["constructed"], e["excluded"], e["to_eval"], att, att - infra, valid, att, att - valid])
write("episode_accounting_v1.csv", ["model", "pool", "constructed", "excluded_pre_run", "eligible", "attempted",
      "executed_without_infra_failure", "valid_terminal_output", "scored(missing=fail)", "invalid_or_missing_scored_0"], acc)

# 3. repeat stability (A pool; identical episodes, temperature 0)
rep = []
for m in MODELS:
    main = {r["episode_id"]: r for r in R(m, "A.jsonl")}
    rr = [json.loads(l) for l in open(V1 / "runs/v1__repeat1" / m / "all/A.jsonl")]
    n = len(rr); v = t = g = 0; T = [0, 0]; G = [0, 0]
    for r in rr:
        a = main[r["episode_id"]]; v += a["verdict"] == r["verdict"]
        t1, t2 = int(bool(a["metric"]["TDA"])), int(bool(r["metric"]["TDA"])); g1, g2 = int(bool(a["metric"]["GSR"])), int(bool(r["metric"]["GSR"]))
        t += t1 == t2; g += g1 == g2; T[0] += t1; T[1] += t2; G[0] += g1; G[1] += g2
    rep.append([DISPLAY[m], n, v, t, g, T[0], T[1], G[0], G[1]])
write("repeat_stability_A.csv", ["model", "episodes_repeated", "same_verdict", "same_TDA", "same_GSR",
      "TDA_main", "TDA_repeat", "GSR_main", "GSR_repeat"], rep)

# 4. full-pool capability scores (Figure-5 metrics, missing = fail)
cap = []
for m in MODELS:
    A = R(m, "A.jsonl"); tda = sum(bool(r["metric"]["TDA"]) for r in A if r.get("verdict_present")) / len(A)
    gsr = sum(bool(r["metric"]["GSR"]) for r in A if r.get("verdict_present")) / len(A)
    b = []
    for r in R(m, "B_acq/*.jsonl"):
        s, gg = r["score"], r["gold"]
        if r.get("error") is not None or r.get("response") is None: b.append(0); continue
        ada, tp, asa, uha = bool(s["ADA"]), bool(s["TDA_post"]), s.get("ASA") == 1.0, s.get("UHA") == 1.0
        b.append(int((ada and tp) if not gg["acquisition_required"] else (ada and asa and tp) if not gg["acquisition_genuinely_unavailable"] else (ada and asa and uha)))
    an = {(x["model"], x["capability"]): x for x in csv.DictReader(open(V1 / "analysis/v1__main_merged/capability_metrics_BCD.csv"))}
    te = {x["model"]: x for x in csv.DictReader(open(V1 / "analysis/v1__main_merged/temporal_E.csv"))}
    d = DISPLAY[m]
    cap.append([d, len(A), round(100 * tda, 1), round(100 * gsr, 1), round(100 * (tda - gsr), 1), round(100 * sum(b) / len(b), 1),
                round(100 * float(an[(d, "C")]["coverage(recall)"]), 1), round(100 * float(an[(d, "D_physical")]["CC"]), 1),
                round(100 * float(an[(d, "D_physical")]["CSA"]), 1), round(100 * float(te[d]["TC=mean_CC_grounded"]), 1)])
write("full_pool_capability_scores.csv", ["model", "A_episodes", "A_TDA", "A_GSR", "A_gap_pp", "B_AGS(n=66)", "C_coverage(n=112)",
      "D_CC(n=70)", "D_CSA(n=70)", "E_mean_grounded(469 seq)"], cap)

with open(OUT / "SHA256SUMS.txt", "w") as f:
    for p in sorted(OUT.glob("*.csv")) + ([Path(__file__).resolve()] if OUT == HERE else []):
        f.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n")
print("ok")
