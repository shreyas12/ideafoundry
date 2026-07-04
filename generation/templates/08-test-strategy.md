# Template — 08-test-strategy.md

<!-- token-budget: <=3K output -->
<!-- requires: [qa] -->
<!-- loads: [meta, qa, product] -->
<!-- eager: no -->

The test strategy. **Rendered only when QA is in the roster.** Slot-fill from `qa.json` (+ `product` to name the features acceptance skeletons cover). Proportionality is the point — a weekend hack renders a short acceptance-level doc, not a full pyramid. Dropped if QA absent.

---

## Render shape

```markdown
# <brief.vision title> — Test Strategy

**Approach.** <qa.summary>
**Levels.** <qa.test_strategy.levels> — <qa.test_strategy.rationale>

## Acceptance criteria (by feature)
<for ac in qa.acceptance_skeletons:>
### <ac.id> · covers <ac.feature> (→ product.features[ac.feature].name)
- **Given** <ac.given>
- **When** <ac.when>
- **Then** <ac.then>
<end for>

## Edge cases
<for ec in qa.edge_cases: - **<ec.case>** → expected: <ec.expected> (serves <ec.serves>)>

## Release risks & smoke checks
<for rr in qa.release_risks: - **<rr.risk>** — smoke-check before every ship: <rr.smoke_check>>
```

## Rules
- **Every acceptance skeleton maps to a real `product.features.*` id** (via `ac.feature`). A skeleton referencing an unknown feature → `⚠ acceptance references unknown feature`, not a silent render.
- **Proportionality:** render exactly the `qa.test_strategy.levels` QA chose — do not upgrade a weekend hack to a full test pyramid because the template *could* hold one.
- The edge cases should include the riskiest integration the Engineer flagged (QA already pulled it in via dep-summary); render it prominently.
- ≤3K.
