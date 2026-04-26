from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class MemoryTools:
    """Stub retrieval layer for issue/process memory."""

    def retrieve_similar_issues(self, repo: str, issue_text: str) -> list[dict[str, Any]]:
        return [
            {
                "issue_id": "similar-1",
                "title": "Sample similar issue",
                "score": 0.71,
            }
        ]

    def retrieve_process_guidance(self, role: str) -> dict[str, Any]:
        return {
            "role": role,
            "guidance": f"Process guidance placeholder for role={role}",
        }

    def retrieve_repo_knowledge(self, repo: str, topic: str) -> list[dict[str, Any]]:
        return [
            {
                "repo": repo,
                "topic": topic,
                "content": "Repository knowledge placeholder",
                "score": 0.64,
            }
        ]

# Made with Bob
