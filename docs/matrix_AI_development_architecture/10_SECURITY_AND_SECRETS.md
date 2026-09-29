# 10 — Security and Secrets for Autonomous Development

## 1. Secret classes

Examples:
- OpenAI key;
- Google service/OAuth credentials;
- Meta access token/app secret;
- database URL/password;
- object-storage keys;
- deployment tokens.

## 2. Storage

Use:
- environment variables;
- CI secret store;
- managed secret manager where available.

Never store live values in:
- Markdown;
- task JSON;
- commit messages;
- logs;
- issue titles;
- screenshots.

## 3. Agent output hygiene

When reporting configuration:
- name environment variable;
- do not print secret value;
- redact tokens from command output.

## 4. Commands

Agents must avoid commands likely to expose full environment/secrets unless necessary.

If diagnostic output contains secrets:
- do not persist it;
- redact before logging/reporting.

## 5. Dependency policy

New dependencies should:
- have a clear purpose;
- be reasonably maintained;
- not duplicate existing stack;
- be pinned/locked according to project tooling.

Major dependency additions require Reviewer attention.

## 6. Supply chain

CI should eventually include:
- dependency audit;
- secret scanning;
- container vulnerability scan when practical.

These are release hardening gates, not a reason to block initial repository bootstrap if tooling is unavailable.
