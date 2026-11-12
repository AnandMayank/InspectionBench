# Expanded evaluation v1 analysis — run `v1__main_merged`

View: **expanded_evaluation_v1** (new API calls, frozen protocol; never mixed with the as-submitted panel).

## Coverage

| model | pool | eligible_units | persisted_units | coverage | infra_failed_units |
|---|---|---|---|---|---|
| Claude Opus 5.5 | A | 2388 | 2388 | 100.0 | 0 |
| Claude Opus 5.5 | E | 469 | 469 | 100.0 | 0 |
| Claude Opus 5.5 | B_acq | 66 | 66 | 100.0 | 0 |
| Claude Opus 5.5 | B_legacy | 12 | 12 | 100.0 | 0 |
| Claude Opus 5.5 | C | 112 | 112 | 100.0 | 0 |
| Claude Opus 5.5 | D_enterprise | 16 | 16 | 100.0 | 0 |
| Claude Opus 5.5 | D_physical | 70 | 70 | 100.0 | 0 |
| GPT-6-Astra | A | 2388 | 2388 | 100.0 | 0 |
| GPT-6-Astra | E | 469 | 469 | 100.0 | 0 |
| GPT-6-Astra | B_acq | 66 | 66 | 100.0 | 0 |
| GPT-6-Astra | B_legacy | 12 | 12 | 100.0 | 0 |
| GPT-6-Astra | C | 112 | 112 | 100.0 | 0 |
| GPT-6-Astra | D_enterprise | 16 | 16 | 100.0 | 0 |
| GPT-6-Astra | D_physical | 70 | 70 | 100.0 | 0 |
| DeepSeek V4 Pro 0813 | A | 2388 | 2388 | 100.0 | 0 |
| DeepSeek V4 Pro 0813 | E | 469 | 469 | 100.0 | 0 |
| DeepSeek V4 Pro 0813 | B_acq | 66 | 66 | 100.0 | 0 |
| DeepSeek V4 Pro 0813 | B_legacy | 12 | 12 | 100.0 | 0 |
| DeepSeek V4 Pro 0813 | C | 112 | 112 | 100.0 | 0 |
| DeepSeek V4 Pro 0813 | D_enterprise | 16 | 16 | 100.0 | 0 |
| DeepSeek V4 Pro 0813 | D_physical | 70 | 70 | 100.0 | 0 |
| Gemini 3.1 Pro Preview | A | 2388 | 2388 | 100.0 | 0 |
| Gemini 3.1 Pro Preview | E | 469 | 469 | 100.0 | 0 |
| Gemini 3.1 Pro Preview | B_acq | 66 | 66 | 100.0 | 0 |
| Gemini 3.1 Pro Preview | B_legacy | 12 | 12 | 100.0 | 0 |
| Gemini 3.1 Pro Preview | C | 112 | 112 | 100.0 | 0 |
| Gemini 3.1 Pro Preview | D_enterprise | 16 | 16 | 100.0 | 0 |
| Gemini 3.1 Pro Preview | D_physical | 70 | 70 | 100.0 | 0 |
| Qwen3.5-397B-A17B | A | 2388 | 2388 | 100.0 | 0 |
| Qwen3.5-397B-A17B | E | 469 | 469 | 100.0 | 0 |
| Qwen3.5-397B-A17B | B_acq | 66 | 66 | 100.0 | 0 |
| Qwen3.5-397B-A17B | B_legacy | 12 | 12 | 100.0 | 0 |
| Qwen3.5-397B-A17B | C | 112 | 112 | 100.0 | 0 |
| Qwen3.5-397B-A17B | D_enterprise | 16 | 16 | 100.0 | 0 |
| Qwen3.5-397B-A17B | D_physical | 70 | 70 | 100.0 | 0 |

GSR rescored from persisted traces; rows where rescored GSR differs from stored GSR: 0.

## A gap decomposition

| model | convention | n | TDA_pct | GSR_pct | gap_pp | mechanical_pp=(nDIG/n)*TDA_DIG | residual_pp(nonDIG TDA=1,GSR=0) |
|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | dropped(paper) | 2359 | 74.1416 | 50.9962 | 23.1454 | 22.7639 | 0.381518 |
| Claude Opus 5.5 | A1(missing=0) | 2388 | 73.2412 | 50.3769 | 22.8643 | 22.4874 | 0.376884 |
| GPT-6-Astra | dropped(paper) | 2388 | 73.995 | 51.2982 | 22.6968 | 22.6549 | 0.041876 |
| GPT-6-Astra | A1(missing=0) | 2388 | 73.995 | 51.2982 | 22.6968 | 22.6549 | 0.041876 |
| DeepSeek V4 Pro 0813 | dropped(paper) | 2370 | 69.9156 | 48.1435 | 21.7722 | 19.789 | 1.98312 |
| DeepSeek V4 Pro 0813 | A1(missing=0) | 2388 | 69.3886 | 47.7806 | 21.608 | 19.6399 | 1.96817 |
| Gemini 3.1 Pro Preview | dropped(paper) | 2373 | 62.1576 | 53.9823 | 8.17531 | 8.17531 | 0 |
| Gemini 3.1 Pro Preview | A1(missing=0) | 2388 | 61.7672 | 53.6432 | 8.12395 | 8.12395 | 0 |
| Qwen3.5-397B-A17B | dropped(paper) | 2364 | 72.6311 | 52.5804 | 20.0508 | 19.9239 | 0.126904 |
| Qwen3.5-397B-A17B | A1(missing=0) | 2388 | 71.9012 | 52.0519 | 19.8492 | 19.7236 | 0.125628 |

## R1 and LLMs under DIGITAL_ONLY by digital decidability

| world_subset | n_worlds | policy | TDA | balanced_accuracy | agreement_with_R1 |
|---|---|---|---|---|---|
| ALL | 800 | R1 digital-only rule | 66.9 | 62.3 | None |
| ALL | 800 | always-ESCALATE | 67.6 | 50.0 | None |
| ALL | 800 | LLM Claude Opus 5.5 (DIGITAL_ONLY) | 67.5 | 50.3 | 0.679648 |
| ALL | 800 | LLM GPT-6-Astra (DIGITAL_ONLY) | 68.0 | 50.0 | 0.672111 |
| ALL | 800 | LLM DeepSeek V4 Pro 0813 (DIGITAL_ONLY) | 58.9 | 55.8 | 0.792714 |
| ALL | 800 | LLM Gemini 3.1 Pro Preview (DIGITAL_ONLY) | 24.4 | 20.8 | 0.282663 |
| ALL | 800 | LLM Qwen3.5-397B-A17B (DIGITAL_ONLY) | 59.2 | 52.1 | 0.778894 |
| digitally_determined | 535 | R1 digital-only rule | 100.0 | 100.0 | None |
| digitally_determined | 535 | always-ESCALATE | 76.1 | 50.0 | None |
| digitally_determined | 535 | LLM Claude Opus 5.5 (DIGITAL_ONLY) | 76.6 | 51.9 | 0.765918 |
| digitally_determined | 535 | LLM GPT-6-Astra (DIGITAL_ONLY) | 76.2 | 50.0 | 0.762172 |
| digitally_determined | 535 | LLM DeepSeek V4 Pro 0813 (DIGITAL_ONLY) | 79.0 | 84.3 | 0.790262 |
| digitally_determined | 535 | LLM Gemini 3.1 Pro Preview (DIGITAL_ONLY) | 30.3 | 27.5 | 0.303371 |
| digitally_determined | 535 | LLM Qwen3.5-397B-A17B (DIGITAL_ONLY) | 77.7 | 73.5 | 0.777154 |
| digitally_undecidable | 265 | R1 digital-only rule | 0.0 | 0.0 | None |
| digitally_undecidable | 265 | always-ESCALATE | 50.6 | 50.0 | None |
| digitally_undecidable | 265 | LLM Claude Opus 5.5 (DIGITAL_ONLY) | 48.9 | 47.8 | 0.503817 |
| digitally_undecidable | 265 | LLM GPT-6-Astra (DIGITAL_ONLY) | 51.1 | 50.0 | 0.48855 |
| digitally_undecidable | 265 | LLM DeepSeek V4 Pro 0813 (DIGITAL_ONLY) | 17.9 | 17.5 | 0.79771 |
| digitally_undecidable | 265 | LLM Gemini 3.1 Pro Preview (DIGITAL_ONLY) | 12.2 | 11.9 | 0.240458 |
| digitally_undecidable | 265 | LLM Qwen3.5-397B-A17B (DIGITAL_ONLY) | 21.4 | 20.9 | 0.782443 |

## Paired FULL vs withheld (Holm within family)

| model | family | value | contrast | n_worlds | delta_pp | delta_ci95_pp | p_holm | significant_0.05 |
|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | F1 | ALL | FULL-DIGITAL_ONLY | 796 | 8.9 | [6.2, 11.8] | 4.75775e-09 | True |
| Claude Opus 5.5 | F1 | ALL | FULL-PHYSICAL_ONLY | 796 | 0.5 | [-2.3, 3.3] | 1 | False |
| Claude Opus 5.5 | F3 | determined | FULL-DIGITAL_ONLY | 534 | 10.5 | [6.6, 14.4] | 1.90864e-06 | True |
| Claude Opus 5.5 | F3 | undecidable | FULL-DIGITAL_ONLY | 262 | 5.7 | [3.1, 8.8] | 0.000244141 | True |
| GPT-6-Astra | F1 | ALL | FULL-DIGITAL_ONLY | 796 | 7.4 | [4.3, 10.6] | 3.48843e-05 | True |
| GPT-6-Astra | F1 | ALL | FULL-PHYSICAL_ONLY | 796 | -3.3 | [-6.7, 0.3] | 0.354598 | False |
| GPT-6-Astra | F3 | determined | FULL-DIGITAL_ONLY | 534 | 11 | [6.4, 15.7] | 2.90703e-05 | True |
| GPT-6-Astra | F3 | undecidable | FULL-DIGITAL_ONLY | 262 | 0 | [0.0, 0.0] | 1 | False |
| DeepSeek V4 Pro 0813 | F1 | ALL | FULL-DIGITAL_ONLY | 796 | 14.9 | [11.9, 18.0] | 5.30421e-20 | True |
| DeepSeek V4 Pro 0813 | F1 | ALL | FULL-PHYSICAL_ONLY | 796 | -1.5 | [-4.8, 1.8] | 1 | False |
| DeepSeek V4 Pro 0813 | F3 | determined | FULL-DIGITAL_ONLY | 534 | 5.1 | [1.9, 8.2] | 0.00954903 | True |
| DeepSeek V4 Pro 0813 | F3 | undecidable | FULL-DIGITAL_ONLY | 262 | 35.1 | [29.4, 40.8] | 6.71478e-26 | True |
| Gemini 3.1 Pro Preview | F1 | ALL | FULL-DIGITAL_ONLY | 796 | 56.4 | [52.4, 60.4] | 5.98711e-103 | True |
| Gemini 3.1 Pro Preview | F1 | ALL | FULL-PHYSICAL_ONLY | 796 | 0.6 | [-1.8, 3.0] | 1 | False |
| Gemini 3.1 Pro Preview | F3 | determined | FULL-DIGITAL_ONLY | 534 | 45.9 | [40.6, 50.9] | 6.70295e-49 | True |
| Gemini 3.1 Pro Preview | F3 | undecidable | FULL-DIGITAL_ONLY | 262 | 77.9 | [72.9, 82.8] | 7.77877e-61 | True |
| Qwen3.5-397B-A17B | F1 | ALL | FULL-DIGITAL_ONLY | 796 | 20.4 | [16.2, 24.6] | 2.67304e-19 | True |
| Qwen3.5-397B-A17B | F1 | ALL | FULL-PHYSICAL_ONLY | 796 | 2.5 | [-0.4, 5.5] | 0.462159 | False |
| Qwen3.5-397B-A17B | F3 | determined | FULL-DIGITAL_ONLY | 534 | 0.6 | [-3.9, 5.1] | 1 | False |
| Qwen3.5-397B-A17B | F3 | undecidable | FULL-DIGITAL_ONLY | 262 | 60.7 | [54.6, 66.8] | 8.86759e-46 | True |

## B / C / D

| ADA | ASA | CC | CC_wilson95 | CSA | CS_F1 | CS_precision | CS_recall | LCA | MAR | TDA_post | UAR | UHA | capability | clusters(template x asset) | coverage(recall) | coverage_ci95(template x asset) | errors | f1 | forbidden_violation | model | n | ordering | precision | required_action_recall | view |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.933333 |  |  |  |  |  |  |  | 0 | 0.257576 | 0 | 0.75 | B | 15 |  |  |  |  |  | Claude Opus 5.5 | 66 |  |  |  | expanded_evaluation_v1 |
|  |  | 0.366071 |  |  |  |  |  |  |  |  |  |  | C |  | 0.422885 | [0.340, 0.518] |  | 0.475048 | 0 | Claude Opus 5.5 | 112 | 0.598214 | 0.744554 |  | expanded_evaluation_v1 |
|  |  | 0.871429 |  | 0.514286 | 0.701786 | 0.871429 | 0.630952 | 0.5 |  |  |  |  | D_physical |  |  |  | 0 |  |  | Claude Opus 5.5 | 70 |  |  |  | expanded_evaluation_v1 |
|  |  | 0.6875 | [0.44, 0.86] |  |  |  |  |  |  |  |  |  | D_enterprise |  |  |  |  |  |  | Claude Opus 5.5 | 16 |  |  | 0.319196 | expanded_evaluation_v1 |
| 1 | 0.933333 |  |  |  |  |  |  |  | 0 | 0.227273 | 0 | 1 | B | 15 |  |  |  |  |  | GPT-6-Astra | 66 |  |  |  | expanded_evaluation_v1 |
|  |  | 0.366071 |  |  |  |  |  |  |  |  |  |  | C |  | 0.339392 | [0.283, 0.408] |  | 0.437923 | 0 | GPT-6-Astra | 112 | 0.785714 | 0.83536 |  | expanded_evaluation_v1 |
|  |  | 0.9 |  | 0.5 | 0.682143 | 0.871429 | 0.607143 | 0.446429 |  |  |  |  | D_physical |  |  |  | 0 |  |  | GPT-6-Astra | 70 |  |  |  | expanded_evaluation_v1 |
|  |  | 0.75 | [0.51, 0.90] |  |  |  |  |  |  |  |  |  | D_enterprise |  |  |  |  |  |  | GPT-6-Astra | 16 |  |  | 0.196429 | expanded_evaluation_v1 |
| 1 | 0.933333 |  |  |  |  |  |  |  | 0 | 0.424242 | 0 | 1 | B | 15 |  |  |  |  |  | DeepSeek V4 Pro 0813 | 66 |  |  |  | expanded_evaluation_v1 |
|  |  | 0.616071 |  |  |  |  |  |  |  |  |  |  | C |  | 0.365221 | [0.306, 0.435] |  | 0.453227 | 0.0982143 | DeepSeek V4 Pro 0813 | 112 | 0.758929 | 0.818895 |  | expanded_evaluation_v1 |
|  |  | 0.714286 |  | 0.514286 | 0.573214 | 0.728571 | 0.529762 | 0.428571 |  |  |  |  | D_physical |  |  |  | 0 |  |  | DeepSeek V4 Pro 0813 | 70 |  |  |  | expanded_evaluation_v1 |
|  |  | 1 | [0.81, 1.00] |  |  |  |  |  |  |  |  |  | D_enterprise |  |  |  |  |  |  | DeepSeek V4 Pro 0813 | 16 |  |  | 0.196429 | expanded_evaluation_v1 |
| 1 | 0.933333 |  |  |  |  |  |  |  | 0 | 0.712121 | 0 | 1 | B | 15 |  |  |  |  |  | Gemini 3.1 Pro Preview | 66 |  |  |  | expanded_evaluation_v1 |
|  |  | 0.366071 |  |  |  |  |  |  |  |  |  |  | C |  | 0.141582 | [0.079, 0.220] |  | 0.180942 | 0.125 | Gemini 3.1 Pro Preview | 112 | 1 | 0.301786 |  | expanded_evaluation_v1 |
|  |  | 0.742857 |  | 0.385714 | 0.580952 | 0.728571 | 0.511905 | 0.357143 |  |  |  |  | D_physical |  |  |  | 0 |  |  | Gemini 3.1 Pro Preview | 70 |  |  |  | expanded_evaluation_v1 |
|  |  | 0.875 | [0.64, 0.97] |  |  |  |  |  |  |  |  |  | D_enterprise |  |  |  |  |  |  | Gemini 3.1 Pro Preview | 16 |  |  | 0.165179 | expanded_evaluation_v1 |
| 1 | 0.933333 |  |  |  |  |  |  |  | 0 | 0.772727 | 0 | 1 | B | 15 |  |  |  |  |  | Qwen3.5-397B-A17B | 66 |  |  |  | expanded_evaluation_v1 |
|  |  | 0.669643 |  |  |  |  |  |  |  |  |  |  | C |  | 0.274607 | [0.232, 0.327] |  | 0.375921 | 0 | Qwen3.5-397B-A17B | 112 | 0.741071 | 0.786756 |  | expanded_evaluation_v1 |
|  |  | 0.828571 |  | 0.457143 | 0.616667 | 0.8 | 0.547619 | 0.392857 |  |  |  |  | D_physical |  |  |  | 0 |  |  | Qwen3.5-397B-A17B | 70 |  |  |  | expanded_evaluation_v1 |
|  |  | 1 | [0.81, 1.00] |  |  |  |  |  |  |  |  |  | D_enterprise |  |  |  |  |  |  | Qwen3.5-397B-A17B | 16 |  |  | 0.205357 | expanded_evaluation_v1 |

## E

| TC=mean_CC_grounded | TC_seq_ci95 | TDA(CC) | budget_refused_read | episodes | fresh_observation | model | no_current_or_prior_observation | reused_earlier_observation | seqs_with_3_grounded | sequences | view |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.389481 | [0.367, 0.412] | 0.63113 | 449 | 1407 | 835 | Claude Opus 5.5 | 23 | 100 | 0 | 469 | expanded_evaluation_v1 |
| 0.564321 | [0.549, 0.580] | 0.653873 | 455 | 1407 | 927 | GPT-6-Astra |  | 25 | 0 | 469 | expanded_evaluation_v1 |
| 0.560057 | [0.543, 0.576] | 0.704335 | 463 | 1407 | 938 | DeepSeek V4 Pro 0813 | 6 |  | 0 | 469 | expanded_evaluation_v1 |
| 0.573561 | [0.559, 0.588] | 0.573561 | 469 | 1407 | 938 | Gemini 3.1 Pro Preview |  |  | 0 | 469 | expanded_evaluation_v1 |
| 0.432836 | [0.419, 0.448] | 0.703625 | 753 | 1407 | 647 | Qwen3.5-397B-A17B | 2 | 5 | 4 | 469 | expanded_evaluation_v1 |
