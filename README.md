# InspectionBench

**Evidence-Grounded Evaluation of Agentic Industrial Inspection**

*Anonymous repository for double-blind review.*

InspectionBench is an execution-grounded benchmark for agentic physical AI in industrial
inspection. An agent receives an alert and asset context, acquires visual, operational,
and telemetry evidence through tool calls, and turns the returned observations into an
operational decision — `COMMIT`, `ESCALATE`, or `ABORT` — before issuing the matching
enterprise action. Unlike benchmarks that supply evidence in the prompt, InspectionBench
scores whether the agent actually acquired the evidence it relied on: a plausible-looking
terminal decision is only credited if the delivered observations satisfy the grounding
contract behind it.

## Why this benchmark

Industrial monitoring produces alerts, not decisions. An autonomous inspection agent must
decide what to inspect, which evidence channel to use, when it has acquired enough, whether
the required procedure was actually completed, whether the proposed physical action is
admissible, and whether evidence acquired earlier is still valid by the time it commits.
InspectionBench operationalizes each of these questions as an independent, scored
capability, rather than a single leaderboard number.

| Capability | Question it answers |
|---|---|
| **A** — Evidence grounding | Did the terminal decision actually follow from evidence the agent received? |
| **B** — Evidence acquisition | Did the agent recognize what evidence it needed and select the right acquisition? |
| **C** — Procedural execution | Did the inspection actually happen, or just produce a plausible tool trace? |
| **D** — Relational physical grounding | Does the agent understand the physical constraint governing its proposed action? |
| **E** — Temporal grounding | Is the evidence still valid when the agent finally commits? |

## Dataset at a glance

- **4,120** canonical episodes generated from **1,552** grounded worlds and **21**
  scenario templates across six industrial asset types.
- **116** facility-collected images, **1,296** procedurally rendered perception scenes,
  and **24,601** replayed operational records (IoT, acoustic, thermal, access-geometry,
  visual-defect, work-order-history), each carrying an explicit evidence-provenance class.
- A **world-to-scenario compiler** that holds a world's physical state and gold decision
  fixed while varying only what the agent can observe or access (evidence visibility,
  modality/tool access, temporal validity), certified with a world-state hash so that a
  score difference inside a matched set is attributable only to what the agent could
  reach — never to a silently different world.
- **25** agent-visible tools spanning two backends (a Spot-SDK-shaped robot interface and
  an enterprise asset-management interface), covering seven evidence modalities.

## Repository layout

```
InspectionBench/
├── README.md
├── src/                          # core compiler and scoring modules
│   ├── scenario_gen.py           # asset registry, world construction (A-family)
│   ├── scenario_contract.py      # evidence-provenance classes, scenario binding
│   ├── cd_generator.py           # parameterized C/D template generator + scorer
│   ├── sequence_executor.py      # multi-episode sequence generator (E-family)
│   ├── classc_fixtures.py        # hand-authored procedural fixture set (C-family)
│   ├── couchdb_executor.py       # server-backed tool-execution environment
│   ├── tool_executor.py          # tool-call dispatch and result contract
│   ├── execution_trace.py        # tamper-evident, hash-chained execution trace
│   ├── l3_scoring.py             # terminal-action normalization/comparison
│   ├── l3_grounded_scoring.py    # grounded success rate (GSR) scoring
│   └── ordering.py               # procedural ordering-satisfaction check
├── data/examples/                # one complete compiled episode per capability
│   ├── example_A_evidence_grounding.json
│   ├── example_B_evidence_acquisition.json
│   ├── example_C_procedural_execution.json
│   ├── example_D_physical_grounding.json
│   └── example_E_temporal_grounding.json
└── figures/                      # capability-score and grounding-gap figures
```

## Results

![Capability scores by model](figures/figure5_capability_heatmap.png)

Terminal-decision accuracy (TDA) substantially overstates evidence-grounded success (GSR)
for every model evaluated — a policy that always escalates reaches high terminal accuracy
on this pool while acquiring no evidence at all, scoring zero on GSR.

![Terminal vs. grounded success](figures/figure6_evidence_grounding_gap.png)

The same pattern reappears in physical grounding: a model can reach the correct
terminal decision while still failing to recover *which* physical constraint made that
decision correct.

![Decisions vs. physical constraints](figures/figure7_physical_grounding_gap.png)

Matching a world across evidence-access regimes (`FULL` / `PHYSICAL_ONLY` / `DIGITAL_ONLY`)
while holding the underlying fault state fixed exposes a further failure: several models'
terminal accuracy barely drops under `DIGITAL_ONLY`, despite having no physical evidence
to ground a decision in.

![Matched-regime channel substitution](figures/figure_matched_regime_channel_substitution.png)

## Scoring contract

Every success predicate is a pure function of the agent's response and its execution
trace — none are LLM-judged. The primary predicates are conjunctive: a decision is
credited as grounded only if the required observation was actually delivered (non-null
observation identifier, successful tool execution), its provenance hash-chain verifies,
the agent's citation (if any) matches a delivered observation of the required modality,
and no forbidden action was executed. Full per-capability predicate definitions (TDA,
GSR, ADA, ASA, UHA, procedural coverage, ordering satisfaction, CSA, LCA, TVR) are
reproduced in `src/` docstrings and match the released scoring code exactly — nothing in
this repository is illustrative-only.

## Example episode

`data/examples/example_D_physical_grounding.json` is a compiled physical-admissibility
episode: an agent must recognize that an open corrective work order on the target asset
means the correct action is `ESCALATE`, not `DISPATCH`, and that doing so requires calling
`list_waypoints`, `get_battery`, `navigate_to`, and `get_work_order` — in that order —
before deciding. The full execution trace is tamper-evident: every event stores a hash of
its predecessor, so a score difference can always be traced back to what the agent actually
did, not to an ambiguous record.

## Status

This repository accompanies a paper currently under double-blind review. It is provided
for reviewer inspection of the benchmark's construction, scoring contract, and example
data. Full evaluation results, trained-model outputs, and the complete evidence substrate
will be released on publication.

## License

Released for review purposes. A permissive open-source license will be finalized on
publication.
