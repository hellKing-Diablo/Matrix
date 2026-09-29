# 04 — API Contracts

All internal REST endpoints use `/api/v1`.

## 1. WhatsApp webhook verification

### `GET /webhooks/whatsapp`

Purpose: Meta webhook verification.

Expected query parameters:
- `hub.mode`
- `hub.verify_token`
- `hub.challenge`

Behavior:
- compare verify token using constant-time-safe comparison where practical;
- on valid subscription verification return raw `hub.challenge`;
- otherwise return 403.

## 2. WhatsApp inbound webhook

### `POST /webhooks/whatsapp`

Purpose: Receive WhatsApp events.

Rules:
1. validate request shape;
2. derive provider event/message ID;
3. insert `webhook_events`;
4. if duplicate unique constraint is hit, return success without reprocessing;
5. enqueue relevant media message;
6. return 200 quickly.

Do not run OCR or AI inside this request.

Response:
```json
{"status":"accepted"}
```

## 3. Health endpoints

### `GET /health/live`
Returns process liveness only.

Example:
```json
{"status":"ok"}
```

### `GET /health/ready`
Checks:
- PostgreSQL connectivity;
- Redis connectivity;
- required configuration presence.

Do not call OpenAI/Google/Meta on every readiness request.

## 4. Scan status

### `GET /api/v1/scans/{scan_id}`

Purpose: Internal/admin observability.

Response:
```json
{
  "id": "uuid",
  "status": "completed",
  "classification": "business_card",
  "contact_id": "uuid",
  "failure_code": null,
  "created_at": "...",
  "completed_at": "..."
}
```

No raw provider secrets or full webhook payloads in standard response.

## 5. Contact read

### `GET /api/v1/contacts/{contact_id}`

Response:
```json
{
  "id": "uuid",
  "full_name": "John Smith",
  "job_title": "Director",
  "company": {
    "id": "uuid",
    "name": "ABC Technologies"
  },
  "contact_methods": [
    {"kind":"phone","label":"mobile","value":"+919876543210"},
    {"kind":"email","label":"work","value":"john@abc.com"}
  ],
  "address": "Ahmedabad, Gujarat",
  "extra_fields": {}
}
```

## 6. List contacts

### `GET /api/v1/contacts`

Query parameters:
- `limit` default 50, max 100;
- `cursor` preferred over offset;
- `q` optional basic name/company/email search.

V1 endpoint may be internal only.

## 7. Google Sheets connection configuration

A full public OAuth UI is not required in V1. Configuration may initially be performed by an operator/agent using environment-backed credentials and an internal endpoint.

### `POST /api/v1/integrations/google-sheets`

Request:
```json
{
  "spreadsheet_id": "...",
  "worksheet_name": "Contacts",
  "column_mapping": {
    "full_name": "Name",
    "company": "Company",
    "job_title": "Title",
    "primary_phone": "Phone",
    "primary_email": "Email"
  }
}
```

Response:
```json
{
  "id": "uuid",
  "provider": "google_sheets",
  "status": "active"
}
```

Authentication for this internal endpoint must be implemented before exposing it publicly.

## 8. Retry failed scan

### `POST /api/v1/scans/{scan_id}/retry`

Allowed only when status is retryable.

Behavior:
- create/enqueue a fresh processing attempt;
- do not duplicate canonical contact;
- preserve previous failure metadata.

## 9. Error envelope

For MATRIX-owned REST APIs:

```json
{
  "error": {
    "code": "SCAN_NOT_FOUND",
    "message": "Scan not found",
    "request_id": "..."
  }
}
```

Do not return provider stack traces or secret-bearing exceptions.

## 10. Authentication

V1 priorities:
- Meta webhook: provider verification/signature validation;
- internal/admin endpoints: simple secure operator authentication initially;
- future user-facing API: OAuth/JWT/session system in a later phase.

No endpoint should be publicly unauthenticated except required webhook and health surfaces.
