from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from .nodes import (
    bot_workflow_agent,
    classify_intent_and_state,
    close_or_wait,
    execute_actions,
    human_approval_gate,
    implementation_agent,
    ingest_event,
    issue_reporter_agent,
    load_issue_context,
    policy_guard,
    quality_agent,
    role_route,
    route_to_role_agent,
    technical_writer_agent,
    update_memory_and_metrics,
)
from .state import IssueOpsState


def build_graph():
    graph = StateGraph(IssueOpsState)

    graph.add_node("ingest_event", ingest_event)
    graph.add_node("load_issue_context", load_issue_context)
    graph.add_node("classify_intent_and_state", classify_intent_and_state)
    graph.add_node("policy_guard", policy_guard)
    graph.add_node("route_to_role_agent", route_to_role_agent)
    graph.add_node("issue_reporter_agent", issue_reporter_agent)
    graph.add_node("bot_workflow_agent", bot_workflow_agent)
    graph.add_node("implementation_agent", implementation_agent)
    graph.add_node("quality_agent", quality_agent)
    graph.add_node("technical_writer_agent", technical_writer_agent)
    graph.add_node("human_approval_gate", human_approval_gate)
    graph.add_node("execute_actions", execute_actions)
    graph.add_node("update_memory_and_metrics", update_memory_and_metrics)
    graph.add_node("close_or_wait", close_or_wait)

    graph.add_edge(START, "ingest_event")
    graph.add_edge("ingest_event", "load_issue_context")
    graph.add_edge("load_issue_context", "classify_intent_and_state")
    graph.add_edge("classify_intent_and_state", "policy_guard")
    graph.add_edge("policy_guard", "route_to_role_agent")

    graph.add_conditional_edges(
        "route_to_role_agent",
        role_route,
        {
            "issue_reporter": "issue_reporter_agent",
            "bot": "bot_workflow_agent",
            "implementation": "implementation_agent",
            "quality": "quality_agent",
            "technical_writer": "technical_writer_agent",
        },
    )

    graph.add_edge("issue_reporter_agent", "human_approval_gate")
    graph.add_edge("bot_workflow_agent", "human_approval_gate")
    graph.add_edge("implementation_agent", "human_approval_gate")
    graph.add_edge("quality_agent", "human_approval_gate")
    graph.add_edge("technical_writer_agent", "human_approval_gate")
    graph.add_edge("human_approval_gate", "execute_actions")
    graph.add_edge("execute_actions", "update_memory_and_metrics")
    graph.add_edge("update_memory_and_metrics", "close_or_wait")
    graph.add_edge("close_or_wait", END)

    return graph.compile()

# Made with Bob
