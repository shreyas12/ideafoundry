# Discovery — Probing Rubric (Stage 2)

<!-- token-budget: <=1.2K -->
<!-- phase: Discovery · loaded after mandatory-questions.md -->

Stage 2 is **adaptive probing governed by judgment, not a decision tree.** Domain trees ("if health → ask A, B, C") are infinite and stale on arrival. Instead, apply these **heuristics**: read what Stage 1 surfaced, and probe only where a missing answer would materially change the Brief, the roster, or the architecture.

**Budget:** you have `8 − questions_asked` questions left. Most projects need **0–2** Stage-2 questions. A weekend hack for internal tooling often needs none. Spend them where they're load-bearing.

## Probing heuristics

Fire a probe when a signal is present **and** the answer would change a downstream decision:

| Signal in the Brief so far | Probe | Why it's load-bearing |
|---|---|---|
| **Regulated domain** (health, finance, kids, EU personal data, hiring) | Which compliance regime applies? What data is stored? | Makes Security mandatory; changes architecture (encryption, tenancy, retention). |
| **Audience < 13, or any health data** | Which specific law? (COPPA, HIPAA, GDPR-minor…) | Changes the threat model and gates whole doc sections. |
| **AI-native** (LLM/model in the core loop) | Model provider? Latency budget? Per-request inference cost? Correctness tolerance? | Drives stack, cost model, and feasibility challenges. |
| **Consumer-facing with >1 user type** | Do users have accounts / stored progress? Monetization intent? | Triggers UX; may trigger Security (user data). |
| **"Real-time" / "at scale" / "millions of users"** in the pitch | What's the actual concurrency / volume on day one? | Guards against over-engineering; often day-one is tiny. |
| **Integrations named** (Stripe, Slack, Salesforce…) | Which API tier / rate limits / auth model? | Feasibility + becomes a Brief constraint specialists cite. |
| **Vague idea** ("something like X but for Y") | Narrow the audience and the one success metric. | Without this the Brief is Yellow with heavy `gaps_to_clarify`. |

## Rules
- **Do not over-probe.** If Stage 1 gives you a coherent, buildable picture and no high-value signal fires, **stop** — draft the Brief. Over-probing internal tooling for compliance it doesn't have is the same failure as over-scoping.
- **One probe can cover two signals.** Prefer a single well-aimed question over two narrow ones.
- **Overflow → `gaps_to_clarify`, not Q9.** If you still have open questions at the 8-cap, write them into `brief.gaps_to_clarify` so specialists raise them later. Do not exhaust the user.
- A probe that reveals a challenge to the user's framing is fine — note it, but don't argue during Discovery; that's the specialists' and Consensus's job.

## Handoff
When probing is done (or the cap is hit), proceed to **Stage 3 — Confirmation** (see `mandatory-questions.md`): draft Brief → show user → correct → write `planning/brief.json` → compute Confidence band (`confidence.md`).
