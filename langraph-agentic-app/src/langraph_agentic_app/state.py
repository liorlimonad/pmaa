from __future__ import annotations

from typing import Any, Literal, TypedDict


Stage = Literal[
    "new",
    "needs_triage",
    "needs_clarification",
    "ready_for_planning",
    "ready_for_implementation",
    "in_progress",
    "needs_review",
    "needs_qa",
    "needs_docs",
    "ready_to_close",
    "closed",
    "reopened",
    "blocked",
]


class EvidenceItem(TypedDict):
    source: str
    kind: str
    content: str
    score: float


class ActionItem(TypedDict):
    actor: str
    action_type: str
    target: str
    payload: dict[str, Any]
    rationale: str
    status: str


class IssueOpsState(TypedDict):
    issue_id: str
    repo: str
    trigger_event: dict[str, Any]
    issue_snapshot: dict[str, Any]
    related_objects: dict[str, Any]
    conversation_summary: str
    role_hypotheses: list[str]
    current_stage: Stage
    proposed_actions: list[ActionItem]
    executed_actions: list[ActionItem]
    pending_human_actions: list[ActionItem]
    policy_flags: list[str]
    declare_flags: list[str]
    risk_score: float
    confidence: float
    evidence: list[EvidenceItem]
    process_trace: list[dict[str, Any]]
    memory_refs: list[str]
    final_decision: str | None


def initialize_state(
    issue_id: str,
    repo: str,
    trigger_event: dict[str, Any],
) -> IssueOpsState:
    return {
        "issue_id": issue_id,
        "repo": repo,
        "trigger_event": trigger_event,
        "issue_snapshot": {},
        "related_objects": {},
        "conversation_summary": "",
        "role_hypotheses": [],
        "current_stage": "new",
        "proposed_actions": [],
        "executed_actions": [],
        "pending_human_actions": [],
        "policy_flags": [],
        "declare_flags": [],
        "risk_score": 0.0,
        "confidence": 0.0,
        "evidence": [],
        "process_trace": [],
        "memory_refs": [],
        "final_decision": None,
    }

# Made with Bob
