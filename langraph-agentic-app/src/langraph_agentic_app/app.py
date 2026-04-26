from __future__ import annotations

from pprint import pprint

from .config import load_settings
from .state import initialize_state


def main() -> None:
    try:
        from .graph import build_graph
    except Exception as exc:  # pragma: no cover - scaffold fallback
        print("Unable to import LangGraph runtime. Install project dependencies first.")
        print(f"Import error: {exc}")
        return

    settings = load_settings()
    if not settings.github_default_repo or not settings.github_default_issue_id:
        print("Missing required configuration for live GitHub execution.")
        print("Please set:")
        print("  GITHUB_REPO=owner/repo")
        print("  GITHUB_ISSUE_ID=123")
        print("Optional:")
        print("  GITHUB_TOKEN=...")
        print("  GITHUB_DRY_RUN=true|false")
        return

    issue_id = settings.github_default_issue_id
    repo = settings.github_default_repo

    app = build_graph()
    state = initialize_state(
        issue_id=issue_id,
        repo=repo,
        trigger_event={"type": "issues.opened"},
    )
    result = app.invoke(state)
    pprint(result)


if __name__ == "__main__":
    main()

# Made with Bob
