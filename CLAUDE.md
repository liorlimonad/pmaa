# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Process Mining & Agentic Application (PMAA)** research workspace. It mines a GitHub repository's OCEL event log to discover process artifacts (BPMN models, DECLARE constraints, role behaviors), then uses those artifacts to ground a LangGraph multi-agent app that automates GitHub issue operations.

The pipeline flows: raw commits → OCEL enrichment → role annotation → per-role log splitting → process discovery (OCDFG, BPMN, DECLARE) → LangGraph app scaffolding.

## Repository layout

| Path | Purpose |
|---|---|
| `01–09_*.ipynb` | Sequential analysis notebooks (run in order) |
| `enrich_ocel_with_tasks.py` | Standalone script: `commitizen.json` → `commitizen_task_objects.json` |
| `commitizen*.json` | OCEL event logs (raw, role-annotated, task-enriched) |
| `role_logs/` | Per-role OCEL splits + OCDFG visualizations + prose descriptions |
| `bpmn_models/` | Discovered BPMN diagrams per role (`.bpmn` + `.png`) |
| `declare_models/` | Mined DECLARE constraint models per role (JSON) |
| `langraph-agentic-app/` | LangGraph scaffold — see below |

## Notebook pipeline summary

1. **01** — parse `commitizen.json`, produce the initial OCEL
2. **02** — analyse the OCEL with `pm4py` (DFG, footprint)
3. **03** — annotate resource–role mapping
4. **04** — split into per-role OCEL files under `role_logs/`
5. **05** — per-role process mining (OCDFG, DFG)
6. **06** — declarative process mining (DECLARE constraints)
7. **07** — generate prose process descriptions in `role_logs/*_process_description.md`
8. **08** — BPMN discovery and export to `bpmn_models/`
9. **09** — per-role DECLARE model discovery, write to `declare_models/`

## LangGraph agentic app

Located in `langraph-agentic-app/`. Python ≥ 3.10, uses `langgraph`, `langchain-core`, `pydantic`, `requests`.

### Install and run

```bash
cd langraph-agentic-app
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Required env vars before running:
export GITHUB_TOKEN=your_token
export GITHUB_REPO=owner/repo
export GITHUB_ISSUE_ID=123
export GITHUB_DRY_RUN=true   # default is true — set false only for live writes

python -m langraph_agentic_app.app
```

### Graph architecture

```
START → ingest_event → load_issue_context → classify_intent_and_state
      → policy_guard → route_to_role_agent
      → [conditional] → {issue_reporter | bot | implementation | quality | technical_writer}
      → human_approval_gate → execute_actions → update_memory_and_metrics → close_or_wait → END
```

**Key design rules:**
- `IssueOpsState` (TypedDict in `state.py`) is the single shared object passed through every node.
- `policy_guard` scores risk and checks DECLARE constraints; `risk_score >= 0.7` triggers the human approval gate.
- `role_route` (conditional edge function) reads `state["final_decision"]` to pick the agent branch.
- All GitHub mutations in `tools/github_tools.py` check `settings.dry_run` before executing; dry-run is the default.
- Role prompts are plain strings in `prompts.py` — derived from mined role behaviors, not from an LLM.

### Source modules

| Module | Responsibility |
|---|---|
| `state.py` | `IssueOpsState`, `Stage` literal, `initialize_state` |
| `config.py` | `Settings` dataclass, `load_settings()` reads env vars |
| `graph.py` | `build_graph()` wires all nodes and edges |
| `nodes.py` | All node functions and `role_route` |
| `prompts.py` | `ROLE_PROMPTS` dict keyed by role name |
| `tools/github_tools.py` | GitHub REST wrapper with dry-run support |
| `tools/memory_tools.py` | Similarity retrieval stubs |
| `tools/policy_tools.py` | Risk scoring and DECLARE guard checks |

## Environment

The root `.venv` is for the notebooks (pm4py, etc.). The `langraph-agentic-app/.venv` (or installed editable package) is for the LangGraph app. They are separate environments.

Root `.env` holds `OPENAI_API_KEY` for notebook LLM calls; GitHub env vars are set separately for the agentic app.
