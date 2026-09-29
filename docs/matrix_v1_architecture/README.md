# MATRIX V1 — Technical Architecture Specification

**Status:** Architecture baseline  
**Audience:** Autonomous coding agents, reviewer agents, testing agents, and human approver  
**Primary goal:** Build the first production-capable vertical slice of MATRIX.

## 1. Product definition

MATRIX V1 is a WhatsApp-first business-card ingestion system.

The canonical user journey is:

```text
User receives a business card
        ↓
User sends a photo of the card to MATRIX on WhatsApp
        ↓
MATRIX validates the incoming image
        ↓
MATRIX detects whether it is likely a business card
        ↓
Google Vision OCR extracts raw text
        ↓
OpenAI converts OCR text into structured contact JSON
        ↓
Pydantic validates and normalizes the result
        ↓
MATRIX stores the scan and contact in PostgreSQL
        ↓
MATRIX syncs the contact to the user's configured Google Sheet
        ↓
MATRIX sends a human-readable confirmation on WhatsApp
```

## 2. V1 scope

### In scope
- WhatsApp Cloud API webhook ingestion
- Business-card image intake
- Media download
- File validation
- Business-card classification
- Google Cloud Vision OCR
- OpenAI structured extraction
- Pydantic validation
- Contact normalization
- Contact persistence in PostgreSQL
- Basic duplicate detection
- Google Sheets sync
- WhatsApp confirmation/error messages
- Background processing with Celery
- Redis as Celery broker
- S3-compatible object storage for original images
- Dockerized API and worker
- Logging, retries, idempotency, health checks, tests

### Explicitly out of scope
- Web dashboard
- Full CRM UI
- Team assignment
- Reminder engine
- Calendar integration
- Gmail integration
- Voice commands
- Advanced workflow automation
- Billing
- Production-grade multi-region deployment
- RabbitMQ
- Self-hosted OCR
- Complex contact merge UI

## 3. Technology baseline

| Concern | Decision |
|---|---|
| Language | Python 3.12+ |
| API framework | FastAPI |
| Schema validation | Pydantic v2 |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Database | Managed PostgreSQL |
| Task system | Celery |
| Broker | Redis |
| OCR | Google Cloud Vision through `OCRProvider` |
| AI extraction | OpenAI through `StructuredExtractionProvider` |
| Image storage | S3-compatible object storage |
| WhatsApp | Meta WhatsApp Cloud API |
| Sheets | Google Sheets API + OAuth 2.0 |
| Containers | Docker |
| Local orchestration | Docker Compose |
| Tests | Pytest |
| Lint/format | Ruff |
| Type checking | mypy or pyright |

## 4. Architectural principles

1. **PostgreSQL is the system of record.** Google Sheets is a downstream integration.
2. **Provider-specific APIs must remain behind interfaces.**
3. **Webhook handling must remain fast.** Long-running work belongs in Celery.
4. **Every inbound WhatsApp event must be idempotent.**
5. **The original image, raw OCR output, structured extraction, and final normalized contact are separate artifacts.**
6. **Agents must not change foundational architecture without an explicit Architecture Decision Record (ADR) and human approval.**
7. **No agent may hard-code API keys, OAuth tokens, secrets, phone numbers, sheet IDs, or environment-specific URLs.**
8. **A failed downstream integration must not erase or roll back an already-valid contact.**
9. **All external calls must have timeouts and retry policies.**
10. **The system must remain multi-tenant-ready even if V1 is initially used by one organization.**

## 5. Repository shape

```text
matrix/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── providers/
│   │   ├── ocr/
│   │   ├── extraction/
│   │   ├── messaging/
│   │   ├── storage/
│   │   └── integrations/
│   ├── workers/
│   └── main.py
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
├── docker/
├── docs/
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── .env.example
```

## 6. Documentation map

Read in this order:

1. `01_PRODUCT_SCOPE.md`
2. `02_SYSTEM_ARCHITECTURE.md`
3. `03_DATA_MODEL.md`
4. `04_API_CONTRACTS.md`
5. `05_PROCESSING_PIPELINE.md`
6. `06_JOBS_AND_EVENTS.md`
7. `07_PROVIDER_INTERFACES.md`
8. `08_SECURITY_RELIABILITY.md`
9. `09_DEPLOYMENT.md`
10. `10_TESTING_AND_ACCEPTANCE.md`
11. `11_IMPLEMENTATION_ORDER.md`
12. `12_ARCHITECTURE_DECISIONS.md`

## 7. Definition of V1 complete

V1 is complete only when a real WhatsApp business-card image can travel end-to-end through the production-like system and:

- the webhook responds quickly;
- the image is stored;
- OCR output is captured;
- structured extraction is validated;
- a contact is persisted;
- duplicate handling is applied;
- the contact is synced to a configured Google Sheet;
- a confirmation is sent to the WhatsApp user;
- failures are observable and retryable;
- duplicate webhook delivery does not create duplicate contacts;
- automated tests cover the full critical path.
