# EVAL 4 — Amendment + budget gate

Fixture: [`fixtures/eval-4-amendment.json`](fixtures/eval-4-amendment.json) · Traces: EVAL.md §4, PLAN §18

**Prompt.** `/ideafoundry amend "We just learned we need to support offline mode."` — starting from **EVAL 2's completed Consumer App run**.

## How to run
1. Complete EVAL 2 first. **Snapshot** its `planning/` folder (this is the `--baseline`).
2. Run the amend command; save the post-amendment `planning/` + a `tokens.json` recording amendment cost.
3. `python3 evals/check.py --fixture evals/fixtures/eval-4-amendment.json --planning <post>/planning --baseline <eval2-snapshot>/planning --tokens <post>/tokens.json`

## Expected behavior
1. Writes `planning/amendments/001-offline-mode.json` (note + timestamp + `invalidates`/`rerun`/`stale_docs`).
2. Backward traceability walk marks **2–3 specialist outputs stale** — offline touches `architecture.json` (sync/storage), `product.json` (offline caching feature + roadmap), possibly `ux.json` (offline states). Security untouched.
3. **PM + Engineer rerun** (UX may rerun if offline flows are affected) against the amended Brief.
4. **4–5 docs marked stale in README** (`02`, `04`, `01`, `09`, maybe `06`) — **not eagerly regenerated**; they regenerate on next read.
5. Untouched artifacts (`security.json`, `qa.json`, unaffected docs) stay **byte-identical**.

## Assertions (checker)
- **Amendment recorded:** `planning/amendments/` has an entry.
- **Affected-only rerun:** `rerun` includes pm + engineer; **excludes** security + qa (`check_amendment`). A whole-team rerun = FAIL (it's a rerun, not an amendment).
- **Correct staleness set:** `stale_docs` count in [4,5] — no over-marking (`13-risk-register` stale only if a new risk emerged).
- **Byte-identical untouched:** `security.json` / `qa.json` SHA-256 match the baseline.
- **Budget gate:** amendment cost **< 15K** (target 8–12K). Over budget = FAIL **even with good docs**.

## Pass / fail
PASS iff the staleness set is correct, only affected specialists reran, untouched files are byte-identical, and cost < 15K. Eager regeneration of all docs OR a whole-team rerun OR >15K = FAIL.
