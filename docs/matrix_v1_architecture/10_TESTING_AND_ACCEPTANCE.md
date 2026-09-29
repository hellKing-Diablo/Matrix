# 10 — Testing Strategy and Acceptance Criteria

## 1. Test pyramid

### Unit tests
Cover:
- normalization;
- duplicate matching;
- schemas;
- provider adapters with mocked SDK responses;
- state transitions;
- error classification;
- message formatting.

### Integration tests
Cover:
- FastAPI + PostgreSQL;
- worker task + DB;
- Redis/Celery test configuration;
- Alembic migrations;
- repository/service boundaries.

### End-to-end tests
Use fake external providers and simulate:

```text
fake WhatsApp event
→ API
→ queue
→ worker
→ fake OCR
→ fake OpenAI extraction
→ PostgreSQL
→ fake Sheets
→ fake WhatsApp confirmation
```

## 2. Mandatory V1 scenarios

### Happy path
Given a valid card:
- scan completes;
- contact exists;
- methods exist;
- Sheet sync succeeds;
- confirmation is sent.

### Duplicate webhook
Same WhatsApp event delivered twice:
- one webhook-event record;
- one scan or one logical processing sequence;
- no duplicate contact;
- no duplicate Sheet row.

### Duplicate card/contact
Two scans containing same normalized email:
- one canonical contact;
- two scan records linked to it.

### Random photo
- rejected;
- no contact;
- no Sheet row;
- user receives correction.

### Blurry/insufficient card
- no low-quality canonical contact;
- status indicates retry/quality failure;
- user asked to retake.

### OCR provider timeout
- task retries;
- scan not duplicated;
- eventually succeeds or ends in failed state.

### OpenAI validation failure
- one bounded repair/retry path;
- no invalid JSON stored as canonical contact.

### Google Sheets failure
- contact remains saved;
- sync run records failure;
- sync retries independently;
- no duplicate row after retry.

### Redis unavailable at webhook enqueue
- API returns controlled server error or fallback behavior;
- event persistence behavior is documented/tested;
- no silent message loss.

## 3. Security tests
- invalid webhook verification token rejected;
- invalid provider signature rejected where applicable;
- oversized image rejected;
- internal endpoint without auth rejected;
- secrets never appear in standard error responses.

## 4. Migration tests
For every Alembic migration:
- upgrade from previous revision;
- application boots;
- downgrade when supported.

## 5. Definition of done for each coding task

A task is not complete unless:
- code implemented;
- tests added/updated;
- lint passes;
- type checking passes;
- relevant architecture docs updated;
- no secrets committed;
- migration included if schema changed;
- acceptance criteria demonstrated.

## 6. Release acceptance gate

Before V1 release:
- all mandatory scenarios pass;
- clean database migration from zero;
- Docker image boots;
- API readiness works;
- worker processes a full fake-provider E2E job;
- real provider smoke test succeeds in staging;
- duplicate/idempotency test succeeds;
- rollback procedure documented.
