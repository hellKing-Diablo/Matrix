# 11 — Autonomous Execution Loop

The Orchestrator follows this loop until the current milestone is complete or a true human decision is required.

```text
LOAD STATE
   ↓
VALIDATE RESOURCES
   ↓
SELECT READY TASKS
   ↓
ASSIGN SPECIALIST
   ↓
IMPLEMENT
   ↓
TEST
   ↓
FAIL? ── yes ─→ CORRECTION LOOP
   │
   no
   ↓
REVIEW
   ↓
CHANGES? ── yes ─→ CORRECTION LOOP
   │
   no
   ↓
INTEGRATE
   ↓
COMBINED TESTS
   ↓
FAIL? ── yes ─→ INTEGRATION FIX
   │
   no
   ↓
PERSIST STATE
   ↓
MORE TASKS? ── yes ─→ SELECT READY TASKS
   │
   no
   ↓
STAGING / RELEASE GATE
```

## Correction loop

1. record failure;
2. classify root cause;
3. reopen original task or create correction task;
4. assign appropriate specialist;
5. implement fix;
6. rerun relevant tests;
7. rerun review if material code changed.

## Stop conditions

The autonomous loop stops only when:
- milestone complete;
- human approval required;
- critical resource constraint;
- missing credential/external dependency prevents progress;
- architecture ambiguity cannot safely be resolved;
- repeated failure exceeds retry/replan threshold.

## Repeated failure policy

After 3 materially similar failed correction cycles:
- stop repeating the same approach;
- ask Planner/Reviewer for root-cause replan;
- if architecture change is proposed, escalate according to approval policy.
