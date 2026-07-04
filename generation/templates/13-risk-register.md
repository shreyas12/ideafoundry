# Template — 13-risk-register.md

<!-- token-budget: <=3K output -->
<!-- requires: [pm] -->
<!-- loads: [meta, product, architecture, ux, security, qa, decisions] -->
<!-- eager: no -->

The consolidated risk register — every risk any specialist named, in one ranked table. Slot-fill by **aggregating the risk fields across whichever planning files are present**. Each of `architecture`/`ux`/`security`/`qa` is optional: iterate only the files the generator actually loaded (roster gating). Always available (PM is in every roster; PM risks alone populate it).

---

## Render shape

```markdown
# <brief.vision title> — Risk Register

> Aggregated across the active roster. Ranked by severity, then by whether a mitigation exists.

| # | Risk | Source | Severity | Mitigation | Serves |
|---|---|---|---|---|---|
<for pr in product.product_risks: | | <pr.risk> | PM | <sev> | <pr.mitigation> | <pr.serves> |>
<for er in architecture.engineering_risks (if present): | | <er.risk> | Engineer | <sev> | <er.mitigation> | <er.serves> |>
<for ur in ux.ux_risks (if present): | | <ur.risk> | UX | <sev> | <ur.mitigation> | — |>
<for sr in security.security_risks (if present): | | <sr.risk> | Security | <sev> | <sr.mitigation> | — |>
<for th in security.threats (if present): | | <th.threat> | Security(threat) | <th.severity> | <th.mitigation> | — |>
<for rr in qa.release_risks (if present): | | <rr.risk> | QA | <sev> | smoke: <rr.smoke_check> | — |>
<!-- number rows after sorting by severity desc -->

## Unresolved decisions carrying risk
<for es in decisions.escalations: - **<es.question>** — until decided, <the risk of guessing wrong>>
<for u in decisions.unresolved: - <u> (documented, not resolved after 3 Consensus rounds)>
```

## Rules
- **Optional-source aggregation is the whole point:** iterate a specialist's risk field **only if** its planning file was loaded. A Weekend Hack register has PM + Engineer rows only — and that is correct, not incomplete. Never emit a row from an absent file, never a broken `security.*`/`ux.*` reference.
- Rank by severity (assign severity from the source where explicit, else infer high/med/low), then number the rows.
- Fold Consensus `escalations`/`unresolved` in as decision-risk — an open escalation is a live risk until the user decides.
- ≤3K.
