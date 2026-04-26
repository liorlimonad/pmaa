# GitHub Setup and Usage Guide

This guide explains how to connect the LangGraph agentic app to a real GitHub repository and run it against a real issue.

## 1. What the app currently does

The current app:
- connects to the GitHub REST API
- loads one issue from a real repository
- loads related objects from the issue timeline
- runs the LangGraph workflow on that issue
- may propose and execute issue-level actions such as:
  - applying labels
  - requesting reviewers
  - closing an issue

Important:
- by default, mutations should be run in **dry-run mode**
- this means the app computes actions but does not apply live write operations to GitHub

## 2. Prerequisites

You need:
- Python 3.10+
- access to the target GitHub repository
- a GitHub personal access token
- the repository owner/name
- an issue number in that repository

## 3. Create a GitHub token

Create a GitHub personal access token from GitHub settings.

Recommended minimum permissions depend on whether the repo is public or private and whether you want read-only or write behavior.

### For read-only testing
You need enough permission to:
- read issues
- read issue timeline / metadata
- read pull request context if relevant

### For live write testing
You need enough permission to:
- read issues
- write issue comments
- edit issue labels
- request reviewers on related pull requests
- close issues

For fine-grained tokens, grant access only to the specific repository you want to test.

## 4. Choose a real repository and issue

Identify:
- repository slug: `owner/repo`
- issue number: for example `123`

Example:
- repo: `my-org/my-repo`
- issue id: `42`

## 5. Install the app

From the workspace root:

```bash
cd langraph-agentic-app
/Users/liorlimonad/miniforge3/bin/python -m pip install -e .
```

## 6. Configure environment variables

Set these variables before running.

### Required

```bash
export GITHUB_REPO=owner/repo
export GITHUB_ISSUE_ID=123
```

### Recommended

```bash
export GITHUB_TOKEN=your_github_token
export GITHUB_DRY_RUN=true
```

### Optional

```bash
export GITHUB_API_URL=https://api.github.com
export GITHUB_TIMEOUT_SECONDS=20
```

## 7. Safe first run

Always start with dry-run enabled:

```bash
export GITHUB_DRY_RUN=true
```

Then run:

```bash
cd langraph-agentic-app
/Users/liorlimonad/miniforge3/bin/python -m langraph_agentic_app.app
```

## 8. What to expect on a dry run

On a dry run, the app should:
- load the real issue from GitHub
- classify the issue
- choose a role path in the graph
- generate proposed actions
- mark write actions as dry-run actions instead of applying them live

This lets you validate:
- the repo connection works
- the token works
- the issue is accessible
- the graph chooses sensible actions

## 9. Switch to live write mode

Only after dry-run behavior looks correct:

```bash
export GITHUB_DRY_RUN=false
```

Then rerun:

```bash
cd langraph-agentic-app
/Users/liorlimonad/miniforge3/bin/python -m langraph_agentic_app.app
```

In live mode, supported issue-level mutations may actually be sent to GitHub.

## 10. Suggested first test issue

Choose an issue that is safe to experiment on.

Recommended characteristics:
- a non-critical issue
- not security-sensitive
- in a test/sandbox repository if possible
- open issue with simple metadata
- preferably one where adding labels or requesting review is harmless

Best option:
- create a dedicated sandbox repository for experimentation

## 11. Example full setup

```bash
cd /Users/liorlimonad/Documents/pmaa/langraph-agentic-app

export GITHUB_TOKEN=ghp_your_token_here
export GITHUB_REPO=my-org/my-repo
export GITHUB_ISSUE_ID=42
export GITHUB_DRY_RUN=true

/Users/liorlimonad/miniforge3/bin/python -m pip install -e .
/Users/liorlimonad/miniforge3/bin/python -m langraph_agentic_app.app
```

## 12. Common failure cases

### Missing configuration
Symptom:
- app exits and asks for `GITHUB_REPO` and `GITHUB_ISSUE_ID`

Fix:
- set both environment variables before running

### 401 Unauthorized
Symptom:
- GitHub API rejects the request

Fix:
- verify `GITHUB_TOKEN`
- verify token scopes/permissions
- verify token is not expired

### 404 Not Found
Symptom:
- GitHub API cannot find the repo or issue

Fix:
- verify `GITHUB_REPO` is exactly `owner/repo`
- verify `GITHUB_ISSUE_ID` exists in that repo
- verify token can access the repo if it is private

### No related PR found for reviewer request
Symptom:
- reviewer request step returns a warning

Cause:
- current implementation finds related PRs heuristically from the issue timeline

Fix:
- use an issue linked to a PR
- or extend the integration logic to discover related PRs more robustly

## 13. Current limitations

The current app is still an initial integration scaffold.

Limitations:
- one issue per run
- no webhook server yet
- no persistent database yet
- no real vector memory yet
- no LLM-backed planning yet
- related PR detection is heuristic
- task linkage is not yet backed by a real task store

## 14. Recommended operating practice

For now:
1. always test with `GITHUB_DRY_RUN=true`
2. use a sandbox repository first
3. inspect output before allowing live writes
4. only enable live mode on low-risk issues
5. keep token scope minimal

## 15. Next recommended upgrade path

After basic GitHub connectivity works, the next improvements should be:
1. add CLI arguments for repo/issue id
2. add webhook ingestion
3. add `.env` loading support
4. add richer GitHub PR/commit discovery
5. add approval checkpoints before live mutations
6. add LLM-backed reasoning for routing and planning

## 16. Quick command summary

Install:

```bash
cd langraph-agentic-app
/Users/liorlimonad/miniforge3/bin/python -m pip install -e .
```

Dry run:

```bash
export GITHUB_TOKEN=your_token
export GITHUB_REPO=owner/repo
export GITHUB_ISSUE_ID=123
export GITHUB_DRY_RUN=true

/Users/liorlimonad/miniforge3/bin/python -m langraph_agentic_app.app
```

Live mode:

```bash
export GITHUB_DRY_RUN=false
/Users/liorlimonad/miniforge3/bin/python -m langraph_agentic_app.app