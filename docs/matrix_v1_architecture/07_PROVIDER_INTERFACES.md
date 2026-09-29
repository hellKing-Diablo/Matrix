# 07 — Provider Interfaces

Vendor SDKs must not leak into domain services.

## 1. OCRProvider

```python
class OCRResult(BaseModel):
    provider: str
    raw_text: str
    confidence: float | None = None
    language_hints: list[str] = []
    metadata: dict = {}

class OCRProvider(Protocol):
    async def extract_text(self, object_ref: str) -> OCRResult:
        ...
```

Initial implementation:
- `GoogleVisionOCRProvider`

Future:
- `PaddleOCRProvider`
- other self-hosted provider

## 2. StructuredExtractionProvider

```python
class StructuredExtractionProvider(Protocol):
    async def extract_contact(
        self,
        *,
        raw_text: str,
        source_context: dict
    ) -> ExtractedContact:
        ...
```

Initial implementation:
- `OpenAIStructuredExtractionProvider`

Rules:
- use structured/schema-constrained output;
- low temperature/deterministic settings where supported;
- model name configured through environment;
- provider timeout mandatory;
- record provider/model metadata for debugging without logging sensitive prompts unnecessarily.

## 3. ObjectStorageProvider

```python
class ObjectStorageProvider(Protocol):
    async def put_private(
        self,
        *,
        key: str,
        content: bytes,
        content_type: str
    ) -> str:
        ...

    async def get_private(self, object_ref: str) -> bytes:
        ...
```

Initial implementation can use any S3-compatible provider.

## 4. WhatsAppProvider

```python
class WhatsAppProvider(Protocol):
    async def get_media(self, media_id: str) -> bytes:
        ...

    async def send_text(self, to_e164: str, text: str) -> str:
        ...
```

Initial:
- Meta WhatsApp Cloud API.

## 5. GoogleSheetsProvider

```python
class GoogleSheetsProvider(Protocol):
    async def upsert_contact(
        self,
        *,
        connection: IntegrationConnection,
        contact: ContactProjection
    ) -> ExternalSyncResult:
        ...
```

The adapter owns:
- column mapping;
- row lookup;
- upsert mechanics;
- Google-specific errors.

Core contact service must not know A1 ranges or Google SDK types.

## 6. Provider selection

Use dependency injection/configuration:

```text
OCR_PROVIDER=google_vision
EXTRACTION_PROVIDER=openai
OBJECT_STORAGE_PROVIDER=s3
```

Factories may resolve implementations at startup.

## 7. Provider test doubles

Every provider interface must have a fake implementation for tests.

Examples:
- `FakeOCRProvider`
- `FakeExtractionProvider`
- `FakeSheetsProvider`
- `FakeWhatsAppProvider`
- `InMemoryObjectStorageProvider`

End-to-end CI tests must not require paid external APIs.
