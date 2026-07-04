# DeployGate — Developer Tickets (MVP)

> Every ticket traces to a business goal. Build order top-to-bottom. Profile: Internal Tool.

## MVP backlog

### T-01 · Spike the deploy pipeline trigger
Before building on it, confirm the existing deploy pipeline exposes a callable, authenticated trigger (brief.assumptions.a2 — the riskiest unknown).
- **Acceptance:** a scripted authenticated call triggers a no-op deploy in staging; if it can't, escalate before T-05.
- **Size:** S
- **Traces to:** g1
- **Depends on:** none

### T-02 · Auth + SSO session
Wire GitHub OAuth via the existing SSO gateway; establish an authenticated session. Identity only — no authorization decisions here.
- **Acceptance:** an SSO login yields a session carrying the user's GitHub identity + team memberships.
- **Size:** M
- **Traces to:** g1
- **Depends on:** none

### T-03 · Data model + append-only audit
Create `deploy_request`, `approval`, `audit_event`. Revoke UPDATE/DELETE on `audit_event` at the DB grant so the app has no path to mutate it.
- **Acceptance:** schema migrates; an attempt to UPDATE/DELETE an audit_event is rejected by the DB, not just the app.
- **Size:** M
- **Traces to:** g2
- **Depends on:** none

### T-04 · Request a deploy (f1)
One-screen form: service + target env → creates a `deploy_request` (status pending) + an audit event.
- **Acceptance:** an engineer submits a request; it appears as pending; an audit event records the creation.
- **Size:** M
- **Traces to:** g1
- **Depends on:** T-02, T-03

### T-05 · Approve / reject with separation of duties (f2)
A lead in the service's approver allowlist approves/rejects with a reason. **Enforce requester ≠ approver and the approver-role check server-side.** On approval, call the pipeline trigger from T-01.
- **Acceptance:** a non-approver is refused; the requester cannot approve their own request; an approval triggers the pipeline and writes an audit event.
- **Size:** L
- **Traces to:** g1
- **Depends on:** T-01, T-04
- **Note:** allowlist source is pending decision es1 — build against an interface so either source drops in.

### T-06 · Audit trail view (f3)
A read-only, filterable list of requests + decisions for incident review.
- **Acceptance:** a lead can find every decision for a service over a date range; each row shows requester, approver, decision, reason, timestamp.
- **Size:** M
- **Traces to:** g2
- **Depends on:** T-03, T-05

## Deferred (not MVP — do not build yet)
- **Notifications** → Next — improves s2 but the loop ships without it (product.mvp.cut_rationale)
- **Per-service approver policies** → Later — configurability the MVP doesn't need

## Decisions that shaped this backlog
- **f2 enforces separation of duties (requester ≠ approver, approver allowlist)** — required by g1; an approval the requester can self-grant is not an approval.
- ⚠ Open: **where the approver allowlist comes from (es1)** — T-05 builds against an interface so the decision can drop in without rework.
