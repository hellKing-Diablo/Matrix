# 08 — Security, Reliability, and Observability

## 1. Secrets

Never commit:
- Meta access tokens;
- Google credentials;
- OpenAI API keys;
- database URLs;
- Redis passwords;
- object-storage credentials.

Use environment variables locally and a managed secret store in production.

`.env.example` contains names only, never real values.

## 2. Webhook security

Implement:
- Meta verification flow;
- provider signature validation where supported by current API contract;
- payload size limits;
- strict JSON parsing;
- idempotent provider-message handling.

## 3. Authorization

Internal/admin endpoints must not be exposed without authentication.

V1 may use a single operator token behind HTTPS, but it must be:
- random;
- stored as secret;
- rotatable;
- checked securely.

Long-term user auth is out of scope.

## 4. Data minimization

Store only what is needed for product function and debugging.

Avoid:
- logging full webhook payloads in production;
- logging OCR text at INFO level;
- logging full contact JSON at INFO level;
- exposing original images publicly.

## 5. Logging

Every relevant log entry should include:
- `request_id`;
- `scan_id` when available;
- `task_id` when in Celery;
- `organization_id` when available;
- provider name;
- safe error code.

Use structured JSON logs.

## 6. Metrics

Track at minimum:
- webhook requests;
- webhook duplicate rate;
- scan processing count;
- scan completion/failure rate;
- OCR latency;
- extraction latency;
- overall processing latency;
- Sheets sync success/failure;
- provider 429/5xx counts;
- queue depth if available.

## 7. Timeouts

Every outbound HTTP call must specify connect/read timeouts.

No unbounded external request.

## 8. Retry categories

Retry:
- network timeout;
- transient DNS/network;
- HTTP 429;
- provider 5xx.

Usually do not retry:
- HTTP 400 due to our invalid payload;
- authentication failure until credentials are fixed;
- unsupported image;
- semantic validation failure.

## 9. Database transactions

Contact persistence should be transactional.

Do not hold a DB transaction open while calling Google/OpenAI/Meta.

Pattern:
1. external processing;
2. short DB transaction;
3. commit canonical state;
4. downstream integration job.

## 10. Rate limiting

V1 can implement lightweight per-user or per-organization rate limits using Redis.

Rate limiting must fail gracefully and be configurable.

## 11. File safety

Before image decoding:
- max byte-size enforcement;
- allowlist MIME types;
- reject malformed content;
- do not trust file extension;
- use image library safely;
- no arbitrary file execution.

## 12. Object-storage access

- private bucket/container;
- no public-read ACL;
- access through app credentials or signed short-lived URLs;
- lifecycle policy may delete old raw images in a later privacy policy.

## 13. Database backups

Managed PostgreSQL should provide backups or point-in-time recovery when production usage begins.

For prototype/free tiers, document provider limitations explicitly.

## 14. Cost controls

Configuration should allow:
- per-org scan limits;
- provider usage metrics;
- model selection;
- maximum retries;
- maximum image size.

Unexpected cost growth must be observable.
