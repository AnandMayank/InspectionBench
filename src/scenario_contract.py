"""scenario_contract.py — Unified typed gold contract (Pass R1).

Before this module, gold for the 89 ``scenario_R*/`` directories was scattered
across three drifted registries that could each disagree: ``l3_arms.SCENARIOS``
(a hardcoded dict, and the one actually consulted by the live scoring path for
the 15 scenarios it covers), ``Scenarios/gold_robot_inspection.json`` (54
entries, generator-authored), and free-form prose in each scenario's own
``groundtruth.txt`` (two competing conventions, ``Expected verdict:`` on 61
dirs and ``Gold decision:`` on 26, with 2 dirs — R021, R025 — parsing under
neither because their gold lives only inside a ``Gold answer:`` JSON blob).

This module builds one ``ScenarioGold`` per scenario id by reading those
sources in a fixed, documented priority order (never inventing a value), and
is the new canonical entry point for scenario gold going forward.
``groundtruth.txt`` becomes a *rendering* of the typed record, never a second
source of truth: ``render_groundtruth_header`` produces the header lines a
scorer would parse, and round-trips through ``_parse_groundtruth``.

**Source priority per scenario id (highest first):**
1. ``l3_arms.SCENARIOS`` — execution-authoritative. This is the dict the live
   thermal/pilot scoring path (``run_thermal_pilot.py`` via
   ``l3_arms.arms_for``) actually reads today; overriding it here without
   also updating ``l3_arms.py`` would create a fourth drifted source, so R1
   instead makes ``l3_arms.SCENARIOS`` the thing this registry *agrees with*
   for the 15 ids it covers (see ``build_registry``'s cross-check).
2. ``Scenarios/gold_robot_inspection.json`` — generator-authored, 54 entries.
3. Parsed ``groundtruth.txt`` — the fallback for the 35 dirs neither source
   covers, using both header conventions and, for R021/R025, the
   ``Gold answer:`` JSON-blob fallback.

**gold_source** (R4's contract, declared honestly starting now): every record
this pass produces is ``sme_adjudicated`` (hand-authored procedural/gauge
scenarios) or ``externally_mapped`` (FM-26 thermal, whose gold traces to the
Mendeley dataset's own ``fault_class``). **No record is ``derived_from_world``
yet** — that requires the latent WORLD object R4 introduces; a typed registry
is a necessary precondition for ``GOLD=f(W)``, not an instance of it.

**evidence_provenance_class**: the binding L1/L2/L3 taxonomy (plan §R0-PRE)
was defined over *physical-evidence records* (photographs/audio files in
``observation_records.json``) and classifies FM-26 thermal as L2 (Mendeley
rig, not the AssetOpsBench asset itself). It does not have a category for the
gauge/panel scenarios' *procedurally rendered* dial images (``render_gauge``
in ``tool_executor.py``) — those are neither a real external recording (L2)
nor evidence-free (L3, "no embodied inspection loop": these scenarios do
dispatch/navigate/read). This module marks them ``SIMULATED_UNCLASSIFIED``
rather than force-fitting L2 or L3, and flags the gap explicitly in the R1
report rather than deciding it unilaterally.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import l3_arms  # noqa: E402  (sibling module, already on sys.path via callers)

SCEN_ROOT = l3_arms.SCEN_ROOT
GOLD_JSON_PATH = SCEN_ROOT / "Scenarios" / "gold_robot_inspection.json"
TYPED_REGISTRY_PATH = SCEN_ROOT / "Scenarios" / "gold_typed.json"

CONTRACT_VERSION = "1.0.0"

GoldAction = Union[str, Tuple[str, ...]]

GOLD_SOURCE_VALUES = ("derived_from_world", "sme_adjudicated", "externally_mapped")
PROVENANCE_VALUES = (
    "L1_REAL_ASSET_EVIDENCE",
    "L2_ASSET_CLASS_EVIDENCE_REPLAY",
    "L3_EVIDENCE_DIAGNOSTIC",
    "SIMULATED_UNCLASSIFIED",
)

#: FM families whose gold is externally_mapped (traces to an external
#: dataset's own fault_class), never sme_adjudicated. Everything else in this
#: registry today is hand-authored gauge/panel/work-order scenario content.
#: FM-29 is NOT listed here: only ONE of its two scenarios (R091, the
#: source_label=normal control) auto-maps by the general MIMII policy --
#: R090 (source_label=abnormal) required a scenario-specific SME mapping,
#: which _classify() cannot express per-FM. See _GOLD_SOURCE_OVERRIDE below.
EXTERNALLY_MAPPED_FMS = {"FM-26"}

#: FM families with real evidence acquired from an analogous-but-not-same
#: asset (Mendeley motor rig / MIMII pump rig, not the AssetOpsBench asset
#: itself) — L2 per the binding R0-PRE taxonomy.
L2_FMS = {"FM-26", "FM-29"}

#: PASS R3: per-scenario gold_source overrides, for the one case a per-FM
#: table cannot express -- FM-29's two scenarios split across both values
#: (see EXTERNALLY_MAPPED_FMS's note). Never used to override
#: evidence_provenance_class (that IS uniform per-FM here: both are L2).
_GOLD_SOURCE_OVERRIDE: Dict[str, str] = {
    "R090": "sme_adjudicated",   # abnormal clip; ESCALATE gold authored for this scenario only
    "R091": "externally_mapped",  # normal clip; gold_action=COMMIT is MIMII's own general policy
    # PASS R4: the six scenarios world.derive_gold_gauge_band reproduces
    # exactly (verified by world.verify_gauge_band_derivation, and by
    # test_world_gold.py::test_derived_from_world_list_matches_world_module,
    # which fails loudly if this list and world.GAUGE_BAND_DERIVED_SCENARIOS
    # ever diverge -- duplicated here rather than imported, to avoid a
    # scenario_contract <-> world circular import).
    "R009": "derived_from_world", "R015": "derived_from_world",
    "R055": "derived_from_world", "R056": "derived_from_world",
    "R057": "derived_from_world", "R058": "derived_from_world",
}


#: Deliberately restrictive: matches only ALL-CAPS action token(s), optionally
#: joined by '/' or 'or', and stops at the first lowercase word. Several
#: groundtruth.txt lines carry trailing prose after the verdict --
#: "COMMIT with accurate PA score", "ESCALATE if WO similarity returns high
#: match..." -- and an earlier permissive ``[A-Za-z_/ ]+`` pattern silently
#: swallowed that prose as part of the "verdict", manufacturing false
#: cross-source conflicts against gold_robot_inspection.json's precise values.
_ACTION_TOKEN = r"[A-Z][A-Z_]*"
_GOLD1 = re.compile(rf"Expected verdict:\s*({_ACTION_TOKEN}(?:\s*(?:/|or)\s*{_ACTION_TOKEN})*)")
_GOLD2 = re.compile(rf"Gold decision:\s*({_ACTION_TOKEN}(?:\s*(?:/|or)\s*{_ACTION_TOKEN})*)")
_FM1 = re.compile(r"FM flag:\s*([A-Za-z0-9\-]+)")
_FM2 = re.compile(r"Gold fm_flag:\s*([A-Za-z0-9_\-]+|null)")
#: R021/R025 fallback: no header line at all, gold lives only in the
#: `Gold answer:` JSON-ish blob, e.g. `"verdict": "ESCALATE"`.
_GOLD_BLOB = re.compile(r'"verdict"\s*:\s*"([A-Za-z_]+)"')


@dataclass
class ConditionalGold:
    """PASS R4: a typed, faithful representation of branching gold — the
    thing R1's scalar ``gold_action`` cannot express. R004 is the motivating
    case: "COMMIT if reading within 0.9-1.1 m3/s, else ESCALATE" is not one
    answer with a caveat, it is a genuine function of WORLD state, and R1
    silently picked one branch (via whichever source it read). This does
    NOT replace ``gold_action`` — it sits alongside it as the honest full
    picture; ``gold_action`` remains a single value chosen by the same R1
    priority rule, still flagged as a conflict where sources disagree.

    ``condition_field`` names the WORLD field the branch depends on
    (``scenario_contract`` does not evaluate arbitrary expressions — only
    ``world.derive_gold_gauge_band``-style band membership is implemented,
    see ``evaluate``). ``branches`` maps a human-readable condition outcome
    to the gold action for that outcome.
    """

    condition_field: str  # e.g. "value_in_band"
    condition_description: str  # human-readable, for the report/audit trail
    branches: Dict[str, str]  # {"true": "COMMIT", "false": "ESCALATE"}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ConditionalGold":
        return cls(**d)


@dataclass
class ScenarioGold:
    """One scenario's typed, versioned gold record."""

    scenario_id: str
    fm_code: Optional[str]
    asset_id: Optional[str]
    gold_action: GoldAction
    gold_source: str
    evidence_provenance_class: str
    verdict_convention: str  # which source/convention this was read from
    reason: Optional[str] = None
    required_minimal_procedure: Optional[List[str]] = None
    #: PASS R4: set only for scenarios whose real gold is conditional/
    #: branching (R004 today). None for every scalar-gold scenario — this
    #: is additive, not a replacement for gold_action.
    conditional_gold: Optional[ConditionalGold] = None
    #: Catch-all for the long tail of simulator-specific fields (cusum_S,
    #: wrong_rung_energy_J, ...) so migrating to a typed contract never
    #: silently discards information — R1 does not force every one-off field
    #: into a named column, it preserves them.
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.gold_source not in GOLD_SOURCE_VALUES:
            raise ValueError(f"{self.scenario_id}: invalid gold_source {self.gold_source!r}")
        if self.evidence_provenance_class not in PROVENANCE_VALUES:
            raise ValueError(
                f"{self.scenario_id}: invalid evidence_provenance_class "
                f"{self.evidence_provenance_class!r}"
            )
        if not self.gold_action or (
            isinstance(self.gold_action, (list, tuple)) and not any(self.gold_action)
        ):
            raise ValueError(f"{self.scenario_id}: empty gold_action")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if isinstance(self.gold_action, tuple):
            d["gold_action"] = list(self.gold_action)
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ScenarioGold":
        d = dict(d)
        ga = d.get("gold_action")
        if isinstance(ga, list):
            d["gold_action"] = tuple(ga)
        cg = d.get("conditional_gold")
        if isinstance(cg, dict):
            d["conditional_gold"] = ConditionalGold.from_dict(cg)
        return cls(**d)


#: PASS R4: scenarios whose real gold is conditional/branching, not a
#: scalar. R004's own groundtruth.txt states it explicitly ("Expected
#: verdict: COMMIT (if reading within 0.9-1.1 m3/s) or ESCALATE (if outside
#: band)") -- this is a hand transcription of that one scenario's real
#: structure, not a general parser (see ConditionalGold's docstring for why
#: a general parser is out of scope: condition_field names a WORLD field,
#: which only world.py's gauge-band rule currently evaluates).
_CONDITIONAL_GOLD_OVERRIDE: Dict[str, ConditionalGold] = {
    "R004": ConditionalGold(
        condition_field="value_in_band",
        condition_description="metro_pump_1 flow reading within the 0.9-1.1 m3/s operating band",
        branches={"true": "COMMIT", "false": "ESCALATE"},
    ),
}


def scenario_dir(scenario_id: str) -> Optional[Path]:
    return l3_arms.scenario_dir(scenario_id)


def _all_scenario_ids() -> List[str]:
    ids = []
    for d in sorted(SCEN_ROOT.glob("scenario_R*")):
        m = re.search(r"\d+", d.name)
        if m:
            ids.append(f"R{int(m.group()):03d}")
    return ids


def _load_gold_json() -> Dict[str, Any]:
    return json.loads(GOLD_JSON_PATH.read_text())


def _parse_groundtruth(text: str) -> Dict[str, Any]:
    """Parse a groundtruth.txt under either header convention, falling back
    to the `Gold answer:` JSON blob (R021/R025's only source of gold)."""
    v1, v2 = _GOLD1.search(text), _GOLD2.search(text)
    f1, f2 = _FM1.search(text), _FM2.search(text)
    if v1:
        verdict, convention = v1.group(1).strip(), "expected_verdict"
    elif v2:
        verdict, convention = v2.group(1).strip(), "gold_decision"
    else:
        blob = _GOLD_BLOB.search(text)
        if not blob:
            raise ValueError("no verdict found under any known convention or blob fallback")
        verdict, convention = blob.group(1).strip(), "gold_answer_blob"
    fm_flag = None
    if f1:
        fm_flag = f1.group(1).strip()
    elif f2 and f2.group(1) != "null":
        fm_flag = f2.group(1).strip()
    return {"verdict": verdict, "fm_flag": fm_flag, "convention": convention}


def _split_verdict(raw: str) -> GoldAction:
    """'ESCALATE / SHUTDOWN' or 'SHUTDOWN or ESCALATE' -> set-valued gold."""
    parts = re.split(r"\s*(?:/|,| or )\s*", raw.strip())
    parts = [p for p in parts if p]
    return tuple(parts) if len(parts) > 1 else parts[0]


def _classify(fm_code: Optional[str]) -> Tuple[str, str]:
    """(gold_source, evidence_provenance_class) for a given FM family."""
    if fm_code in EXTERNALLY_MAPPED_FMS:
        gold_source = "externally_mapped"
    else:
        gold_source = "sme_adjudicated"
    if fm_code in L2_FMS:
        provenance = "L2_ASSET_CLASS_EVIDENCE_REPLAY"
    else:
        provenance = "SIMULATED_UNCLASSIFIED"
    return gold_source, provenance


def _from_l3_arms(sid: str, manifest: Dict[str, Any]) -> ScenarioGold:
    meta = l3_arms.SCENARIOS[sid]
    fm_code = meta.get("fm") or manifest.get("fm_code")
    gold_source, provenance = _classify(fm_code)
    gold_source = _GOLD_SOURCE_OVERRIDE.get(sid, gold_source)
    gold_action = meta["gold"]
    if isinstance(gold_action, list):
        gold_action = tuple(gold_action)
    rmp = manifest.get("required_minimal_procedure")
    return ScenarioGold(
        scenario_id=sid, fm_code=fm_code, asset_id=meta.get("asset") or manifest.get("asset_id"),
        gold_action=gold_action, gold_source=gold_source,
        evidence_provenance_class=provenance, verdict_convention="l3_arms.SCENARIOS",
        required_minimal_procedure=list(rmp) if rmp else None,
        extra={"axis": meta.get("axis")},
    )


def _from_gold_json(sid: str, entry: Dict[str, Any], manifest: Dict[str, Any]) -> ScenarioGold:
    fm_code = entry.get("fm") or manifest.get("fm_code")
    gold_source, provenance = _classify(fm_code)
    rmp = manifest.get("required_minimal_procedure")
    extra = {k: v for k, v in entry.items()
             if k not in ("scenario", "fm", "asset", "verdict", "reason")}
    return ScenarioGold(
        scenario_id=sid, fm_code=fm_code, asset_id=entry.get("asset") or manifest.get("asset_id"),
        gold_action=_split_verdict(str(entry["verdict"])), gold_source=gold_source,
        evidence_provenance_class=provenance, verdict_convention="gold_robot_inspection.json",
        reason=entry.get("reason"),
        required_minimal_procedure=list(rmp) if rmp else None, extra=extra,
    )


def _from_groundtruth(sid: str, manifest: Dict[str, Any]) -> ScenarioGold:
    d = scenario_dir(sid)
    text = (d / "groundtruth.txt").read_text(errors="replace")
    parsed = _parse_groundtruth(text)
    fm_code = parsed.get("fm_flag") or manifest.get("fm_code")
    gold_source, provenance = _classify(fm_code)
    rmp = manifest.get("required_minimal_procedure")
    return ScenarioGold(
        scenario_id=sid, fm_code=fm_code, asset_id=manifest.get("asset_id"),
        gold_action=_split_verdict(parsed["verdict"]), gold_source=gold_source,
        evidence_provenance_class=provenance, verdict_convention=parsed["convention"],
        required_minimal_procedure=list(rmp) if rmp else None,
    )


def _normalise_for_conflict_check(action: GoldAction) -> frozenset:
    """DISPATCH and COMMIT are the same action post-normalisation
    (l3_scoring.normalise_action) -- comparing raw strings would report that
    equivalence as a false conflict."""
    vals = action if isinstance(action, tuple) else (action,)
    out = set()
    for v in vals:
        u = (v or "").upper()
        out.add("PROCEED" if u in ("DISPATCH", "COMMIT") else u)
    return frozenset(out)


def _check_groundtruth_conflict(sid: str, gold: ScenarioGold) -> Optional[Dict[str, Any]]:
    """Cross-check the chosen gold_action against groundtruth.txt's own
    verdict line, independent of which source built ``gold``. Never silently
    resolved -- either they agree (post DISPATCH/COMMIT normalisation) or the
    disagreement is recorded, verbatim, for the R1 report."""
    d = scenario_dir(sid)
    text = (d / "groundtruth.txt").read_text(errors="replace")
    try:
        parsed = _parse_groundtruth(text)
    except ValueError:
        return None  # nothing to cross-check against
    if gold.verdict_convention == parsed["convention"]:
        return None  # gold WAS built from this exact parse; trivially consistent
    gt_action = _split_verdict(parsed["verdict"])
    gt_norm = _normalise_for_conflict_check(gt_action)
    gold_norm = _normalise_for_conflict_check(gold.gold_action)
    if gt_norm == gold_norm:
        return None
    # Set-valued gold (e.g. R049: {SHUTDOWN, ESCALATE}) -- groundtruth.txt
    # naming one accepted member is agreement, not a conflict.
    if isinstance(gold.gold_action, tuple) and gt_norm <= gold_norm:
        return None
    return {
        "scenario_id": sid,
        "typed_gold_action": gold.gold_action if isinstance(gold.gold_action, str) else list(gold.gold_action),
        "typed_gold_source": gold.verdict_convention,
        "groundtruth_txt_verdict": parsed["verdict"],
        "groundtruth_txt_convention": parsed["convention"],
    }


def build_registry() -> Dict[str, ScenarioGold]:
    """Build the typed gold record for all 89 scenarios.

    Raises on any scenario that cannot be migrated without inventing gold
    (none, as of R1 — every dir resolves through one of the three sources).
    Pre-existing disagreements *between* sources are not adjudicated here —
    see ``build_registry_with_conflicts``.
    """
    registry, _ = build_registry_with_conflicts()
    return registry


def build_registry_with_conflicts() -> Tuple[Dict[str, "ScenarioGold"], List[Dict[str, Any]]]:
    registry: Dict[str, ScenarioGold] = {}
    conflicts: List[Dict[str, Any]] = []
    gold_json = _load_gold_json()
    unmigrated: List[str] = []
    for sid in _all_scenario_ids():
        d = scenario_dir(sid)
        manifest = json.loads((d / "manifest.json").read_text())
        try:
            if sid in l3_arms.SCENARIOS:
                rec = _from_l3_arms(sid, manifest)
            elif sid in gold_json:
                rec = _from_gold_json(sid, gold_json[sid], manifest)
            else:
                rec = _from_groundtruth(sid, manifest)
        except Exception as exc:  # noqa: BLE001 — collected, not swallowed
            unmigrated.append(f"{sid}: {exc}")
            continue
        conflict = _check_groundtruth_conflict(sid, rec)
        if conflict:
            rec.extra["gold_conflict_with_groundtruth_txt"] = True
            conflicts.append(conflict)
        if sid in _CONDITIONAL_GOLD_OVERRIDE:
            rec.conditional_gold = _CONDITIONAL_GOLD_OVERRIDE[sid]
        registry[sid] = rec
    if unmigrated:
        raise ValueError(
            "scenarios that cannot be migrated without inventing gold:\n  "
            + "\n  ".join(unmigrated)
        )
    return registry, conflicts


def validate_registry(registry: Dict[str, ScenarioGold]) -> None:
    expected = set(_all_scenario_ids())
    got = set(registry)
    missing = expected - got
    if missing:
        raise ValueError(f"missing scenarios: {sorted(missing)}")
    # PASS R3: 89 was the R1 count, not a permanent invariant -- R090/R091
    # (FM-29 acoustic) added two more. Validate against the actual scenario
    # directory count, not a number frozen at R1.
    assert len(registry) == len(expected), (
        f"expected {len(expected)} scenarios (one per scenario_R* dir), got {len(registry)}")


def render_groundtruth_header(gold: ScenarioGold) -> str:
    """The header block a scorer parses, rendered FROM the typed record.

    Round-trips: ``_parse_groundtruth(render_groundtruth_header(g))["verdict"]``
    reproduces ``g.gold_action`` (joined) exactly.
    """
    action = gold.gold_action
    verdict_text = " / ".join(action) if isinstance(action, tuple) else action
    lines = [f"Expected verdict: {verdict_text}"]
    if gold.fm_code:
        lines.append(f"FM flag: {gold.fm_code}")
    return "\n".join(lines) + "\n"


def gold_action_for(scenario_id: str, registry: Optional[Dict[str, ScenarioGold]] = None) -> GoldAction:
    """Convenience accessor -- the single call sites should migrate to."""
    reg = registry if registry is not None else build_registry()
    return reg[scenario_id].gold_action


def save_registry(registry: Dict[str, ScenarioGold], path: Path = TYPED_REGISTRY_PATH) -> None:
    payload = {
        "contract_version": CONTRACT_VERSION,
        "scenarios": {sid: g.to_dict() for sid, g in sorted(registry.items())},
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def load_registry(path: Path = TYPED_REGISTRY_PATH) -> Dict[str, ScenarioGold]:
    payload = json.loads(path.read_text())
    return {sid: ScenarioGold.from_dict(d) for sid, d in payload["scenarios"].items()}


def coverage_report(registry: Dict[str, ScenarioGold]) -> Dict[str, Any]:
    """§GATE-style counts, reported per class -- never summed (R0-PRE rule 4)."""
    from collections import Counter
    gold_source_counts = Counter(g.gold_source for g in registry.values())
    provenance_counts = Counter(g.evidence_provenance_class for g in registry.values())
    convention_counts = Counter(g.verdict_convention for g in registry.values())
    return {
        "total_scenarios": len(registry),
        "gold_source_distribution": dict(gold_source_counts),
        "evidence_provenance_distribution": dict(provenance_counts),
        "verdict_convention_distribution": dict(convention_counts),
    }


CONFLICTS_REPORT_PATH = SCEN_ROOT / "Scenarios" / "gold_conflicts_report.json"


if __name__ == "__main__":
    reg, conflicts = build_registry_with_conflicts()
    validate_registry(reg)
    save_registry(reg)
    CONFLICTS_REPORT_PATH.write_text(json.dumps({"conflicts": conflicts}, indent=2) + "\n")
    print(f"wrote {TYPED_REGISTRY_PATH} ({len(reg)} scenarios)")
    print(f"wrote {CONFLICTS_REPORT_PATH} ({len(conflicts)} unresolved cross-source conflicts)")
    print(json.dumps(coverage_report(reg), indent=2))
