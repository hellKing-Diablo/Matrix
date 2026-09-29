# 01 — Product Scope and Behavioral Contract

## 1. Primary actor

A business user who receives business cards at events and wants the contact information captured automatically.

## 2. Happy path

1. User sends a business-card image to the configured MATRIX WhatsApp number.
2. WhatsApp Cloud API delivers the webhook event.
3. MATRIX acknowledges receipt quickly.
4. MATRIX downloads and stores the image.
5. MATRIX determines whether the image is a valid, processable business-card candidate.
6. Google Vision returns OCR text.
7. OpenAI converts the OCR text into a strict contact schema.
8. MATRIX validates and normalizes the result.
9. MATRIX checks for a likely duplicate.
10. MATRIX creates or updates the canonical contact.
11. MATRIX syncs the normalized contact to Google Sheets.
12. MATRIX replies with the extracted contact details and sync status.

## 3. Non-business-card behavior

If an image is clearly not a business card:
- do not create a contact;
- do not sync to Google Sheets;
- persist the scan with `rejected_not_business_card`;
- respond with a concise message requesting a business-card image.

## 4. Low-quality card behavior

If the image appears to be a business card but extraction quality is too low:
- preserve image and extraction artifacts;
- mark scan as `needs_retry`;
- do not create a canonical contact unless minimum quality rules pass;
- ask the user to retake the image.

## 5. Minimum contact quality rule

A scan may create a canonical contact when:
- `full_name` exists; AND
- at least one of the following exists:
  - phone number,
  - email,
  - company name,
  - website.

This is a V1 policy and may be changed later through an ADR.

## 6. Canonical extracted fields

```json
{
  "full_name": "string|null",
  "first_name": "string|null",
  "last_name": "string|null",
  "job_title": "string|null",
  "department": "string|null",
  "company": {
    "name": "string|null",
    "industry": "string|null",
    "description": "string|null"
  },
  "phones": [
    {
      "value": "string",
      "label": "mobile|office|whatsapp|fax|other|null"
    }
  ],
  "emails": [
    {
      "value": "string",
      "label": "work|personal|other|null"
    }
  ],
  "websites": ["string"],
  "social_links": [
    {
      "platform": "linkedin|x|instagram|facebook|other",
      "url": "string"
    }
  ],
  "address": "string|null",
  "extra_fields": {},
  "source_language": "string|null"
}
```

## 7. User-facing confirmation

Example:

```text
Saved contact:

John Smith
Director — ABC Technologies
Phone: +91 98765 43210
Email: john@abc.com

Synced to your Google Sheet.
```

Do not expose raw JSON to ordinary users.

## 8. V1 duplicate policy

A likely duplicate is determined by normalized identifiers in this order:

1. exact normalized email;
2. exact normalized phone;
3. same normalized full name + same normalized company name.

For V1:
- if exact email or phone matches, update missing fields on the existing contact;
- do not overwrite existing non-null values with lower-confidence values automatically;
- record the new scan as a separate source artifact;
- do not create a second canonical contact.

## 9. Performance objectives

These are engineering targets, not hard guarantees:

- webhook acknowledgement: under 2 seconds where possible;
- normal card processing: under 20 seconds;
- external API calls use explicit timeouts;
- background processing must not block webhook acknowledgement.

## 10. Privacy baseline

Business-card images and extracted contact data are personal/business contact information. Treat them as sensitive application data:
- never write secrets or full card images to application logs;
- restrict object storage access;
- use TLS for external traffic;
- encrypt managed storage using provider defaults;
- support deletion of a contact and its linked scans later.
