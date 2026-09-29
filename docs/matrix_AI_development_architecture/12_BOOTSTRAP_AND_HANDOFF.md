# 12 — Bootstrap and Handoff Procedure

## Phase A — Install architecture into repository

Recommended structure:

```text
matrix/
├── architecture/
│   ├── product/
│   └── ai-development/
├── AGENTS.md
├── agents/
├── .ai/
└── application code...
```

The root `AGENTS.md` may either be this file copied from the package or a short pointer that declares this package authoritative.

## Phase B — First orchestrator boot

Orchestrator must:

1. verify Git repository exists;
2. locate product architecture;
3. load AI-development rules;
4. inspect `.ai` state;
5. inspect disk/resource status;
6. identify current branch;
7. ensure no uncommitted unknown work is overwritten;
8. ask Planner for the initial V1 task DAG;
9. validate DAG against product `11_IMPLEMENTATION_ORDER.md`;
10. write tasks into `.ai/TASKS.json`;
11. set first dependency-free tasks to `ready`.

## Phase C — First implementation milestone

Recommended first milestone:

```text
Repository foundation
+ settings
+ FastAPI health endpoint
+ test tooling
+ Docker baseline
+ CI skeleton
```

This proves the autonomous development loop before high-risk product work begins.

## Phase D — Validate agent architecture itself

Before allowing long unattended execution, test the development system with one small task:

1. Orchestrator assigns;
2. Coder implements;
3. Tester verifies;
4. Reviewer reviews;
5. Integrator merges;
6. state files update;
7. branch/worktree is cleaned.

Only then allow larger autonomous task batches.

## Phase E — Human visibility

The human approver should receive concise status summaries such as:

```text
MATRIX V1
Milestone: Database foundation
Completed: 7/9 tasks
Tests: 186 passed, 0 failed
Review blockers: 0
Disk: 2.1 GB free
Human decisions required: 0
Next: WhatsApp webhook ingestion
```

The system should avoid asking the human to approve routine implementation details.

## Phase F — Production

Production deployment remains gated by:
- staging pass;
- release tests;
- reviewer approval;
- human approval where policy requires;
- rollback plan.

The autonomous architecture is complete when an agent can safely resume from repository state after restart and continue from the next valid task without reconstructing intent from chat history.
