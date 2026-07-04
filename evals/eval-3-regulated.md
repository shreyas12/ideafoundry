# EVAL 3 — Regulated (technically ambitious)

Fixture: [`fixtures/eval-3-regulated.json`](fixtures/eval-3-regulated.json) · Traces: EVAL.md §3, PLAN §13, §16

**Prompt.** "Semantic caching layer for LLM apps handling customer prompts."

## How to run
1. `/ideafoundry regulated` with the prompt; complete the full five-specialist workshop; save `planning/` + `docs/` + `tokens.json` (record per-doc render cost too).
2. `python3 evals/check.py --fixture evals/fixtures/eval-3-regulated.json --planning <run>/planning --tokens <run>/tokens.json`

## Expected behavior
- **Discovery:** probes data sensitivity (customer prompts = PII), compliance regime, latency budget, model provider, cache-hit correctness tolerance, deployment surface. AI-native + customer-data triggers both the compliance and latency/inference-cost probes. Likely Green after 7–8 questions.
- **Roster:** **all five.** Security **mandatory** (customer prompts = personal data + production surface), justification recorded.
- **Security must push back:** ≥1 concrete threat the Brief ignored (cross-tenant semantic collision, cache poisoning, PII retention) + a compliance mapping.
- **Engineer must push back on latency:** a semantic cache adds an embedding + vector-search hop; if the Brief implies "faster than the model always," Engineer fires a `high` challenge.

## Assertions (checker)
- **DECISIVE — enforcement survives the wide ceiling.** `banned_ceiling_terms` is empty (enterprise patterns are appropriate here), so the check flips to `justification_must_cite_brief`: **every** `complexity_justification` (e.g. dedicated vector store, per-tenant KMS) must cite a Brief/compliance constraint in `why_needed` — not "best practices". This is the "ceiling scales with profile, enforcement never disappears" assertion.
- **Security fired:** ≥1 challenge or concrete threat the Brief ignored (`check_challenges` any_fired_min = 1; a threat in `security.threats` also satisfies the spirit — verify manually if no challenge fired).
- **Consensus batching:** Engineer's latency challenge + Security's PII challenge appear in **one** `decisions.escalations` batch. Simplifier flags any justification not Brief-grounded into `simplification_candidates`.
- **Roster mandatory:** Security ∈ roster.
- **Budget:** initial ≤46K; each on-demand render <3K; typical read (initial + 4 docs) ≤52K; hard cap 55K. `render all` should warn.
- **Docs:** full 14-doc set available; `07-security-review` renders its Compliance section (GDPR/SOC2).

## Pass / fail
PASS iff Security pushed back, every ceiling deviation is Brief-justified, high challenges batched into one escalation, and the run stays under the 55K cap with each doc under 3K. An unjustified enterprise choice OR a blown budget = FAIL.
