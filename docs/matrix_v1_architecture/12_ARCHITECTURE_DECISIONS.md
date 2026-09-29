# 12 — Architecture Decisions and Open Questions

This file is the initial ADR register.

## ADR-001 — Modular monolith, not microservices
**Decision:** Use one codebase with API and worker processes.

**Reason:** V1 complexity does not justify distributed service boundaries.

**Status:** Accepted.

## ADR-002 — FastAPI/Python
**Decision:** Use Python + FastAPI.

**Reason:** Strong fit for OCR/AI pipeline, clean typing/schema tooling, agent implementation simplicity.

**Status:** Accepted.

## ADR-003 — PostgreSQL as canonical store
**Decision:** Managed PostgreSQL is the source of truth.

**Reason:** Relational contact/company model plus JSONB flexibility.

**Status:** Accepted.

## ADR-004 — Redis + Celery in V1
**Decision:** Use Redis as broker and Celery as background-task framework.

**Reason:** Keep webhook fast; support retries and external-provider workloads without introducing RabbitMQ.

**Status:** Accepted.

## ADR-005 — Provider abstractions
**Decision:** OCR, AI extraction, WhatsApp, object storage, and Sheets use interfaces.

**Reason:** Avoid vendor lock-in and enable self-hosted OCR later.

**Status:** Accepted.

## ADR-006 — Google Vision first
**Decision:** Initial OCR adapter uses Google Cloud Vision.

**Reason:** Low implementation burden for V1.

**Status:** Accepted, replaceable.

## ADR-007 — OpenAI structured extraction
**Decision:** Use schema-constrained structured contact extraction.

**Reason:** Canonical JSON is the machine artifact; summaries are secondary.

**Status:** Accepted, provider replaceable.

## ADR-008 — Managed DB outside constrained AI VM
**Decision:** Do not permanently host PostgreSQL on the 5 GB AI automation VM.

**Reason:** Preserve disk and separate development orchestration from production persistence.

**Status:** Accepted.

## ADR-009 — Original images in object storage
**Decision:** Store card image binaries outside PostgreSQL.

**Reason:** Keep DB small and suitable for structured data.

**Status:** Accepted.

## ADR-010 — Multi-tenant-ready schema
**Decision:** Carry `organization_id` in business-domain tables.

**Reason:** Avoid expensive tenancy retrofit later.

**Status:** Accepted.

---

# Open questions that do NOT block initial implementation

1. Which exact managed PostgreSQL provider will be used?
2. Which exact S3-compatible object-storage provider will be used?
3. Exact OpenAI model name at deployment time.
4. Exact business-card classification implementation/threshold.
5. Final image retention duration.
6. Exact production hosting platform.
7. Whether user confirmation/correction editing is added before full V1 launch.
8. Whether Sheets OAuth is operator-configured or user self-service in V1.

Agents may implement configuration points for these questions, but must not invent irreversible provider-specific architecture.

---

# Decisions requiring human approval

The following require an ADR plus explicit human approval:
- change primary programming language/framework;
- change canonical database;
- introduce a new message broker;
- split into microservices;
- alter tenancy strategy;
- add automatic destructive contact merging;
- introduce a new paid external provider;
- materially change data retention/privacy behavior;
- change production deployment topology;
- expose new public/authenticated user surfaces.
