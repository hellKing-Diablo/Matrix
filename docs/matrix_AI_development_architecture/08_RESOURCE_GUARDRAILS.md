# 08 — Resource Guardrails for the Constrained AI VM

## 1. Constraint

The AI-development VM has approximately 5 GB maximum disk allocation available for this project environment.

The architecture assumes this is a **thin development/orchestration node**, not the permanent data plane.

## 2. Must remain remote

Do not persist locally:
- production PostgreSQL data;
- business-card image archive;
- backups;
- large AI model weights;
- large Docker image exports.

Prefer:
- managed PostgreSQL;
- remote object storage;
- API-based OCR/LLM providers.

## 3. Disk thresholds

Thresholds are based on **free disk remaining**, not total project size.

Recommended defaults:

- **Healthy:** > 1.5 GB free
- **Warning:** 750 MB–1.5 GB free
- **Critical:** < 750 MB free

These are configuration defaults, not immutable constants.

## 4. Behavior by threshold

### Healthy
Normal work allowed.

### Warning
Before heavy operation:
- prune safe build cache;
- remove expired temp files;
- remove merged worktrees;
- rotate/compress logs;
- avoid unnecessary Docker rebuilds.

### Critical
Do not:
- start Docker builds;
- install large dependency sets;
- create new worktrees;
- download large artifacts.

Allowed:
- state repair;
- safe cleanup;
- lightweight Git operations;
- notify/escalate if cleanup cannot restore headroom.

## 5. Shared environments

Avoid:
```text
agent1/.venv
agent2/.venv
agent3/.venv
```

Prefer:
- one project virtual environment where safe;
- shared package/download cache with bounds;
- task worktrees sharing the same Git object database.

## 6. Docker hygiene

Agents/DevOps must:
- use slim images;
- use `.dockerignore`;
- avoid copying `.git` into image;
- prune dangling build cache after release/failed experiments;
- not run local Postgres by default;
- not retain old unused image versions indefinitely.

## 7. Temporary file policy

Temporary media/build artifacts:
- stored under known temp directory;
- linked to task/run id;
- deleted on success;
- cleanup attempted on failure;
- never treated as canonical data.

## 8. Resource status update

Before any heavy build or multi-agent parallel phase, write/update `.ai/RESOURCE_STATUS.md` with:
- free disk;
- active worktrees;
- relevant Docker usage;
- notable temp/cache usage;
- action taken if warning/critical.
