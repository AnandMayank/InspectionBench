# Reproducing the reported numbers from the released run records

Everything below runs on a CPU with Python ≥ 3.10 and the standard library only. No API key or GPU is needed.

## 0. Unpack

```bash
find results -name '*.gz' -exec gunzip {} +
```

## 1. Appendix J tables

```bash
python3 reproducibility/build_repro_tables.py /tmp/ib_check
for f in compute_tokens_cost episode_accounting_v1 full_pool_capability_scores repeat_stability_A; do
  diff -q /tmp/ib_check/$f.csv reproducibility/$f.csv && echo "$f reproduced"
done
```

| Output | Content | Paper |
|---|---|---|
| `episode_accounting_v1.csv` | Per model × pool: constructed, excluded before the run, eligible, attempted, executed, valid output, scored, invalid (scored 0) | App. J, episode accounting |
| `compute_tokens_cost.csv` | Calls, input, output and reasoning tokens, elapsed and worker hours, list-price cost, per run and model | App. J, compute and cost |
| `full_pool_capability_scores.csv` | TDA, GSR and their gap on 2,388 A episodes; B AGS; C coverage; D CC and CSA; E grounded success | App. J, full-pool results |
| `repeat_stability_A.csv` | Verdict, TDA and GSR agreement on 60 repeated A episodes per model | App. J, controls |

Costs are estimates at provider list prices (USD per 1M input/output tokens: Claude Opus 5.5 4/20, GPT-6-Astra 10/50,
DeepSeek V4 Pro 0813 1.32/3.96, Gemini 3.1 Pro Preview 2/12, Qwen3.5-397B-A17B 0.60/3.60). They are not invoices.

## 2. Compare two runs episode by episode

```bash
cd results/expanded_evaluation_v1/runs
python3 ../../../reproducibility/compare_runs.py v1__main_merged v1__repeat1
```

This prints shared episodes and same verdict / TDA / GSR, per model, for A (and for E, per visit). Expect about 92% (A)
and 81% (E) verdict agreement. At temperature 0 the model outputs are still not deterministic, so agreement is not
identity.

## 3. Inspect any episode

Each line of `results/expanded_evaluation_v1/runs/v1__main_merged/<model>/<shard>/A.jsonl` is one episode:

| Field | Content |
|---|---|
| `turns[].sent` | The exact text sent to the model |
| `turns[].parsed` | The model's parsed reply |
| `traces` | The hash-chained execution trace: every request, execution, result and delivery event |
| `metric` | TDA, GSR and the other per-episode scores |
| `usage` | Tokens for this episode |

`interface/example_episode/TRANSCRIPT.md` renders one such record in full.

## 4. Configuration as run

`results/expanded_evaluation_v1/protocol/v1.json` records the configuration the runs used, read from the runner code:

| Setting | Value |
|---|---|
| Model ids | the five gateway ids |
| Temperature | 0 |
| Max tokens | 1,024 (16,384 for DeepSeek); 2,048 for the B and D-physical runners |
| Retry policy | transport errors only |
| CouchDB image | pinned by digest |
| Code | SHA-256 of all 921 files the runner executed |

The runner refused to start if any of those files changed.

Re-running the models from scratch also needs the CouchDB data volume, the rendered scenes and the tool servers. These
will be released on publication (see the README).
