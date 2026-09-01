---
description: Switch to main, pull latest, and force-delete the branch you just merged
allowed-tools: Bash(git:*)
---

You are cleaning up after a branch has already been merged into
`main` (e.g. via a merged PR on GitHub). Follow these steps
exactly and in order. Do not skip a step or reorder them.

## Step 1 — Check current branch
Run `git branch --show-current`.

If the current branch is `main`, stop immediately and tell the
user there is no branch to clean up — this command is meant to be
run from the feature branch that was just merged.

Remember this branch name as `merged_branch` for later steps.

## Step 2 — Check working directory is clean
Run `git status` and check for uncommitted, unstaged, or untracked
files. If any exist, stop immediately and tell the user to commit
or stash changes before proceeding. DO NOT CONTINUE until the
working directory is clean.

## Step 3 — Switch to main and pull latest
Run:
```
git checkout main
git pull origin main
```

## Step 4 — Force-delete the merged branch
The user has confirmed `merged_branch` was already merged into
`main`, so force delete it locally:
```
git branch -D <merged_branch>
```

If the delete fails, report the error to the user.

## Step 5 — Report to the user
Print a short summary in this exact format:
```
Branch:  now on main (pulled latest)
Deleted: <merged_branch>
```
