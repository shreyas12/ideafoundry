# Amendment — targeted re-plan, not a rerun

<!-- token-budget: <=1.2K -->
<!-- Loaded on `/ideafoundry amend <note>`. Depends on traceability.md for the staleness walk. Target cost 8–12K, hard cap 15K. -->

Reality changes after planning. Amendment is **first-class**: it re-plans only what the change touches. A run that reruns the whole team or eagerly regenerates every doc is **not an amendment — it's a rerun**, and it fails the budget gate.

## Steps
1. **Record.** Write `planning/amendments/NNN-<slug>.json`:
   ```json
   {"schema_version":1,"id":"001","note":"support offline mode","timestamp":"<ISO>","invalidates":[],"rerun":[],"stale_docs":[]}
   ```
   `NNN` is the next zero-padded number (`ls planning/amendments/`). History is the folder; **do not build a diff/rollback engine** — rollback is `git revert`.

2. **Update the Brief if needed.** If the amendment changes a stated fact (a constraint, a goal, an assumption), append **new** Brief IDs and tag superseded ones `stale: true` (never renumber). Record the changed IDs.

3. **Backward staleness walk** (`traceability.md`). From the changed Brief IDs, compute the staleness set: which specialist outputs are invalidated, which specialists must rerun, which docs go stale. Fill `invalidates` / `rerun` / `stale_docs` in the amendment file. **Typical: 3–8 IDs, 1–2 specialists.**

4. **Tag stale.** Set `stale: true` on each invalidated `planning/<role>.json`. Mark each affected doc `stale` in `README.md`. **Do not regenerate docs now.**

5. **Rerun only affected specialists** against the amended Brief, one per turn, re-anchoring as always. Untouched specialists' files stay **byte-identical**. Reruns may cascade (rerun Engineer → its `summary` changed → QA that depended on it may need rerun) — follow the walk, don't rerun defensively.

6. **Re-run Consensus only if reruns produced new conflicts/challenges.** If the staleness set is a single specialist with no new conflict, skip Consensus and go straight to state/STATUS write.

7. **Write state.** `STATUS.md` + `state.json` (`last_completed_phase: amendment:NNN`).

## Lazy doc regeneration
A doc flagged `stale` regenerates from the **current** `planning/` on its **next** `/ideafoundry render`, then flips back to `available`. Amendment never eagerly regenerates — this is what keeps cost at 8–12K instead of a full render.

## Budget gate
Target 8–12K, **hard cap 15K**. If a proposed amendment would exceed it, the walk is over-marking — tighten it (field-level precision, `traceability.md`), don't raise the cap.

## Guardrails
- No over-marking: a doc/specialist that never traced to the change stays untouched and byte-identical.
- No eager regen: stale docs wait for a read.
- No whole-team rerun: if you're rerunning >half the roster for a small note, the staleness walk is wrong.
