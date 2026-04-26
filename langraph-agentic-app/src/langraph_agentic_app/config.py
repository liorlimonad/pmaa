from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    github_token: str | None
    github_api_url: str
    github_default_repo: str | None
    github_default_issue_id: str | None
    github_timeout_seconds: float
    dry_run: bool

    @property
    def github_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
        return headers


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _normalize_github_repo(value: str | None) -> str | None:
    if not value:
        return None

    repo = value.strip()

    prefixes = [
        "https://github.com/",
        "http://github.com/",
        "git@github.com:",
    ]
    for prefix in prefixes:
        if repo.startswith(prefix):
            repo = repo[len(prefix):]
            break

    if repo.endswith(".git"):
        repo = repo[:-4]

    repo = repo.strip("/")

    if repo.count("/") >= 2:
        parts = repo.split("/")
        repo = "/".join(parts[-2:])

    return repo or None


def load_settings() -> Settings:
    return Settings(
        github_token=os.getenv("GITHUB_TOKEN"),
        github_api_url=os.getenv("GITHUB_API_URL", "https://api.github.com"),
        github_default_repo=_normalize_github_repo(os.getenv("GITHUB_REPO")),
        github_default_issue_id=os.getenv("GITHUB_ISSUE_ID"),
        github_timeout_seconds=float(os.getenv("GITHUB_TIMEOUT_SECONDS", "20")),
        dry_run=_parse_bool(os.getenv("GITHUB_DRY_RUN"), default=True),
    )

# Made with Bob
