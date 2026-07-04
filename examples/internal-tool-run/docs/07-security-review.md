# DeployGate — Security Review

**Crown-jewel risk.** Integrity: only the right people approve, and the audit trail cannot be forged. The Brief's biggest gap is conflating SSO authentication with authorization — SSO proves identity, it does not decide who may approve, and as written nothing stops an engineer approving their own deploy.

## Threat model
- **[high] An engineer approves their own deploy request, defeating the control** — enforce requester ≠ approver server-side, plus an explicit approver-role check.
- **[high] Audit records are altered or deleted to hide who authorized a release** — append-only `audit_event` with UPDATE/DELETE revoked at the DB grant; no app path to mutate.
- **[medium] Any authenticated SSO user can call the approve endpoint** — authorize on the lead role, not merely a valid session.

## Authentication & authorization
- **AuthN:** GitHub OAuth via the existing SSO gateway (brief.constraints.c3). Identity only — never treated as authorization.
- **AuthZ boundary:** Role-based. An authenticated user may request; only a user in the service's approver allowlist may approve/reject; a request's own requester may never approve it (separation of duties).

## Secrets & data protection
- **Secrets:** the deploy-pipeline API token lives in the platform secret store / env — never in the DB or the repo; rotated on the platform schedule.
- **At rest:** Postgres on the internal platform's encrypted volume · **In transit:** TLS terminated at the SSO gateway.
- **Tenant isolation:** single-tenant internal tool — not applicable.

<!-- Compliance section omitted: this is an internal, non-regulated tool (no security.compliance in planning). Per the template contract, the section is dropped entirely rather than stubbed "N/A". -->

## Challenges to the Brief
- **[high]** on brief.assumptions.a1: the Brief assumes GitHub SSO is sufficient for access control, but SSO authenticates identity and does not authorize approval — as written, any engineer could approve any deploy, including their own, defeating g1. → Add an explicit approver allowlist (sourced from GitHub team membership) and enforce requester ≠ approver server-side. *(Surfaced to the user as escalation es1; decision pending.)*

## Security risks
- **Approver allowlist drifts out of date as people change teams** — source the allowlist from GitHub team membership rather than a hand-maintained list.
