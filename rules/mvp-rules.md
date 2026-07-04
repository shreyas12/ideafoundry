# MVP Rules — force a real scope cut

<!-- token-budget: <=0.8K -->
<!-- Referenced by the PM specialist (and by Consensus when checking the MVP boundary). General planning discipline lives in planning-rules.md. -->

The most common planning failure is "everything is MVP." These rules force a genuine cut.

## 1. The MVP is the core loop, not the feature list
Find the **single loop** a user must complete for the product to have delivered its value once (e.g. *capture standup → detect blocker → surface it*). The MVP is that loop plus only what the loop cannot run without. Everything else is roadmap.

## 2. `deferred` must be non-empty
`product.mvp.deferred` is **required to be non-empty** unless the Brief is already a single-feature idea. If you cannot name one thing to cut, you have not found the core loop — try again. A pass shows features **explicitly moved to a later roadmap phase**, not silently dropped.

## 3. Every cut cites a Brief constraint
`cut_rationale` ties each deferral to a real constraint — `brief.timeline.t1` (won't fit the horizon), `brief.constraints.c1` (solo dev), `brief.non_goals.ng1` (out of scope by declaration). "Nice to have later" is not a rationale; a Brief-grounded reason is.

## 4. Don't gold-plate the MVP
No analytics dashboards, admin panels, multi-tenant settings, or configurability in the MVP unless a `goal` or `success_metric` *requires* them. These are the classic scope creep that turns a 2-week hack into a 2-month build.

## 5. The MVP must be shippable and measurable
The MVP has to move at least one `brief.success_metrics` entry. If the cut leaves nothing measurable, it's cut too deep. The boundary is: smallest thing that both **runs the core loop** and **moves a success metric**.

## 6. Consistency across artifacts
`product.mvp.included` is the single source: `12-developer-tickets.md` (backlog), `09-roadmap.md` (MVP phase), and `PLAN_SUMMARY.md` (feature list) all derive from it. They must agree — if they don't, the MVP boundary wasn't set cleanly.
