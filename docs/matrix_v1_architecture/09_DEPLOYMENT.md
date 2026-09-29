# 09 — Deployment Architecture

## 1. Separation of concerns

The autonomous AI VM is primarily a **development/orchestration machine**.

Do not make it the permanent home of:
- PostgreSQL data;
- business-card images;
- backups;
- large persistent Docker volumes.

## 2. V1 environments

### Development
Can run:
- FastAPI container;
- Celery container;
- Redis container;
- fake providers;
- optional local Postgres for developer convenience if disk permits.

Preferred when disk is constrained:
- managed development PostgreSQL;
- managed/object storage;
- local Redis only.

### Staging
- public HTTPS endpoint;
- separate database/schema or separate project;
- separate object-storage prefix/bucket;
- test WhatsApp number/config where possible;
- sandbox/test Sheet.

### Production
- public HTTPS endpoint;
- managed PostgreSQL;
- private object storage;
- Redis;
- API container;
- worker container.

## 3. Docker image strategy

One application image, multiple commands.

Example:

API:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Worker:
```bash
celery -A app.workers.celery_app worker --loglevel=INFO
```

Do not build unrelated duplicated images unless justified.

## 4. Dockerfile baseline

- slim Python base;
- pinned dependencies;
- non-root runtime user;
- no development tools in final stage;
- multi-stage build if native dependencies make it useful;
- `.dockerignore` excludes `.git`, tests caches, local artifacts, `.env`.

## 5. Docker Compose baseline

Services:
```text
api
worker
redis
```

PostgreSQL should normally be remote in the constrained-VM setup.

## 6. Configuration

Environment variables:

```text
APP_ENV
DATABASE_URL
REDIS_URL

WHATSAPP_VERIFY_TOKEN
WHATSAPP_ACCESS_TOKEN
WHATSAPP_PHONE_NUMBER_ID
WHATSAPP_APP_SECRET

GOOGLE_CLOUD_PROJECT
GOOGLE_APPLICATION_CREDENTIALS / equivalent secret injection

OPENAI_API_KEY
OPENAI_MODEL

OBJECT_STORAGE_ENDPOINT
OBJECT_STORAGE_BUCKET
OBJECT_STORAGE_ACCESS_KEY
OBJECT_STORAGE_SECRET_KEY

GOOGLE_SHEETS_CREDENTIAL_REF
```

No production secrets in Compose files committed to Git.

## 7. CI pipeline

At minimum:

```text
checkout
  ↓
dependency install
  ↓
ruff
  ↓
type check
  ↓
unit tests
  ↓
integration tests
  ↓
build Docker image
  ↓
container smoke test
```

Deployment occurs only after review/approval in the future autonomous-agent architecture.

## 8. VM disk hygiene

Because the AI VM has a tight disk budget:
- avoid local Postgres volume;
- prune Docker build cache periodically;
- keep card images remote;
- keep dependency caches bounded;
- do not store downloaded model weights;
- use slim container images;
- rotate logs;
- clone repository shallowly if useful.

## 9. HTTPS

WhatsApp webhooks require a publicly reachable HTTPS endpoint.

Use a reverse proxy/platform ingress that terminates TLS.

The exact hosting provider is intentionally not locked by this architecture.
