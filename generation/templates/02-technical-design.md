# Template — 02-technical-design.md

<!-- token-budget: <=3K output -->
<!-- requires: [engineer] -->
<!-- loads: [meta, brief, architecture, decisions] -->
<!-- eager: no -->

The engineering design doc. Slot-fill from `architecture.json` (+ `decisions` for any resolved architectural conflicts). If Engineer is absent from the roster this template is **dropped entirely** by the generator (README marks it `not in roster`) — it never renders half-built.

---

## Render shape

```markdown
# <brief.vision title> — Technical Design

**Approach.** <architecture.approach>

## Stack
<for k, v in architecture.stack: - **<k>:** <v>>
_Chosen for the simplest option satisfying the Brief. Deviations are justified below._

## System shape
<architecture.summary — one line: process model + storage + scheduler>

## API surface (overview)
<for e in architecture.api_surface: - `<e.method> <e.path>` — <e.purpose> (serves <e.serves>)>
_Full contract: `03-api-design.md`._

## Data model (overview)
<for d in architecture.data_schema: - **<d.entity>** — key: <d.key_fields> — <d.notes>>
_Full schema: `04-database-schema.md`._

## Complexity decisions
<for cj in architecture.complexity_justification: - **<cj.recommendation>** — needed because <cj.why_needed>; simpler <cj.simpler_alternative_considered> rejected: <cj.why_rejected>>
<if none: "No ceiling-exceeding choices — defaults throughout (SQLite/single-instance/library-auth/cron).">
<for sc in decisions.simplification_candidates (if any): "⚠ Flagged by Consensus Simplifier: <sc.recommendation> — <sc.reason_flagged>">

## Engineering risks
<for er in architecture.engineering_risks: - **<er.risk>** — <er.mitigation> (serves <er.serves>)>
```

## Rules
- **Drop-not-degrade:** rendered only when `engineer` ∈ roster (schema-level `requires`). No engineer → template absent, no broken `architecture.*` refs anywhere.
- Overview-only for API/schema — the deep docs are `03`/`04`. Don't duplicate; link.
- Surface `decisions.simplification_candidates` here — this is where an over-engineered choice that Consensus flagged becomes visible to the reader.
- ≤3K.
