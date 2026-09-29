# 11 — Implementation Order for Autonomous Agents

Agents should implement in this dependency order unless an approved plan says otherwise.

## Phase 0 — Repository foundation
Deliver:
- Python project;
- `pyproject.toml`;
- FastAPI app;
- settings module;
- structured logging;
- Ruff;
- type checking;
- Pytest;
- Dockerfile;
- Compose;
- CI skeleton.

Acceptance:
- `/health/live` works;
- tests/lint/type-check pass.

## Phase 1 — Database foundation
Deliver:
- SQLAlchemy base/session;
- Alembic;
- organizations;
- WhatsApp accounts;
- webhook events;
- scans;
- companies;
- contacts;
- contact methods;
- integration connections;
- sync runs.

Acceptance:
- migrations up/down;
- DB integration tests.

## Phase 2 — WhatsApp ingestion
Deliver:
- verification endpoint;
- webhook endpoint;
- event parsing;
- idempotency ledger;
- scan creation;
- enqueue task.

Use fake enqueue/provider during early tests.

## Phase 3 — Celery/Redis
Deliver:
- Celery application;
- Redis broker config;
- `process_business_card` skeleton;
- task logging;
- retry foundation.

## Phase 4 — Object storage and media
Deliver:
- WhatsApp media provider;
- object-storage interface/implementation;
- file validation;
- hash computation.

## Phase 5 — OCR
Deliver:
- `OCRProvider`;
- fake OCR;
- Google Vision adapter;
- timeout/error mapping;
- persistence of OCR result.

## Phase 6 — Structured extraction
Deliver:
- Pydantic canonical schema;
- extraction provider interface;
- fake extraction provider;
- OpenAI structured-output adapter;
- validation/repair rules.

## Phase 7 — Normalization and duplicate resolution
Deliver:
- normalization utilities;
- minimum quality gate;
- duplicate resolver;
- contact/company/contact-method persistence.

## Phase 8 — Google Sheets
Deliver:
- Google Sheets provider;
- column mapping;
- deterministic row key / upsert;
- sync runs;
- independent retry behavior.

## Phase 9 — WhatsApp responses
Deliver:
- confirmation formatter;
- rejection/retake/error messages;
- outbound provider adapter.

## Phase 10 — Hardening
Deliver:
- rate limiting;
- metrics;
- improved logs;
- request IDs;
- security checks;
- failure dashboards/queries;
- staging smoke tests.

## Agent constraints

Agents must not:
- introduce microservices;
- introduce RabbitMQ;
- change PostgreSQL to another database;
- bypass provider interfaces;
- replace Celery/Redis;
- add a frontend dashboard;
- add billing/auth platform work;
- change core duplicate policy;
- add new major external dependencies;

without an ADR and human approval.

## Preferred task granularity

A coding task should usually be completable with:
- one focused domain goal;
- a small number of files;
- explicit acceptance criteria;
- tests.

Avoid tasks like:
> "Build the whole backend."

Prefer:
> "Implement WhatsApp webhook idempotency using `webhook_events` unique constraint and tests for duplicate delivery."
