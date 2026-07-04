# Template — 09-roadmap.md

<!-- token-budget: <=3K output -->
<!-- requires: [pm] -->
<!-- loads: [meta, brief, product, decisions] -->
<!-- eager: no -->

The phased roadmap. Slot-fill from `product.roadmap` (+ `product.mvp` and `decisions.resolved` for anything Consensus moved between phases). Shows the MVP → Next → Later progression and *why* deferred work waits. Always available (PM is in every roster).

---

## Render shape

```markdown
# <brief.vision title> — Roadmap

**Horizon.** <brief.timeline.horizon>  <if brief.timeline.hard_deadline: · hard deadline <date>>

<for phase in product.roadmap:>
## <phase.phase>
<if phase.outcome: **Outcome:** <phase.outcome>>
<for fid in phase.features → product.features[fid]: - **<f.name>** — <one line> (serves <f.serves>)>
<end for>

## Why deferred work waits
<product.mvp.cut_rationale>
<for d in decisions.resolved where a feature moved phase: - <d.decision> — <d.rationale>>

## Sequencing risks
<pull product_risks / engineering_risks that threaten the phase order — e.g. "Next depends on integration X, the riskiest unknown">
```

## Rules
- Phases come straight from `product.roadmap`; features render by resolving their ids against `product.features`.
- **Honor Consensus movements:** if `decisions.resolved` shifted a feature MVP→Next, it renders in Next here, and the *why deferred* section cites that decision — the roadmap must not contradict the tickets.
- The MVP phase should match `12-developer-tickets.md`'s backlog exactly (same feature set) — both derive from `product.mvp.included`.
- ≤3K.
