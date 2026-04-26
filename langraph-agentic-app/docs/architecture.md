# Architecture

## Overview

This LangGraph application is a scaffold for an agentic GitHub issue-operations system grounded in mined process artifacts from this workspace.

The mined roles suggest two main operational classes:

- coordination-heavy roles
  - `issue_reporter`
  - `bot`

- execution-heavy roles
  - `contributor`
  - `feature_developer`
  - `maintainer`
  - `devops_engineer`
  - `quality_engineer`
  - `technical_writer`

The graph therefore uses:
- a shared issue-centric state
- a supervisor-style routing layer
- specialist role nodes
- policy and human approval checkpoints

## Object-centric modeling choice

The app treats the issue as the primary orchestration object and stores linked objects explicitly:
- issue
- task
- commit
- pull request
- labels
- reviewers
- users

This mirrors the mined OCEL structure more faithfully than a chat-history-only design.

## Node sequence

Top-level sequence:

1. `ingest_event`
2. `load_issue_context`
3. `classify_intent_and_state`
4. `policy_guard`
5. `route_to_role_agent`
6. one specialist role node
7. `human_approval_gate`
8. `execute_actions`
9. `update_memory_and_metrics`
10. `close_or_wait`

## Role-node intent

### `issue_reporter_agent`
Focused on:
- clarification
- communication
- duplicate awareness
- issue preparation

### `bot_workflow_agent`
Focused on:
- labels
- comments
- review requests
- safe workflow automation

### `implementation_agent`
Shared execution core for:
- contributor
- feature developer
- maintainer
- devops
- quality-oriented implementation
- docs-oriented implementation when needed

### `quality_agent`
Focused on:
- tests
- validation plans
- regression awareness
- acceptance criteria

### `technical_writer_agent`
Focused on:
- docs updates
- release communication
- explanation quality

## Policy grounding

This scaffold includes placeholders for:
- risk scoring
- DECLARE guard checks
- BPMN next-step expectations

Intended use:
- DECLARE as lightweight invariant checking
- BPMN/flow artifacts as next-step priors
- markdown role descriptions as role prompts and behavioral contracts

## Human-in-the-loop

High-risk actions should be held in `pending_human_actions`.
Typical examples:
- issue closure in sensitive contexts
- merge/deploy actions
- repository-wide changes
- irreversible governance actions

## Extension points

To productionize this scaffold:
- replace stub GitHub tools with real API clients
- add LLM-backed reasoning inside role nodes
- persist memory in a database or vector store
- ingest mined artifacts into a retrieval/policy layer
- add auth, audit logs, and approval UX