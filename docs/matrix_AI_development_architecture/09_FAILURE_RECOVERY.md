# 09 — Failure and Recovery

## 1. Agent crash

If an agent stops mid-task:
- task remains `in_progress` until Orchestrator reconciliation;
- inspect branch diff and last commit;
- run relevant tests;
- either resume or reassign;
- do not discard work blindly.

## 2. VM restart

On restart:
1. load persistent state;
2. inspect Git/worktrees;
3. inspect running containers/processes;
4. verify database/service connectivity;
5. mark stale locks/tasks;
6. resume only safe tasks.

## 3. Failed tests

Tester records:
- failing command;
- concise failure summary;
- suspected component;
- whether failure is deterministic.

Orchestrator routes task back to implementation as `changes_requested`.

## 4. Failed review

Reviewer findings become explicit correction tasks or reopen the original task.

No merge until blockers/major findings close.

## 5. Integration regression

If combined branch breaks:
- Integrator identifies likely merge/interaction cause;
- do not blindly revert unrelated approved work;
- create integration-fix task;
- retest affected tasks.

## 6. Bad staging release

DevOps must have rollback procedure before production deployment.

Staging may be redeployed freely if no protected data is at risk.

## 7. Production incident

Automatic actions may include:
- stop further deployments;
- mark release unhealthy;
- rollback application version when rollback is known safe.

Human approval is required for destructive data restoration or uncertain migrations.

## 8. Corrupted state files

Use:
- Git history;
- branch state;
- CI/test artifacts;
- deployment records

to reconstruct `.ai` state.

State files are important but not more authoritative than actual repository/deployment evidence.
