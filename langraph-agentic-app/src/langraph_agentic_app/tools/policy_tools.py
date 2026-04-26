from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PolicyTools:
    """Stub policy layer grounded in mined process expectations."""

    def score_risk(self, issue_snapshot: dict[str, Any], related_objects: dict[str, Any]) -> float:
        labels = set(issue_snapshot.get("labels", []))
        risk = 0.1
        if "security" in labels:
            risk += 0.6
        if "production" in labels:
            risk += 0.2
        if related_objects.get("pull_requests"):
            risk += 0.1
        return min(risk, 1.0)

    def check_declare_guards(self, issue_snapshot: dict[str, Any]) -> list[str]:
        flags: list[str] = []
        if issue_snapshot.get("state") == "closed" and issue_snapshot.get("closure_attempted_again"):
            flags.append("closed_more_than_once")
        return flags

    def check_bpmn_next_step(self, current_stage: str) -> list[str]:
        expected = {
            "new": ["needs_triage"],
            "needs_triage": ["needs_clarification", "ready_for_planning"],
            "ready_for_planning": ["ready_for_implementation"],
            "ready_to_close": ["closed"],
        }
        return expected.get(current_stage, [])

# Made with Bob
