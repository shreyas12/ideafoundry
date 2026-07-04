# EVAL 1 — Weekend Hack (anti-over-engineering)

Fixture: [`fixtures/eval-1-weekend-hack.json`](fixtures/eval-1-weekend-hack.json) · Traces: EVAL.md §1, PLAN §13

**Prompt.** "Slack app that summarizes standups and flags blockers. Solo dev, 2 weeks."

## How to run
1. `/ideafoundry weekend-hack` with the prompt above; complete the workshop; save the `planning/` folder + `docs/` + `tokens.json`.
2. `python3 evals/check.py --fixture evals/fixtures/eval-1-weekend-hack.json --planning <run>/planning --tokens <run>/tokens.json`

## Expected behavior
- **Discovery:** ≤6 questions. Captures problem (standup noise), user (small eng teams via Slack), platform (Slack app), success (blockers surfaced daily), timeline (2 weeks), team (solo). Should **not** over-probe compliance. `non_goals` should include analytics dashboards / multi-workspace admin / historical trends — if absent, Discovery under-probed (soft fail).
- **Roster:** **PM + Engineer.** UX **proposed and declined** ("single Slack surface, no bespoke UI"); Security **proposed and declined** ("no user data beyond Slack-scoped messages; revisit if storing transcripts"). Both declines carry reasoning in `roster.json`.
- **Engineer:** single-process Bolt bot, SQLite, Slack OAuth (library default), cron. No queue/cache/custom-auth/microservices.

## Assertions (checker)
- **DECISIVE — zero unjustified ceiling items.** No `banned_ceiling_term` (kubernetes, redis, message queue, microservice, custom auth, …) appears in `architecture.json` stack/approach/summary **unless** a matching `complexity_justification` exists. `check_ceiling` → unjustified count **must be 0**; any hit **fails the eval regardless of output quality**.
- **Defaults present:** db ∈ {sqlite, postgres}; auth mentions Slack OAuth / library / default; scheduler mentions cron.
- **Roster reasoning:** included + excluded roles all carry a non-empty `reason`.
- **MVP cut:** `product.mvp.deferred` non-empty.
- **Traceability:** every feature `serves` a real goal id.
- **Consensus:** ≥1 resolved disagreement *or* a genuinely empty `conflicts.json` (a plausible outcome is trimming NLP blocker-detection to keyword + `@blocked`, NLP → roadmap).
- **Budget:** profile total ≤ 35K hard cap (target initial ≤26K).
- **Docs gating:** `06/07/08` never rendered (their specialists are absent) — see [`eval-0-roster-degradation.md`](eval-0-roster-degradation.md).

## Pass / fail
PASS iff unjustified ceiling count = 0, budget under cap, roster reasoned, MVP cut real, and docs gated. A single unjustified ceiling item = **FAIL** — this is the failure mode most likely to make IdeaFoundry look silly in public.
