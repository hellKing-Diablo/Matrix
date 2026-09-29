# 06 — Background Jobs, Queueing, and Idempotency

## 1. Celery tasks

### `process_business_card(scan_id)`
Orchestrates the card-processing pipeline.

Must be restartable from persisted scan state.

### `sync_contact_to_google_sheets(sync_run_id)`
Handles one Sheets sync operation.

### `send_whatsapp_message(message_request_id or payload_ref)`
Optional dedicated outbound messaging task. V1 may call the messaging provider from the main worker if kept isolated behind an interface.

### `retry_failed_scan(scan_id)`
Administrative wrapper that verifies retry eligibility and re-enqueues processing.

## 2. Why queueing exists

The webhook path should remain fast:

```text
WhatsApp → FastAPI → persist event → enqueue job → HTTP 200
```

Heavy work:

```text
Redis → Celery worker → OCR → AI → DB → Sheets → WhatsApp
```

## 3. Celery configuration baseline

- broker: Redis;
- JSON serialization only;
- task acknowledgement configured to avoid silent loss;
- sensible worker prefetch;
- per-task soft/hard timeouts;
- retry policies for external providers;
- structured logging with task id and scan id.

Avoid pickle serialization.

## 4. Idempotency keys

### Incoming webhook
Use:
```text
whatsapp:{provider_message_id}
```

Durable enforcement:
`webhook_events(provider, provider_event_id)` unique constraint.

### Scan processing
Primary idempotency unit:
`scan_id`.

Before creating new canonical resources, inspect scan state and linked `contact_id`.

### Sheets sync
Recommended idempotency key:
```text
google_sheets:{integration_connection_id}:{contact_id}:{contact_updated_at}
```

For V1, store a deterministic external row key such as MATRIX contact UUID in a hidden or explicit Sheet column. Update/UPSERT based on that key rather than blindly appending on every retry.

## 5. Retry policy baseline

For transient errors:
- attempt 1 immediately;
- retry after ~5 seconds;
- then ~30 seconds;
- then ~2 minutes;
- bounded maximum attempts, e.g. 5.

Add jitter in production.

Do not retry permanent validation failures.

## 6. Dead/final failures

When retry budget is exhausted:
- mark related scan/sync run `failed`;
- persist safe error code;
- emit structured log;
- optionally notify user with generic failure message;
- make failure discoverable via status endpoint.

## 7. Event vocabulary

Internal domain events may initially be function calls/task launches rather than a dedicated event bus.

Names:
```text
scan.received
scan.rejected
scan.ocr_completed
scan.extracted
contact.created
contact.updated
integration.sync_requested
integration.sync_succeeded
integration.sync_failed
```

Do not introduce RabbitMQ or Kafka in V1 merely to implement this vocabulary.
