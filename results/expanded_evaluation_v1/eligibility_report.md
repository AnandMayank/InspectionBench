# Expanded evaluation v1: eligibility report

Written before any expanded run. Script `scripts/10_eligibility.py`. Excluded episodes are listed one per row in `eligibility_exclusions.csv`. The per-pool frozen lists consumed by the runner are in `eligible/`.

| pool | constructed | valid | executable | excluded | to_evaluate | units | source | source_sha256 |
|---|---|---|---|---|---|---|---|---|
| A | 2400 | 2400 | 2400 | 12 | 2388 | 796 worlds | a_e_pool_manifest.json | 6db2113ebd587956 |
| E | 1440 | 1440 | 1440 | 33 | 1407 | 469 sequences; 10 kept sequences share some (not all) episode fingerprints with another sequence | a_e_pool_manifest.json | 6db2113ebd587956 |
| B_acq | 66 | 66 | 66 | 0 | 66 | 66 episodes; templates {"B-ACQ-1": 12, "B-ACQ-2": 36, "B-ACQ-3": 12, "B-ACQ-4": 6} | b_acquisition_final_manifest.json | e9443564591ffff7 |
| B_legacy | 12 | 12 | 12 | 0 | 12 | 12 episodes | frozen_93_historical_manifest.json (B rows); runner manifest reports/ec/phase8h1_pilot_manifest.json sha d2b48c0b0c9e | d2b48c0b0c9ef19f |
| C | 112 | 112 | 112 | 0 | 112 | {"T-C-BATTERY_ABORT": 36, "T-C-PANEL_STUCK": 8, "T-C-WO_GATE": 8, "T-C-PRECEDENCE": 4, "T-C-LOCALIZATION_ABORT": 24, "T-C-WAYPOINT_ESCALATE": 8, "T-C-ROUTE_BUDGET": 24} | cd_4000_final_manifest.json | 749a44db18c4f982 |
| D_enterprise | 20 | 20 | 16 | 4 | 16 | {"T-D-WO_GATE": 8, "T-D-WO_SIMILARITY": 8, "T-D-ROUTE_DEPENDENCY": 4} | cd_4000_final_manifest.json | 749a44db18c4f982 |
| D_physical | 70 | 70 | 70 | 0 | 70 | 70 canonical (88 generated before fingerprint dedup) | d_physical_canonical_manifest.json | 52f34ab7c9855ee5 |
| TOTAL | 4120 | 4120 | 4116 | 49 | 4071 |  |  |  |

## Exclusion reasons

| pool | reason | n |
|---|---|---|
| A | observationally identical | 12 |
| D_enterprise | template defect: navigate_to drops waypoint arg, pose never updates; COMMIT gold unreachable (camera_ready_revision_report_20261030.md s2B; paper G.2) | 4 |
| E | sequence observationally identical | 33 |

Notes:
- 'valid' means that, for A and E, rebuilding the world from its recorded seed reproduces the manifest `world_hash` and recomputed gold equals stored gold (`phase8k1_world_identity_sweep.check_ae_pool_row`). For B, C and D, gold is template- or oracle-derived and stored in the manifest.
- 'Fingerprint collision' means two different seeds produced worlds whose recorded observable fields (asset, physical value, IoT value, WO, technician) are identical after rounding. These are the source of the manifest's 45-episode A/E dedup note. Evaluating both would count one observable world twice.
- The paper's 4,120 is the undeduplicated sum. The manifest's own net total is 4,075.
