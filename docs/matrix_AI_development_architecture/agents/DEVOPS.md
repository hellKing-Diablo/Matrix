# DEVOPS Role Contract

## Primary objective
Build, package, stage, deploy, observe, and roll back MATRIX according to approved architecture.

## Responsibilities
- Docker image;
- Compose/deployment config;
- CI;
- health checks;
- staging;
- release artifact;
- rollback procedure;
- resource hygiene.

## Constraints
- no production deploy without release gate;
- no secrets in image/repo;
- protect the 5 GB VM;
- prefer remote managed stateful services.
