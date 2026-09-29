# AGENTS.md — Common Operating Contract

Every autonomous agent working on MATRIX must follow this file.

## 1. Mission

Build MATRIX according to the approved product architecture with minimal human intervention while preserving correctness, security, auditability, and recoverability.

## 2. Required reading before work

Every agent must read:
- product architecture `README.md`;
- product architecture decisions;
- this file;
- its own role file under `agents/`;
- the assigned task record in `.ai/TASKS.json`;
- relevant architecture documents for the task.

## 3. Never do these without human approval

- change primary language/framework;
- change PostgreSQL to another canonical database;
- introduce or replace a message broker;
- split the modular monolith into microservices;
- add a new paid provider or materially increase recurring cost;
- perform destructive production data operations;
- weaken authentication/security requirements;
- expose a new public production endpoint not in architecture;
- change data-retention policy materially;
- deploy to production unless the approval policy explicitly allows it;
- commit secrets;
- rewrite large unrelated areas "for cleanliness";
- bypass failing required tests.

## 4. Task discipline

Agents work only on explicit task scope.

Before coding, the assigned implementation agent must record:
- task goal;
- dependencies;
- files expected to change;
- tests to add/update;
- architecture sections relied upon;
- risks.

If the task is too broad, return it to the Orchestrator for decomposition.

## 5. Definition of done

A code task is done only when:
- acceptance criteria pass;
- required tests pass;
- lint passes;
- type checks pass where configured;
- migrations are included if schema changed;
- docs are updated if contracts changed;
- security checks pass;
- reviewer approval is recorded;
- task state is persisted.

## 6. No self-approval

The material implementation agent cannot be the sole final reviewer.

A different logical role must perform review.

## 7. Git rules

- never develop directly on `main`;
- use task branches or lightweight worktrees;
- branch format: `agent/<task-id>-<short-name>`;
- commits must be scoped to the task;
- do not mix unrelated refactors;
- merge only after required test/review gates.

## 8. Secrets

Never:
- place secrets in source code;
- echo secrets in logs;
- store live keys in Markdown;
- commit `.env`;
- paste tokens into task state.

Use secret references or environment-variable names.

## 9. External services

Provider calls must:
- respect product provider interfaces;
- have explicit timeouts;
- classify transient/permanent failures;
- avoid paid/live calls in ordinary CI where fakes suffice.

## 10. Resource limits

The AI VM is disk constrained.

Agents must:
- avoid local PostgreSQL unless explicitly authorized;
- avoid downloading large model weights;
- avoid duplicate virtual environments;
- keep Docker caches bounded;
- clean temporary files after tasks;
- stop large operations if free disk enters the critical threshold defined in `08_RESOURCE_GUARDRAILS.md`.

## 11. Ambiguity policy

If ambiguity affects only implementation detail:
- choose the simplest option compatible with architecture;
- document it.

If ambiguity affects architecture, security, data integrity, recurring cost, or production behavior:
- create an ADR proposal;
- mark task blocked on decision;
- continue unrelated safe work.

## 12. State persistence

Important progress must be written to:
- `.ai/TASKS.json`;
- `.ai/PROJECT_STATE.md`;
- relevant status files;
- Git.

Do not rely solely on chat/session memory.

## 13. Error handling

Never hide errors merely to make tests green.

For unexpected failures:
- preserve evidence;
- update task/blocker state;
- provide a reproducible failure description;
- route to the Orchestrator.

## 14. Architecture protection

When implementation appears to require architecture change:
- do not silently change architecture;
- draft ADR;
- show exact reason, alternatives, tradeoffs, migration impact;
- await approval when required.
