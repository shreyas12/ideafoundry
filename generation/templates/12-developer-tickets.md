# Template — 12-developer-tickets.md

<!-- token-budget: <=3K output -->
<!-- requires: [pm] -->
<!-- loads: [meta, goals, product, decisions] -->
<!-- eager: yes — always rendered on the initial run -->

The doc an engineer (or a coding assistant) opens first. Turn `product.mvp.included` into **small, executable tickets**, each carrying a required `traces_to` a goal ID. Slot-fill from `product.json` + `decisions.json` — **no synthesis, no re-reading specialist reasoning**. Respect Consensus: if `decisions.resolved` trimmed a feature to roadmap, it is **not** an MVP ticket here.

---

## Render shape

```markdown
# <brief.vision title> — Developer Tickets (MVP)

> Every ticket traces to a business goal. Build order top-to-bottom. Profile: <meta.profile>.

## MVP backlog
<for f in product.mvp.included → product.features[f], in build order:>
### T-<nn> · <f.name>
<f.user_story>
- **Acceptance:** <derive 1–3 checkable criteria from the feature + any qa.acceptance_skeletons[feature==f] if qa present>
- **Size:** <S|M|L, inferred from scope>
- **Traces to:** <f.serves>   ← required; a ticket with no goal ID is a defect
- **Depends on:** <earlier T-ids or "none">
<end for>

## Deferred (not MVP — do not build yet)
<for f in product.mvp.deferred: - <f.name> → <roadmap phase from product.roadmap> — <product.mvp.cut_rationale ref>>

## Decisions that shaped this backlog
<for d in decisions.resolved: - <d.decision> — <d.rationale>>
<if decisions.escalations non-empty: "⚠ Open: <es.question> — backlog may shift once decided.">
```

## Rules
- **`traces_to` is mandatory on every ticket.** Every ticket's `serves`/`traces_to` must resolve to a real `goals.*` / `brief.goals.*` ID. If a feature has no goal link, that is a PM defect — surface it as `⚠ untraced` rather than inventing a goal.
- **Small enough to execute.** One feature → one ticket unless the feature obviously splits (then T-4a/T-4b). No epic-sized tickets; push detail into acceptance criteria.
- **Honor Consensus.** Only `product.mvp.included` become MVP tickets. Anything Consensus moved to roadmap goes in *Deferred*, never in the backlog.
- **Acceptance criteria** reuse `qa.acceptance_skeletons` when QA is in the roster (match on `feature` id); otherwise derive 1–3 checkable lines from the user story. Never stub "TBD".
- **≤3K.** If MVP is large, keep ticket bodies terse and point deep detail at `01-product-requirements.md`.
