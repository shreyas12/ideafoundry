# Template — 01-product-requirements.md

<!-- token-budget: <=3K output -->
<!-- requires: [pm] -->
<!-- loads: [meta, brief, goals, product, ux] -->
<!-- eager: no -->

The PRD. Slot-fill from `product.json` (+ `brief` for goals/users/metrics). **UX sections are gated on the UX specialist being in the roster** — if `ux.json` is absent, omit *User flows* and the *Experience notes* per feature entirely (do not stub). Cite Brief IDs; never restate Brief prose.

---

## Render shape

```markdown
# <brief.vision title> — Product Requirements

**Goal.** <brief.vision>  ·  **Success =** <for s in brief.success_metrics: <s.metric> → <s.target>>

## Users
<for u in brief.target_users: - **<u.label>** (<u.sophistication>) — <u.description>>

## Features
<for f in product.features (mvp first, then next/later):>
### <f.id> · <f.name>  [<f.priority>]
- **Story:** <f.user_story>
- **Serves:** <f.serves>
- **User flow:** <if ux present: ux.primary_flows[feature==f.id].steps>   <!-- omit this line entirely if UX absent -->
<end for>

## MVP boundary
**In:** <product.mvp.included names>
**Out (deferred):** <product.mvp.deferred names> — <product.mvp.cut_rationale>
**Non-goals:** <brief.non_goals texts>

## Open questions
<for gap in product.gaps_to_clarify + brief.gaps_to_clarify: - <gap.text> (blocks: <gap.blocks>)>
<if none: "None outstanding.">
```

## Rules
- **UX gating:** the *User flow* line and any experience detail render **only** if `ux.json` was loaded (UX in roster). Absent → omit the line, no "N/A". This is the F-040 graceful-degradation contract.
- Group features MVP → Next → Later using `f.priority`; the MVP boundary section makes the cut explicit.
- Cite `brief.*` IDs for goals/users/metrics; do not paste Brief text.
- ≤3K — per-feature detail stays terse; acceptance detail lives in `12`/`08`.
