# 05 — Test and Review Gates

## 1. Gate sequence

```text
Implementation
    ↓
Static checks
    ↓
Unit tests
    ↓
Integration tests
    ↓
Tester acceptance verification
    ↓
Reviewer
    ↓
Integration merge
    ↓
Combined tests
    ↓
Staging E2E
```

## 2. Static checks

Required where configured:
- Ruff;
- type checking;
- dependency/secret scanning where available;
- migration consistency.

## 3. Tester obligations

Tester must:
- read acceptance criteria;
- run required tests;
- inspect changed code enough to design meaningful negative tests;
- report exact failing command/output summary;
- avoid fixing production code directly unless reassigned as Coder.

## 4. Review checklist

Reviewer checks:

### Architecture
- follows product architecture;
- provider boundaries preserved;
- no unnecessary new service.

### Correctness
- edge cases;
- transaction boundaries;
- idempotency;
- retry safety.

### Security
- no hard-coded secrets;
- authentication/authorization intact;
- sensitive data not logged;
- safe file handling.

### Reliability
- timeouts;
- bounded retries;
- controlled failures;
- no silent exception swallowing.

### Data
- migrations safe;
- constraints appropriate;
- no destructive behavior without approval.

### Tests
- acceptance criteria tested;
- regressions likely covered;
- fakes/mocks do not create false confidence.

## 5. Review severity

- `BLOCKER`: security/data loss/architecture violation.
- `MAJOR`: correctness/reliability problem.
- `MINOR`: maintainability/documentation issue.
- `NIT`: optional.

A task cannot merge with unresolved BLOCKER or MAJOR findings.

## 6. Independence rule

The agent responsible for a material implementation may not be the only agent performing final review.

Logical role separation is sufficient even if the same underlying model is used at a different time/context.
