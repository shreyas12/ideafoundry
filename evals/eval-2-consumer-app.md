# EVAL 2 — Consumer App (vague consumer idea)

Fixture: [`fixtures/eval-2-consumer-app.json`](fixtures/eval-2-consumer-app.json) · Traces: EVAL.md §2, PLAN §12–13

**Prompt.** "Something like Duolingo but for financial literacy."

## How to run
1. `/ideafoundry consumer-app` with the prompt; complete the workshop; save `planning/` + `docs/` + `tokens.json`.
2. `python3 evals/check.py --fixture evals/fixtures/eval-2-consumer-app.json --planning <run>/planning --tokens <run>/tokens.json`

## Expected behavior
- **Discovery narrows the vagueness:** probes audience (adults/teens?), platform (mobile-first likely), accounts/user-data, monetization, success metric (retention vs lessons). ≤8 questions; if audience <18, a minor-data question fires. Confidence likely **Yellow** with populated `gaps_to_clarify`.
- **Roster:** **PM + Engineer + UX.** **Security proposed** because accounts + progress = stored user data — the proposal *recommends a specialist the user didn't ask for* and explains why (exercises "teaches when it recommends"). Recorded in `roster.json` either as included (with reason) or declined-after-proposal (with reason).
- **UX output:** mobile-first; 3 core flows (onboard→placement, daily-lesson, streak/review); explicit accessibility floor.

## Assertions (checker)
- **DECISIVE — UX high challenge surfaces.** UX fires `challenges_to_brief` with `impact: high` on the success metric ("lessons completed rewards volume, not retention"); `check_challenges` requires ≥1 high challenge **and** that it's represented in `decisions.escalations` (materiality gate: high surfaces, med/low → `challenges_log.json`).
- **Security-proposed reasoning:** if Security is included, its inclusion reason cites the user-data signal; if declined, the decline reason does. Non-empty either way.
- **Ceiling:** zero unjustified items (lighter banned list; consumer app rarely needs enterprise infra).
- **Roster reasoning / MVP cut / traceability:** as global criteria.
- **Consensus:** one surfaced challenge (UX metric) + one resolved conflict (e.g. PM vs UX on onboarding length — placement test vs quick start).
- **Budget:** profile total ≤ 45K (target initial ~34K).
- **Docs:** 8-doc set including `06-ux-specification`; `07-security-review` present iff Security joined, else flagged `not in roster`.

## Pass / fail
PASS iff the UX metric challenge fired **and surfaced**, Security was *proposed with reasoning* (not silently added/omitted), budget under cap, and global criteria hold.
