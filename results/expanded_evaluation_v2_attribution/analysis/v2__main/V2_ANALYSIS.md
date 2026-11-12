# v2 attribution and perturbation sensitivity — run `v2__main`

View: **expanded_evaluation_v2_attribution** (separate protocol: structured evidence citations + observed_at; never merged with v1 or the submitted panel). VEA is a new metric; GSR keeps its original definition. Explicit citation is necessary for trace attribution but does not by itself prove correct reasoning; `decision_contradicts_cited_evidence` reports where the decision disagrees with the agent's own cited evidence.

| model | member | regime | n | TDA | GSR(original) | VEA | VEA_wilson95 | cited_any | all_citations_valid | cites_valid_physical | decision_supported | decision_contradicts_cited_evidence | GSR=1_but_VEA=0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | ALL | ALL | 500 | 52.0 | 52.0 | 52.0 | [0.476, 0.563] | 81.0 | 80.0 | 64.0 | 54.4 | 9.6 | 0 |
| Claude Opus 5.5 | cf_phys_out | FULL | 100 | 77.0 | 77.0 | 77.0 | [0.678, 0.842] | 77.0 | 77.0 | 77.0 | 77.0 | 0.0 | 0 |
| Claude Opus 5.5 | cf_phys_out | PHYSICAL_ONLY | 100 | 97.0 | 97.0 | 97.0 | [0.915, 0.990] | 97.0 | 97.0 | 97.0 | 97.0 | 0.0 | 0 |
| Claude Opus 5.5 | orig | DIGITAL_ONLY | 100 | 0.0 | 0.0 | 0.0 | [0.000, 0.037] | 85.0 | 80.0 | 0.0 | 0.0 | 0.0 | 0 |
| Claude Opus 5.5 | orig | FULL | 100 | 28.0 | 28.0 | 28.0 | [0.201, 0.375] | 65.0 | 65.0 | 65.0 | 33.0 | 32.0 | 0 |
| Claude Opus 5.5 | orig | PHYSICAL_ONLY | 100 | 58.0 | 58.0 | 58.0 | [0.482, 0.672] | 81.0 | 81.0 | 81.0 | 65.0 | 16.0 | 0 |
| DeepSeek V4 Pro 0813 | ALL | ALL | 500 | 75.6 | 65.2 | 62.8 | [0.585, 0.669] | 99.6 | 96.2 | 74.2 | 65.2 | 8.8 | 12 |
| DeepSeek V4 Pro 0813 | cf_phys_out | FULL | 100 | 97.0 | 97.0 | 91.0 | [0.838, 0.952] | 99.0 | 97.0 | 91.0 | 91.0 | 0.0 | 6 |
| DeepSeek V4 Pro 0813 | cf_phys_out | PHYSICAL_ONLY | 100 | 99.0 | 96.0 | 94.0 | [0.875, 0.972] | 100.0 | 98.0 | 95.0 | 94.0 | 0.0 | 2 |
| DeepSeek V4 Pro 0813 | orig | DIGITAL_ONLY | 100 | 49.0 | 0.0 | 0.0 | [0.000, 0.037] | 100.0 | 90.0 | 0.0 | 0.0 | 0.0 | 0 |
| DeepSeek V4 Pro 0813 | orig | FULL | 100 | 52.0 | 52.0 | 48.0 | [0.385, 0.577] | 99.0 | 98.0 | 88.0 | 54.0 | 34.0 | 4 |
| DeepSeek V4 Pro 0813 | orig | PHYSICAL_ONLY | 100 | 81.0 | 81.0 | 81.0 | [0.722, 0.875] | 100.0 | 98.0 | 97.0 | 87.0 | 10.0 | 0 |
| GPT-6-Astra | ALL | ALL | 500 | 65.6 | 65.4 | 65.4 | [0.611, 0.694] | 99.8 | 99.4 | 80.0 | 68.2 | 11.8 | 0 |
| GPT-6-Astra | cf_phys_out | FULL | 100 | 100.0 | 100.0 | 100.0 | [0.963, 1.000] | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 | 0 |
| GPT-6-Astra | cf_phys_out | PHYSICAL_ONLY | 100 | 100.0 | 100.0 | 100.0 | [0.963, 1.000] | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 | 0 |
| GPT-6-Astra | orig | DIGITAL_ONLY | 100 | 1.0 | 0.0 | 0.0 | [0.000, 0.037] | 99.0 | 97.0 | 0.0 | 0.0 | 0.0 | 0 |
| GPT-6-Astra | orig | FULL | 100 | 43.0 | 43.0 | 43.0 | [0.337, 0.528] | 100.0 | 100.0 | 100.0 | 50.0 | 50.0 | 0 |
| GPT-6-Astra | orig | PHYSICAL_ONLY | 100 | 84.0 | 84.0 | 84.0 | [0.756, 0.899] | 100.0 | 100.0 | 100.0 | 91.0 | 9.0 | 0 |
| Gemini 3.1 Pro Preview | ALL | ALL | 500 | 75.8 | 73.0 | 73.0 | [0.689, 0.767] | 84.0 | 84.0 | 78.4 | 75.8 | 2.6 | 0 |
| Gemini 3.1 Pro Preview | cf_phys_out | FULL | 100 | 98.0 | 98.0 | 98.0 | [0.930, 0.994] | 98.0 | 98.0 | 98.0 | 98.0 | 0.0 | 0 |
| Gemini 3.1 Pro Preview | cf_phys_out | PHYSICAL_ONLY | 100 | 99.0 | 99.0 | 99.0 | [0.946, 0.998] | 99.0 | 99.0 | 99.0 | 99.0 | 0.0 | 0 |
| Gemini 3.1 Pro Preview | orig | DIGITAL_ONLY | 100 | 14.0 | 0.0 | 0.0 | [0.000, 0.037] | 28.0 | 28.0 | 0.0 | 0.0 | 0.0 | 0 |
| Gemini 3.1 Pro Preview | orig | FULL | 100 | 81.0 | 81.0 | 81.0 | [0.722, 0.875] | 95.0 | 95.0 | 95.0 | 88.0 | 7.0 | 0 |
| Gemini 3.1 Pro Preview | orig | PHYSICAL_ONLY | 100 | 87.0 | 87.0 | 87.0 | [0.790, 0.922] | 100.0 | 100.0 | 100.0 | 94.0 | 6.0 | 0 |
| Qwen3.5-397B-A17B | ALL | ALL | 500 | 85.6 | 75.6 | 74.2 | [0.702, 0.778] | 100.0 | 95.8 | 78.8 | 77.2 | 1.6 | 7 |
| Qwen3.5-397B-A17B | cf_phys_out | FULL | 100 | 100.0 | 100.0 | 98.0 | [0.930, 0.994] | 100.0 | 98.0 | 98.0 | 98.0 | 0.0 | 2 |
| Qwen3.5-397B-A17B | cf_phys_out | PHYSICAL_ONLY | 100 | 100.0 | 100.0 | 98.0 | [0.930, 0.994] | 100.0 | 98.0 | 99.0 | 99.0 | 0.0 | 2 |
| Qwen3.5-397B-A17B | orig | DIGITAL_ONLY | 100 | 50.0 | 0.0 | 0.0 | [0.000, 0.037] | 100.0 | 86.0 | 0.0 | 0.0 | 0.0 | 0 |
| Qwen3.5-397B-A17B | orig | FULL | 100 | 88.0 | 88.0 | 86.0 | [0.779, 0.915] | 100.0 | 98.0 | 98.0 | 93.0 | 5.0 | 2 |
| Qwen3.5-397B-A17B | orig | PHYSICAL_ONLY | 100 | 90.0 | 90.0 | 89.0 | [0.814, 0.937] | 100.0 | 99.0 | 99.0 | 96.0 | 3.0 | 1 |

## Decision sensitivity to the delivered physical reading (matched pairs)

| model | regime | pairs | P(ESC|orig) | P(ESC|cf) | sensitivity_delta | delta_ci95 | mcnemar_p | correct_flip_rate(COMMIT->ESCALATE) | any_flip_rate |
|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | FULL | 100 | 37.0 | 77.0 | 0.4 | [0.260, 0.530] | 2.78e-07 | 26.0 | 64.0 |
| Claude Opus 5.5 | PHYSICAL_ONLY | 100 | 23.0 | 97.0 | 0.74 | [0.650, 0.820] | 1.06e-22 | 55.0 | 77.0 |
| GPT-6-Astra | FULL | 100 | 57.0 | 100.0 | 0.43 | [0.330, 0.530] | 2.27e-13 | 43.0 | 43.0 |
| GPT-6-Astra | PHYSICAL_ONLY | 100 | 16.0 | 100.0 | 0.84 | [0.760, 0.910] | 1.03e-25 | 84.0 | 84.0 |
| DeepSeek V4 Pro 0813 | FULL | 100 | 47.0 | 97.0 | 0.5 | [0.400, 0.600] | 1.78e-15 | 49.0 | 50.0 |
| DeepSeek V4 Pro 0813 | PHYSICAL_ONLY | 100 | 19.0 | 99.0 | 0.8 | [0.710, 0.880] | 3.43e-23 | 81.0 | 82.0 |
| Gemini 3.1 Pro Preview | FULL | 100 | 14.0 | 98.0 | 0.84 | [0.760, 0.910] | 1.03e-25 | 79.0 | 86.0 |
| Gemini 3.1 Pro Preview | PHYSICAL_ONLY | 100 | 13.0 | 99.0 | 0.86 | [0.790, 0.920] | 2.58e-26 | 86.0 | 87.0 |
| Qwen3.5-397B-A17B | FULL | 100 | 12.0 | 100.0 | 0.88 | [0.810, 0.940] | 6.46e-27 | 88.0 | 88.0 |
| Qwen3.5-397B-A17B | PHYSICAL_ONLY | 100 | 10.0 | 100.0 | 0.9 | [0.840, 0.960] | 1.62e-27 | 90.0 | 90.0 |
