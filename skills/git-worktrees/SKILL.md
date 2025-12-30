---
name: git-worktrees
description: Git worktrees for isolated parallel development on multiple branches simultaneously.
---

# Git Worktrees

> Source: travisvn/awesome-claude-skills

## Overview
Git worktrees allow working on multiple branches simultaneously without switching.

## Basic Commands

```bash
# Create worktree for existing branch
git worktree add ../feature-x feature-x

# Create worktree with new branch
git worktree add -b feature-y ../feature-y

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../feature-x

# Prune stale worktrees
git worktree prune
```

## Directory Structure

```
project/              # Main worktree (main branch)
project-feature-x/    # Worktree for feature-x branch
project-hotfix/       # Worktree for hotfix branch
```

## Use Cases

### 1. Parallel Feature Development
```bash
# Work on feature while keeping main clean
git worktree add ../project-feature features/new-feature
cd ../project-feature
# Work here without affecting main
```

### 2. Quick Hotfix
```bash
# Urgent fix without stashing current work
git worktree add ../project-hotfix hotfix/critical-bug
cd ../project-hotfix
# Fix, commit, push
```

### 3. Code Review
```bash
# Check PR without affecting your work
git worktree add ../project-review pr-branch
cd ../project-review
# Review, test, then remove
```

## Best Practices

1. **Naming convention**: `../project-feature-name` (keep outside main repo)
2. **Shared Build Cache**: Use shared caches (e.g., Turborepo/Nx) outside worktrees to prevent redundant builds.
3. **Dependency Management**: Use pnpm/Yarn Berry with content-addressable storage to save disk space.
4. **Cleanup**: Always `git worktree remove` to prevent stale references.

## Workflow Example

```bash
# You're on main, need to check a bug
git worktree add -b investigate ../project-investigate

# Go there
cd ../project-investigate

# Investigate, fix if small
# ...

# Done, clean up
cd ../project
git worktree remove ../project-investigate
```

## AI-Automated Workflow (2025)
Agents can use worktrees to safely test multiple implementations:
1. `git worktree add ../temp-poc poc-branch`
2. Run automated tests in `temp-poc`.
3. If tests pass, merge and `git worktree remove ../temp-poc`.

## Gotchas

- Can't check out same branch in two worktrees
- Each worktree has its own working directory
- node_modules not shared (run npm install in each)
