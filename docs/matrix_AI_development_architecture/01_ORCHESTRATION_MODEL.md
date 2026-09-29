# 01 — Orchestration Model

## 1. Orchestrator responsibility

The Orchestrator is the central coordinator.

It does not primarily exist to write application code.

It:
- loads project state;
- understands architecture;
- asks Planner for task decomposition;
- schedules dependency-ready tasks;
- chooses appropriate specialist role;
- tracks branches/worktrees;
- triggers tests and review;
- routes failures back to implementation;
- escalates only when policy requires;
- updates persistent state;
- prepares release candidates.

## 2. Work lifecycle

```text
Approved product architecture
        ↓
Planner creates task DAG
        ↓
Orchestrator validates DAG
        ↓
Ready tasks selected
        ↓
Specialist agent implements
        ↓
Tester verifies
        ↓
Reviewer reviews
        ↓
Integrator merges
        ↓
Integration tests
        ↓
Staging
        ↓
Release gate
        ↓
Production approval/deploy
```

## 3. Scheduling rules

A task may become `ready` only when:
- all dependencies are `done`;
- no blocking ADR is unresolved;
- required credentials/infrastructure exist;
- disk/resource guardrails permit execution.

Tasks with no file overlap may execute in parallel.

Tasks with likely overlap should execute serially unless Integrator approves a controlled parallel plan.

## 4. Orchestrator must prevent

- two agents editing the same migration lineage concurrently;
- simultaneous incompatible schema changes;
- parallel modification of the same critical module without coordination;
- deployment while release tests are red;
- architecture drift;
- runaway task spawning.

## 5. Concurrency baseline

Because the VM is constrained, default concurrency should be low.

Recommended baseline:
- 1–2 implementation tasks concurrently;
- 1 test/review task concurrently;
- no duplicate heavy Docker builds.

Concurrency can increase only if CPU, RAM, and disk measurements support it.

## 6. Task status model

Allowed task states:

```text
proposed
planned
ready
in_progress
testing
review
changes_requested
blocked
approved
integrating
done
cancelled
```

Only Orchestrator (or a delegated state manager) changes cross-role lifecycle state.

## 7. Completion rule

A feature is not complete merely because all code tasks are done.

Feature completion requires:
- all child tasks done;
- integration tests pass;
- architecture docs still match;
- no unresolved release blocker;
- release status persisted.
