# 04 — Git and Workspace Workflow

## 1. Branch model

Recommended:

```text
main
└── develop
    ├── agent/MATRIX-001-settings
    ├── agent/MATRIX-002-db
    └── agent/MATRIX-003-webhook
```

`main`:
- release/production baseline;
- protected.

`develop`:
- integrated, tested development baseline.

Task branches:
- one scoped task or tightly coupled task group.

## 2. Worktrees

Use Git worktrees when parallel tasks are needed.

Because disk is constrained:
- keep worktree count low;
- do not create a separate virtual environment per worktree;
- remove worktree after merge;
- avoid copying large generated directories.

## 3. Commit rules

Commits should:
- reference task ID;
- be reasonably atomic;
- exclude secrets;
- exclude large generated artifacts;
- avoid unrelated formatting churn.

Example:
```text
MATRIX-014: add webhook event idempotency constraint
```

## 4. Merge gate

A task branch can merge to `develop` only after:
- task tests pass;
- Tester records pass;
- Reviewer approves;
- migrations are validated;
- no unresolved blocker.

## 5. Integration conflicts

Integrator resolves ordinary conflicts.

If conflict reveals incompatible architectural assumptions:
- stop merge;
- create blocker;
- route to Orchestrator/Planner;
- ADR if required.

## 6. Main/release gate

`develop` may reach `main` only when:
- release candidate tests pass;
- staging smoke tests pass;
- required approval is recorded;
- deployment plan and rollback plan exist.

## 7. Repository hygiene

Do not commit:
- `.env`;
- local database files;
- `__pycache__`;
- coverage artifacts unless policy says so;
- large logs;
- card images;
- credentials;
- Docker layer exports;
- downloaded model weights.
