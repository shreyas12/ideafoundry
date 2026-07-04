# Template — 11-observability.md

<!-- token-budget: <=3K output -->
<!-- requires: [engineer] -->
<!-- loads: [meta, brief, architecture, qa] -->
<!-- eager: no -->

What to log, measure, and alert on. Slot-fill from `architecture` (the failure surfaces) + `brief.success_metrics` (what to instrument) — **the SLO/acceptance-signal section is gated on QA being in the roster** (`qa.release_risks` supply the smoke signals). Dropped whole if Engineer absent.

---

## Render shape

```markdown
# <brief.vision title> — Observability

**What "healthy" means.** tie to <brief.success_metrics: <s.metric> → <s.target>> — instrument the metric, not vanity counters.

## Signals to capture
- **Logs:** <the events that matter for the primary flow + the riskiest integration (architecture.engineering_risks)>
- **Metrics:** <for s in brief.success_metrics: a counter/gauge that measures s.metric>
- **Traces:** <only if architecture is multi-hop; single-service → skip, say so>

## Alerts
<derive from architecture.engineering_risks — alert on the riskiest unknown failing, not on everything>
- **<risk>** → alert when <condition>

## Release / regression signals
<!-- if qa.json present: -->
<for rr in qa.release_risks: - **<rr.risk>** — monitor via <rr.smoke_check> post-deploy>
<!-- if qa.json absent: one line — "No QA in this roster; smoke-check the primary flow manually after each deploy." -->
```

## Rules
- **Instrument the Brief's success metrics** — observability that doesn't measure `brief.success_metrics` is theatre. Anchor every metric to a metric ID.
- **Proportionality:** a single-instance weekend hack gets logs + one health metric, not distributed tracing. Say "traces: not needed at this scale" rather than inventing an APM stack.
- **QA gating:** the *Release/regression signals* section uses `qa.release_risks` when QA ∈ roster; absent → the one-line manual-smoke fallback, no broken `qa.*` ref.
- ≤3K.
