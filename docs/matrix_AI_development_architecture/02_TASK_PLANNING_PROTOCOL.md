# 02 — Task Planning Protocol

## 1. Planner output

The Planner converts architecture into a dependency-aware task DAG.

Each task must contain:

```json
{
  "id": "MATRIX-001",
  "title": "Implement webhook idempotency ledger",
  "type": "backend",
  "status": "planned",
  "priority": "high",
  "dependencies": ["MATRIX-000"],
  "owner_role": "coder",
  "specialty": "backend",
  "scope": [
    "app/api/webhooks/",
    "app/models/webhook_event.py",
    "tests/"
  ],
  "goal": "Prevent duplicate WhatsApp delivery from creating duplicate processing.",
  "acceptance_criteria": [
    "duplicate provider event is accepted safely",
    "only one logical processing sequence is created",
    "tests cover duplicate delivery"
  ],
  "forbidden_changes": [
    "do not redesign database",
    "do not change queue technology"
  ],
  "required_tests": [
    "unit",
    "integration"
  ],
  "risk": "medium",
  "requires_human_approval": false
}
```

## 2. Task sizing

Good task:
- one clear deliverable;
- bounded code surface;
- measurable tests;
- usually one logical PR/merge.

Bad task:
> Build backend.

Good replacement:
- bootstrap settings and app factory;
- add DB session;
- create webhook-event migration;
- implement webhook verification;
- implement webhook idempotency;
- enqueue image task.

## 3. Dependency planning

Planner must identify:
- schema dependencies;
- interface dependencies;
- external credential dependencies;
- migration ordering;
- test fixtures/fakes required first.

## 4. Vertical-slice priority

Where possible, prioritize an early thin end-to-end path using fake providers.

Example:
```text
fake WhatsApp webhook
→ FastAPI
→ queue
→ fake OCR
→ fake extraction
→ DB
→ fake Sheets
→ fake confirmation
```

This reveals architectural integration problems before live-provider work.

## 5. Architecture traceability

Every significant task should reference relevant architecture docs.

Example:
```json
"architecture_refs": [
  "product/04_API_CONTRACTS.md#whatsapp-inbound-webhook",
  "product/06_JOBS_AND_EVENTS.md#idempotency-keys"
]
```

## 6. Replanning

Planner may replan when:
- tests reveal missing dependency;
- an ADR changes architecture;
- external provider contract changes;
- integration conflict requires sequencing change.

Replanning must not silently discard completed work.
