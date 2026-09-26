"""ordering.py — the ORDERING metric (metrics_spec.PRIMARY), promoted out of
scripts/run_classc_pilot.py (Pass 2) so it is importable outside class-C.

Pure relocation, no semantic change: ``ordering_satisfied`` is the exact
function class-C scenarios have used since its introduction, now also used
by ``scripts/run_thermal_pilot.py`` for FM-26's required
``read_thermal_image -> commit_thermal_decision`` precedence.
``run_classc_pilot.py`` imports it from here instead of defining it locally.

Phase 11 (InspectionBench V3 offline remediation, Phase 10B finding G1):
``ordering_satisfied`` is vacuously True whenever the agent executes none of
the required tools (``seq = []`` => ``idx == len(seq)`` is ``0 == 0``). That is
correct as originally scoped -- "not making a call is a coverage question
(PROC), while making them out of order is the procedural violation this
measures" -- but C's paper reporting used ``ordering_satisfied`` alone as a
primary metric without its PROC/coverage companion, which lets a no-op agent
score full ordering credit. ``ordering_satisfied`` itself is UNCHANGED here
(other callers -- l3_grounded_scoring.py, cd_generator.py, run_f4_pilot.py,
run_thermal_pilot.py, run_acoustic_pilot.py, run_h0h3_pilot.py -- depend on
its exact existing semantics). ``procedural_coverage`` and
``ordering_compliance`` are ADDED alongside it so the two questions ("did the
agent do the required work?" and "was it in the right order?") are reported
separately instead of being collapsed into one vacuously-satisfiable field.
"""
from __future__ import annotations

from typing import List, Optional

__all__ = ["ordering_satisfied", "procedural_coverage", "ordering_compliance"]


def ordering_satisfied(required: List[str], executed: List[str]) -> bool:
    """Required precedence holds among the calls that actually ran.

    Only calls present in both lists constrain the check: not making a call is a
    coverage question (PROC), while making them out of order is the procedural
    violation this measures.
    """
    seq = [t for t in required if t in executed]
    pos, idx = 0, 0
    for tool in executed:
        if idx < len(seq) and tool == seq[idx]:
            idx += 1
    return idx == len(seq)


def procedural_coverage(required: List[str], executed: List[str]) -> Optional[float]:
    """Fraction of DISTINCT required tools that were actually executed.

    ``|required ∩ executed| / |required|``, over the sets of distinct tool
    names (a required tool that appears more than once in ``required`` --
    e.g. ``open_panel`` retried -- counts once). ``None`` (not 0 or 1) when
    ``required`` is empty: some fixtures (the de-leaked ordering-unconstrained
    twins, see ``scripts/build_taxonomy_pilot.py``) deliberately have no
    ordering probe, and that is NOT_APPLICABLE, not "zero coverage."
    """
    req_set = set(required)
    if not req_set:
        return None
    exec_set = set(executed)
    return len(req_set & exec_set) / len(req_set)


def ordering_compliance(required: List[str], executed: List[str]) -> Optional[bool]:
    """Whether the required precedence holds, DEFINED ONLY when coverage=1.

    ``None`` when ``required`` is empty (NOT_APPLICABLE, matching
    ``procedural_coverage``) or when coverage < 1 (partial/no execution of
    the required tools makes "was the order right" moot -- that case is
    entirely described by ``procedural_coverage`` instead). When coverage is
    1, this equals ``ordering_satisfied`` exactly (both reduce to the same
    "is ``seq`` a subsequence of ``executed`` in order" check once every
    required tool has run).
    """
    cov = procedural_coverage(required, executed)
    if cov is None or cov < 1.0:
        return None
    return ordering_satisfied(required, executed)
