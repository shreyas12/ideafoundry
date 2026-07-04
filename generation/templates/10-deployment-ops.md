# Template — 10-deployment-ops.md

<!-- token-budget: <=3K output -->
<!-- requires: [engineer] -->
<!-- loads: [meta, brief, architecture, security] -->
<!-- eager: no -->

How this gets deployed and run. Slot-fill from `architecture.json` (hosting/stack) — **secrets & hardening sections are gated on Security being in the roster**; if `security.json` is absent, render the deployment mechanics and omit the security-hardening subsection (no stub). Dropped whole if Engineer absent.

---

## Render shape

```markdown
# <brief.vision title> — Deployment & Ops

**Target.** <architecture.stack.hosting>  ·  **Runtime:** <architecture.stack.runtime>  ·  **Store:** <architecture.stack.db>

## Deploy shape
<derive from architecture.summary + stack: single service / container / serverless — one paragraph, matched to the profile ceiling>
- **Build/release:** <simplest mechanism satisfying the Brief — e.g. push-to-deploy, single Docker image, cron via platform scheduler>
- **Environments:** <dev + prod at minimum; more only if the Brief/profile warrants>

## Configuration & secrets
<!-- if security.json present: -->
- **Secrets:** <security.secrets>
- **Hardening:** <security.data_protection.at_rest / in_transit / tenant_isolation as applicable>
<!-- if security.json absent: render one line — "Secrets via platform env vars / library defaults; no dedicated Security review in this roster." -->

## Runbook basics
- **Scheduled work:** <architecture.stack.scheduler> — <what runs on it>
- **Backup/restore:** <proportionate to db choice — SQLite file copy vs managed snapshots>
- **Scaling posture:** <single-instance default unless architecture.complexity_justification says otherwise>
```

## Rules
- **Proportionality first:** default to single-instance, managed-hosting, platform-scheduler ops. Only describe autoscaling/orchestration if `architecture.complexity_justification` justified it against a Brief constraint.
- **Security gating:** the *Configuration & secrets* hardening detail comes from `security.json`. Absent Security → render the one-line library-default fallback, never a "N/A" stub and never a broken `security.*` reference.
- ≤3K.
