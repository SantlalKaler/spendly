---
description: Commit and push the current branch
argument-hint: "optional commit message"
allowed-tools: Bash(git:*)
---

You are committing and pushing up the current feature branch.
Follow these steps exactly and in order. Do not skip a step or
reorder them.

User input (optional commit message): $ARGUMENTS

## Step 1 — Check current branch
Run `git branch --show-current`.

If the current branch is `main`, stop immediately and tell the
user there is no feature branch to push — this command is for
pushing a feature branch, not committing directly to `main`.

Remember this branch name as `feature_branch` for later steps.

## Step 2 — Review changes
Run `git status` and `git diff` (staged and unstaged) to see what
will be committed.

If there are no changes to commit (nothing staged, unstaged, or
untracked) and the branch has nothing unpushed, stop and tell the
user there is nothing to push.

Check the untracked/modified files for anything that looks like a
secret or credential (`.env`, keys, tokens, etc). If found, warn
the user and stop — do not add or commit it.

## Step 3 — Stage changes
Run `git add` for the relevant files (avoid `git add -A`/`.` if it
would sweep in unrelated or sensitive files — add specific paths
when in doubt).

## Step 4 — Commit
If the user supplied a commit message in $ARGUMENTS, use it.
Otherwise, write a concise commit message (1-2 sentences) that
describes the "why" of the change, based on the staged diff and
recent `git log` style in this repo.

Run:
```
git commit -m "<message>"
```

If there are no staged changes at this point (branch was already
committed, just needs pushing), skip this step.

## Step 5 — Push
Run:
```
git push -u origin <feature_branch>
```

If the push fails, stop and report the error to the user.

## Step 6 — Report to the user
Print a short summary in this exact format:
```
Pushed:  <feature_branch> -> origin/<feature_branch>
Commit:  <commit message used, or "no new commit">
```

Then tell the user: once the PR is merged, run `/git-checkout-main`
to switch back to `main`, pull latest, and delete this branch.
