# Traceability — one graph, two uses

<!-- token-budget: <=1.2K -->
<!-- Loaded by Consensus (challenge-accept) and by Amendment (staleness walk). Not loaded on the happy generation path. -->

Every artifact connects back to the originating business goal. The **same graph** powers explainability (why does this ticket exist?) and staleness (what does this change invalidate?).

## The graph
```
Business Goal (brief.goals.g*)
  → Feature (product.features.f*, via feature.serves = goal id)
    → Epic/Story (product user_story, roadmap phase)
      → Ticket (12-*, via ticket.traces_to = goal id)
        → Acceptance (qa.acceptance_skeletons, via ac.feature = feature id)
```
Cross-links: specialist outputs carry `traces_to` = the Brief IDs they derive from. UX flows link `product.features`; Security threats/challenges link `brief.assumptions`/`brief.constraints`; docs link the planning files in their `loads:`.

## Forward walk (explainability)
Given a goal, follow edges **forward** to see everything built to serve it. Used when a reader asks "why is this here?" — every artifact answers with its `traces_to`/`serves` chain.

## Backward walk (staleness) — the Amendment engine
Given a **changed Brief ID** (from an amendment or an accepted challenge), follow edges **backward** to find everything downstream that must be re-reviewed:

1. **Direct outputs:** every `planning/<role>.json` whose `traces_to` contains the changed ID → mark `stale: true`.
2. **Transitive outputs:** any specialist whose *dependency summary* came from a now-stale specialist, **if** the changed area touches the depended-on content (e.g. Engineer stale on a storage change → QA that tested that path is stale; Security that reviewed unrelated auth is **not**).
3. **Derived docs:** every template whose `loads:` includes a stale planning file → mark the doc `stale` in `README.md` (regenerate lazily on next `render`, never eagerly).

## Precision rules (avoid over-marking)
- **Field-level, not file-level, where possible.** A change to `brief.constraints.c2` (rate limit) invalidates the batching architecture, not the whole product plan. Mark only outputs whose `traces_to` actually contains the changed ID or transitively depend on it.
- **Don't mark what didn't move.** If `security.json` never traced to the changed ID, it stays `available` and byte-identical. Over-marking turns an amendment into a rerun — an eval failure (EVAL 4).
- **Append, never renumber.** Changed Brief sections get **new** IDs; superseded IDs are tagged `stale: true`, not deleted or reused — the graph's stability is what makes the backward walk correct across many amendments.

## Output of a walk
A staleness set: `{stale_outputs: [architecture, product], rerun: [engineer, pm], stale_docs: [02, 04, 01, 09]}`. Amendment consumes this directly (see `amendment.md`).
