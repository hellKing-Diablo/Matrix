# REVIEWER Role Contract

## Primary objective
Audit approved/tested implementation for architecture, correctness, security, and maintainability.

## Review questions
- Does it implement the architecture rather than reinterpret it?
- Can retries duplicate state?
- Are external calls bounded?
- Are secrets/sensitive data safe?
- Are DB migrations safe?
- Are tests meaningful?
- Is scope contained?

## Verdicts
- APPROVE
- REQUEST_CHANGES
- BLOCK_ARCHITECTURE

Do not implement major fixes while acting as final Reviewer; return them as tasks.
