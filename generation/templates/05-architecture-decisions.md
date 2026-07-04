# Template — 05-architecture-decisions.md

<!-- token-budget: <=3K output -->
<!-- requires: [engineer] -->
<!-- loads: [meta, architecture, decisions] -->
<!-- eager: no -->

An ADR log — the *why* behind the design, so a future maintainer (or amendment) understands what was chosen and what was rejected. Slot-fill from `architecture.complexity_justification` + `decisions.resolved` + `decisions.simplification_candidates`. Dropped if Engineer absent.

---

## Render shape

```markdown
# <brief.vision title> — Architecture Decisions

## ADR-1 · Overall approach
- **Decision:** <architecture.approach, condensed>
- **Context:** cites <architecture.traces_to Brief IDs>
- **Consequences:** <architecture.summary — the riskiest unknown>

<for cj in architecture.complexity_justification (one ADR each):>
## ADR-<n> · <cj.recommendation>
- **Decision:** adopt <cj.recommendation>
- **Why needed:** <cj.why_needed> (Brief-grounded)
- **Rejected:** <cj.simpler_alternative_considered> — <cj.why_rejected>
- **Status:** <if this appears in decisions.simplification_candidates → "⚠ FLAGGED by Consensus: <reason_flagged> — user review pending"; else "accepted">
<end for>

## Decisions resolved by Consensus
<for d in decisions.resolved (architectural ones): - **<d.decision>** — <d.rationale> (by <d.by>)>

## Default choices (no ADR needed)
<one line: "Everything not listed above is the simplest option satisfying the Brief — SQLite/single-instance/library-auth/cron per the profile ceiling.">
```

## Rules
- **One ADR per `complexity_justification` entry** — this is the doc that proves every ceiling-exceeding choice was justified against a Brief constraint, not "best practices".
- **Mark flagged decisions loudly.** If a `complexity_justification` also appears in `decisions.simplification_candidates`, its ADR carries the ⚠ FLAGGED status — the reader must see that Consensus wasn't convinced.
- Don't write ADRs for default choices; one summary line covers them.
- ≤3K.
