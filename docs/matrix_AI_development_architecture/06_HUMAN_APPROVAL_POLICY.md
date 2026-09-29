# 06 — Human Approval Policy

## 1. Goal

Minimize routine human involvement while retaining control over high-impact decisions.

## 2. No approval normally required

- implementing approved endpoint;
- adding tests;
- fixing lint/type errors;
- small refactor within architecture;
- adding non-breaking validation;
- updating docs to match approved behavior;
- retrying failed CI;
- fixing bug inside task scope;
- merging to `develop` after all gates pass.

## 3. Approval required

### Architecture
- new framework/language;
- database replacement;
- message broker change;
- microservice split;
- major schema redesign.

### Cost
- new paid external provider;
- material recurring infrastructure increase;
- enabling high-cost model by default.

### Security/privacy
- auth model change;
- data-retention change;
- new public exposure of personal/contact data;
- weakening controls.

### Destructive operations
- dropping production table/column with data;
- bulk delete;
- irreversible migration;
- credential rotation with downtime risk.

### Production
- first production deployment;
- release with known major risk;
- rollback involving data restoration;
- production environment topology change.

## 4. Approval request format

Agent must present:

```text
Decision:
Why needed:
Options:
Recommended option:
Risk:
Cost impact:
Data impact:
Rollback:
What happens if declined:
```

Avoid dumping raw implementation detail unless needed.

## 5. Approval persistence

Approved decisions must be recorded in:
- `.ai/DECISIONS.md`;
- task record;
- ADR when architectural.

Do not rely only on conversational approval.
