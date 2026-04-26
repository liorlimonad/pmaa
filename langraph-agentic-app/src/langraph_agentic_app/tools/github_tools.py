from __future__ import annotations

from dataclasses import dataclass

import requests

from ..config import Settings


@dataclass
class GitHubTools:
    """GitHub REST API wrapper with optional dry-run mutation mode."""

    settings: Settings

    def _url(self, path: str) -> str:
        return f"{self.settings.github_api_url.rstrip('/')}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, *, json: dict | None = None) -> dict:
        response = requests.request(
            method=method,
            url=self._url(path),
            headers=self.settings.github_headers,
            json=json,
            timeout=self.settings.github_timeout_seconds,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def _dry_run_result(self, action: str, repo: str, issue_id: str, payload: dict | None = None) -> dict:
        return {
            "dry_run": True,
            "action": action,
            "repo": repo,
            "issue_id": issue_id,
            "payload": payload or {},
        }

    def get_issue(self, repo: str, issue_id: str) -> dict:
        issue = self._request("GET", f"repos/{repo}/issues/{issue_id}")
        return {
            "id": str(issue.get("number", issue_id)),
            "repo": repo,
            "title": issue.get("title", ""),
            "body": issue.get("body") or "",
            "labels": [label["name"] for label in issue.get("labels", []) if "name" in label],
            "state": issue.get("state", "open"),
            "assignees": [assignee["login"] for assignee in issue.get("assignees", []) if "login" in assignee],
            "reviewers": [],
            "html_url": issue.get("html_url"),
        }

    def list_related_objects(self, repo: str, issue_id: str) -> dict:
        timeline = self._request("GET", f"repos/{repo}/issues/{issue_id}/timeline")
        events = timeline if isinstance(timeline, list) else []
        pull_requests = []
        commits = []
        participants = set()
        reviewers = set()

        for event in events:
            actor = event.get("actor") or {}
            if actor.get("login"):
                participants.add(actor["login"])
            source = event.get("source") or {}
            issue = source.get("issue") or {}
            if issue.get("pull_request"):
                pull_requests.append(issue.get("number"))
            if event.get("event") == "review_requested":
                requested_reviewer = event.get("requested_reviewer") or {}
                if requested_reviewer.get("login"):
                    reviewers.add(requested_reviewer["login"])
            commit_id = event.get("commit_id")
            if commit_id:
                commits.append(commit_id)

        return {
            "commits": commits,
            "pull_requests": pull_requests,
            "tasks": [],
            "reviewers": sorted(reviewers),
            "participants": sorted(participants),
        }

    def add_comment(self, repo: str, issue_id: str, body: str) -> dict:
        if self.settings.dry_run:
            return self._dry_run_result("comment", repo, issue_id, {"body": body})
        return self._request(
            "POST",
            f"repos/{repo}/issues/{issue_id}/comments",
            json={"body": body},
        )

    def update_labels(self, repo: str, issue_id: str, labels: list[str]) -> dict:
        if self.settings.dry_run:
            return self._dry_run_result("labels", repo, issue_id, {"labels": labels})
        return self._request(
            "PATCH",
            f"repos/{repo}/issues/{issue_id}",
            json={"labels": labels},
        )

    def request_reviewers(self, repo: str, issue_id: str, reviewers: list[str]) -> dict:
        if self.settings.dry_run:
            return self._dry_run_result("request_reviewers", repo, issue_id, {"reviewers": reviewers})
        related = self.list_related_objects(repo, issue_id)
        if not related["pull_requests"]:
            return {
                "warning": "No related pull request found for issue",
                "repo": repo,
                "issue_id": issue_id,
                "reviewers": reviewers,
            }
        pr_number = related["pull_requests"][0]
        return self._request(
            "POST",
            f"repos/{repo}/pulls/{pr_number}/requested_reviewers",
            json={"reviewers": reviewers},
        )

    def close_issue(self, repo: str, issue_id: str) -> dict:
        if self.settings.dry_run:
            return self._dry_run_result("close_issue", repo, issue_id)
        return self._request(
            "PATCH",
            f"repos/{repo}/issues/{issue_id}",
            json={"state": "closed"},
        )
