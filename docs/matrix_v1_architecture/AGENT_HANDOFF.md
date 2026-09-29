# MATRIX V1 — Agent Handoff Contract

## Mission

Implement the V1 architecture exactly as specified in this folder.

## First action for any implementation agent

Before coding:
1. read `README.md`;
2. read the relevant numbered architecture files;
3. identify dependencies;
4. produce a scoped implementation plan;
5. list files expected to change;
6. list acceptance tests.

## Non-negotiable invariants

- PostgreSQL is canonical.
- Webhook path stays lightweight.
- OCR/AI/Sheets happen outside the webhook request.
- External providers remain behind interfaces.
- All webhook delivery is idempotent.
- No real secrets in repository.
- Original image is private.
- Sheets failure never destroys a valid contact.
- Schema changes require Alembic.
- V1 remains a modular monolith.

## Required implementation quality

Every task:
- typed code where practical;
- tests;
- controlled errors;
- structured logs;
- no silent exception swallowing;
- explicit timeouts for network calls;
- retry only transient failures;
- documentation updated when contracts change.

## When blocked

Do not silently invent architecture.

If ambiguity affects a foundational decision:
- create a short ADR proposal;
- describe options and impact;
- stop that architectural branch until approved;
- continue unrelated safe work if possible.
