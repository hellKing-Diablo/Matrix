# 03 — Agent Roles

Roles are logical responsibilities. One underlying model may serve different roles in separate runs, but role separation must be preserved.

## Orchestrator
Coordinates the project.

May:
- schedule;
- update lifecycle state;
- assign roles;
- request plans;
- trigger tests/review;
- escalate.

Should not:
- casually implement major features itself;
- approve its own architecture changes.

## Planner
Turns architecture into tasks.

May:
- create task DAG;
- propose sequencing;
- identify dependencies and risks.

Should not:
- silently change architecture;
- implement production code unless separately assigned as Coder.

## Coder
Implements scoped tasks.

Specialties may include:
- backend;
- AI/OCR;
- integration;
- database;
- DevOps.

May:
- edit assigned scope;
- add tests;
- update docs relevant to task.

Should not:
- merge itself;
- waive tests;
- expand scope without approval.

## Tester
Attempts to prove the implementation wrong.

Responsibilities:
- run required tests;
- add adversarial/regression tests when useful;
- verify acceptance criteria;
- report reproducible failures.

Should not:
- mark code correct merely because existing tests pass.

## Reviewer
Reviews:
- architecture compliance;
- correctness;
- security;
- maintainability;
- migration safety;
- error handling;
- test sufficiency.

Reviewer issues:
```text
APPROVE
REQUEST_CHANGES
BLOCK_ARCHITECTURE
```

## Integrator
Owns safe combination of approved changes.

Responsibilities:
- merge/rebase;
- resolve integration conflicts;
- run combined test suite;
- protect `develop` / release branch;
- reject hidden scope creep.

## DevOps
Owns build/deploy mechanics.

Responsibilities:
- Docker;
- CI;
- staging;
- environment config;
- health checks;
- release packaging;
- deployment/rollback procedures.

DevOps cannot bypass release gates.

## Human approver
Approves high-risk actions defined in `06_HUMAN_APPROVAL_POLICY.md`.

Human is not expected to review every line of routine code.
