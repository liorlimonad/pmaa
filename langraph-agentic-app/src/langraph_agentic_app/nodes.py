from __future__ import annotations

from typing import Literal

from .config import load_settings
from .prompts import ROLE_PROMPTS
from .state import ActionItem, IssueOpsState
from .tools import GitHubTools, MemoryTools, PolicyTools

settings = load_settings()
github_tools = GitHubTools(settings=settings)
memory_tools = MemoryTools()
policy_tools = PolicyTools()


def _append_trace(state: IssueOpsState, node: str, detail: str) -> None:
    state.setdefault("process_trace", []).append({"node": node, "detail": detail})


def ingest_event(state: IssueOpsState) -> IssueOpsState:
    state["current_stage"] = "needs_triage"
    _append_trace(state, "ingest_event", "Received issue event and initialized triage stage.")
    return state


def load_issue_context(state: IssueOpsState) -> IssueOpsState:
    repo = state["repo"]
    issue_id = state["issue_id"]
    state["issue_snapshot"] = github_tools.get_issue(repo, issue_id)
    state["related_objects"] = github_tools.list_related_objects(repo, issue_id)
    _append_trace(state, "load_issue_context", "Loaded issue snapshot and related objects.")
    return state


def classify_intent_and_state(state: IssueOpsState) -> IssueOpsState:
    issue = state["issue_snapshot"]
    body = issue.get("body", "")
    title = issue.get("title", "")
    similar = memory_tools.retrieve_similar_issues(state["repo"], f"{title}\n{body}")
    state.setdefault("evidence", []).append(
        {
            "source": "memory",
            "kind": "similar_issues",
            "content": str(similar),
            "score": similar[0]["score"] if similar else 0.0,
        }
    )

    labels = set(issue.get("labels", []))
    role_hypotheses: list[str] = ["issue_reporter", "bot"]

    lower_text = f"{title} {body}".lower()
    if any(token in lower_text for token in ["docs", "documentation", "readme"]):
        role_hypotheses.append("technical_writer")
    if any(token in lower_text for token in ["test", "quality", "regression"]):
        role_hypotheses.append("quality")
    if any(token in lower_text for token in ["deploy", "ci", "workflow", "infra"]):
        role_hypotheses.append("devops")
    if any(token in lower_text for token in ["feature", "enhancement"]):
        role_hypotheses.append("implementation")
    if "bug" in labels:
        role_hypotheses.append("implementation")

    state["role_hypotheses"] = role_hypotheses
    state["conversation_summary"] = f"{title}: {body[:240]}".strip()
    state["confidence"] = 0.72
    _append_trace(state, "classify_intent_and_state", f"Role hypotheses={role_hypotheses}")
    return state


def policy_guard(state: IssueOpsState) -> IssueOpsState:
    risk = policy_tools.score_risk(state["issue_snapshot"], state["related_objects"])
    declare_flags = policy_tools.check_declare_guards(state["issue_snapshot"])
    state["risk_score"] = risk
    state["declare_flags"] = declare_flags

    policy_flags = state.setdefault("policy_flags", [])
    if risk >= 0.7:
        policy_flags.append("high_risk")
    if declare_flags:
        policy_flags.extend(declare_flags)

    _append_trace(
        state,
        "policy_guard",
        f"risk_score={risk}, declare_flags={declare_flags}",
    )
    return state


def route_to_role_agent(state: IssueOpsState) -> IssueOpsState:
    roles = state.get("role_hypotheses", [])
    selected = "issue_reporter"
    for candidate in [
        "technical_writer",
        "quality",
        "devops",
        "implementation",
        "bot",
        "issue_reporter",
    ]:
        if candidate in roles:
            selected = candidate
            break

    state["final_decision"] = selected
    _append_trace(state, "route_to_role_agent", f"Selected role agent={selected}")
    return state


def issue_reporter_agent(state: IssueOpsState) -> IssueOpsState:
    state.setdefault("proposed_actions", []).extend(
        [
            ActionItem(
                actor="issue_reporter",
                action_type="summarize_issue",
                target=state["issue_id"],
                payload={},
                rationale=ROLE_PROMPTS["issue_reporter"],
                status="proposed",
            ),
            ActionItem(
                actor="issue_reporter",
                action_type="ask_for_clarification",
                target=state["issue_id"],
                payload={"questions": ["Please provide expected behavior and actual behavior."]},
                rationale="Issue intake is communication-heavy and clarification-first.",
                status="proposed",
            ),
        ]
    )
    state["current_stage"] = "needs_clarification"
    _append_trace(state, "issue_reporter_agent", "Prepared clarification and intake actions.")
    return state


def bot_workflow_agent(state: IssueOpsState) -> IssueOpsState:
    state.setdefault("proposed_actions", []).extend(
        [
            ActionItem(
                actor="bot",
                action_type="apply_labels",
                target=state["issue_id"],
                payload={"labels": ["triage", "needs-review"]},
                rationale=ROLE_PROMPTS["bot"],
                status="proposed",
            ),
            ActionItem(
                actor="bot",
                action_type="request_reviewers",
                target=state["issue_id"],
                payload={"reviewers": ["maintainer-team"]},
                rationale="Bot role is centered on workflow routing and review orchestration.",
                status="proposed",
            ),
        ]
    )
    state["current_stage"] = "needs_review"
    _append_trace(state, "bot_workflow_agent", "Prepared low-risk workflow automation actions.")
    return state


def implementation_agent(state: IssueOpsState) -> IssueOpsState:
    state.setdefault("proposed_actions", []).extend(
        [
            ActionItem(
                actor="implementation",
                action_type="create_task_plan",
                target=state["issue_id"],
                payload={
                    "steps": [
                        "Inspect relevant code paths",
                        "Implement minimal change",
                        "Link changes to issue and task",
                        "Prepare PR for review",
                    ]
                },
                rationale=ROLE_PROMPTS["implementation"],
                status="proposed",
            )
        ]
    )
    state["current_stage"] = "ready_for_implementation"
    _append_trace(state, "implementation_agent", "Prepared implementation plan.")
    return state


def quality_agent(state: IssueOpsState) -> IssueOpsState:
    state.setdefault("proposed_actions", []).append(
        ActionItem(
            actor="quality",
            action_type="define_validation_plan",
            target=state["issue_id"],
            payload={"checks": ["unit tests", "regression checks", "acceptance criteria review"]},
            rationale=ROLE_PROMPTS["quality"],
            status="proposed",
        )
    )
    state["current_stage"] = "needs_qa"
    _append_trace(state, "quality_agent", "Prepared quality validation plan.")
    return state


def technical_writer_agent(state: IssueOpsState) -> IssueOpsState:
    state.setdefault("proposed_actions", []).append(
        ActionItem(
            actor="technical_writer",
            action_type="prepare_docs_update",
            target=state["issue_id"],
            payload={"artifacts": ["README", "release notes", "usage guide"]},
            rationale=ROLE_PROMPTS["technical_writer"],
            status="proposed",
        )
    )
    state["current_stage"] = "needs_docs"
    _append_trace(state, "technical_writer_agent", "Prepared documentation work items.")
    return state


def human_approval_gate(state: IssueOpsState) -> IssueOpsState:
    if state.get("risk_score", 0.0) >= 0.7:
        pending = state.setdefault("pending_human_actions", [])
        pending.extend(state.get("proposed_actions", []))
        _append_trace(state, "human_approval_gate", "High risk detected; human approval required.")
    else:
        _append_trace(state, "human_approval_gate", "Risk acceptable; no approval required.")
    return state


def execute_actions(state: IssueOpsState) -> IssueOpsState:
    if state.get("pending_human_actions"):
        _append_trace(state, "execute_actions", "Execution deferred pending human approval.")
        return state

    executed = state.setdefault("executed_actions", [])
    for action in state.get("proposed_actions", []):
        action["status"] = "executed"
        executed.append(action)

        if action["action_type"] == "apply_labels":
            github_tools.update_labels(
                state["repo"],
                state["issue_id"],
                action["payload"].get("labels", []),
            )
        elif action["action_type"] == "request_reviewers":
            github_tools.request_reviewers(
                state["repo"],
                state["issue_id"],
                action["payload"].get("reviewers", []),
            )

    _append_trace(state, "execute_actions", f"Executed {len(executed)} actions.")
    return state


def update_memory_and_metrics(state: IssueOpsState) -> IssueOpsState:
    state.setdefault("memory_refs", []).append(f"issue:{state['issue_id']}")
    _append_trace(state, "update_memory_and_metrics", "Updated issue memory references.")
    return state


def close_or_wait(state: IssueOpsState) -> IssueOpsState:
    if state.get("current_stage") == "ready_to_close" and not state.get("pending_human_actions"):
        github_tools.close_issue(state["repo"], state["issue_id"])
        state["current_stage"] = "closed"
        state["final_decision"] = "closed"
        _append_trace(state, "close_or_wait", "Issue closed.")
    else:
        _append_trace(state, "close_or_wait", f"Waiting in stage={state.get('current_stage')}")
    return state


def role_route(state: IssueOpsState) -> Literal[
    "issue_reporter",
    "bot",
    "implementation",
    "quality",
    "technical_writer",
]:
    selected = state.get("final_decision", "issue_reporter")
    if selected == "bot":
        return "bot"
    if selected == "implementation":
        return "implementation"
    if selected == "quality":
        return "quality"
    if selected == "technical_writer":
        return "technical_writer"
    return "issue_reporter"

# Made with Bob
