# 07 — Persistent Project State

## 1. Why

The project must survive:
- agent restart;
- VM reboot;
- lost conversation context;
- partial failure.

## 2. State files

### `.ai/PROJECT_STATE.md`
Human-readable high-level status.

Contains:
- current phase;
- completed milestones;
- active work;
- known risks;
- next planned milestone.

### `.ai/TASKS.json`
Machine-readable task ledger.

Must remain valid JSON.

### `.ai/DECISIONS.md`
Human approvals and significant implementation decisions.

### `.ai/BLOCKERS.md`
Unresolved blockers.

### `.ai/TEST_STATUS.md`
Latest test-gate status by branch/release candidate.

### `.ai/DEPLOYMENT_STATUS.md`
Environment/release state.

### `.ai/RESOURCE_STATUS.md`
Disk/resource observations relevant to safe execution.

## 3. Task ledger integrity

Task IDs are immutable.

Completed tasks are not deleted; they remain as history.

Status transitions should include timestamp/history when practical.

## 4. Minimal task history format

```json
{
  "history": [
    {
      "at": "2026-09-29T13:00:00Z",
      "from": "in_progress",
      "to": "testing",
      "actor_role": "orchestrator"
    }
  ]
}
```

## 5. Recovery rule

On startup, Orchestrator must reconcile:
- Git branches/worktrees;
- `.ai/TASKS.json`;
- running/stale processes;
- latest test status.

If state conflicts, prefer Git and durable test/artifact evidence, then repair state files explicitly.
