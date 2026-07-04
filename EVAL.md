# IdeaFoundry — EVAL.md

> **What this validates.** Four test-idea prompts, each targeting a different profile, plus an amendment run. Each eval specifies expected Discovery behavior, Brief population, roster proposal + reasoning, example structured specialist outputs, expected Consensus escalations, and pass criteria. Every run **measures and reports per-phase token usage and the profile total**. A run that produces good docs but blows the budget is a **fail**. A run that produces an over-engineered plan for a small project is a **fail even if everything else passes** — that is the failure mode most likely to make this tool look silly in public.

## Global pass criteria (all evals)

A run **passes** iff:
1. Discovery captured **real constraints** (not generic filler), within the 8-question cap.
2. Roster proposal was **reasoned**, not blindly full-team; inclusions and exclusions both carry reasoning in `roster.json`.
3. **Only the roster's docs** were generated; absent-specialist docs are flagged `not in roster`, never broken.
4. At least one **visible specialist disagreement** was resolved by Consensus with written rationale.
5. Tickets are **small enough to execute** and every ticket has `traces_to` a goal ID.
6. **Total token usage stayed under the profile's hard cap** (§23); per-phase usage reported.
7. `STATUS.md` was **updated at each phase boundary**.
8. **No specialist recommendation exceeded the profile's complexity ceiling without a Brief-grounded justification.**

## Rubrics (applied to specialist outputs, every eval)

- **PM** — Does the MVP *actually cut scope*? A pass shows features explicitly moved to a later roadmap phase, not "everything is MVP."
- **Engineer** — Does it *challenge feasibility* where the Brief is optimistic, and default to the simplest stack that satisfies the Brief?
- **UX** — Are flows tied to `target_users` and a stated accessibility floor?
- **Security** — Does it *push back* rather than rubber-stamp? A pass fires ≥1 `challenges_to_brief` or a concrete threat the Brief ignored.
- **QA** — Are acceptance skeletons tied to specific features, with real edge cases?
- **challenges_to_brief** — Do they fire only when the Brief is *genuinely wrong* (materiality gate), and does exactly the `high` set surface while `medium`/`low` land in `challenges_log.json`?

---

## EVAL 1 — Weekend Hack (Concrete B2B)

**Prompt:** "Slack app that summarizes standups and flags blockers." Solo dev, 2 weeks.

**Expected Discovery:** ≤6 questions. Captures: problem (standup noise), user (small eng teams via Slack), platform (Slack app), success (blockers surfaced daily), timeline (2 weeks), team (solo). Probing rubric should *not* over-probe compliance — this is internal tooling with no regulated data. Confirmation shows a Yellow/Green Brief.

**Expected Brief population:** `constraints.c1 = solo dev`, `constraints.c2 = 2-week timeline`, `non_goals` should include analytics dashboards, multi-workspace admin, historical trends. If the model doesn't propose non-goals, Discovery under-probed — soft fail.

**Expected roster proposal:** **PM + Engineer.** UX **proposed and declined** ("single Slack surface, no bespoke UI — Slack's affordances suffice"); Security **proposed and declined** ("no user data beyond Slack-scoped messages, no external deployment surface; revisit if storing transcripts"). Both declines captured with reasoning in `roster.json`.

**Example expected Engineer output (`architecture.json`, abridged):**
```json
{
  "summary": "Single-process Slack bot; Bolt SDK; SQLite for state; Slack Events API + a daily cron. No queue, no cache, no custom auth.",
  "traces_to": ["brief.goals.g1", "brief.constraints.c1", "brief.constraints.c2"],
  "stack": {"runtime":"Node + Bolt","db":"SQLite","scheduler":"cron","auth":"Slack OAuth (library default)"},
  "complexity_justification": [],
  "challenges_to_brief": [],
  "gaps_to_clarify": []
}
```

**Anti-over-engineering check (the decisive assertion):** Engineer's output **must not** recommend Kubernetes, Redis, microservices, custom auth, or a message queue. Any such recommendation **must** appear in `complexity_justification` with a Brief-grounded reason. Default recommendations must be SQLite/Postgres single-instance, library-default auth, cron for scheduling. **If Engineer suggests anything more complex without justification → EVAL FAILS.**

**Expected Consensus:** minimal — PM's "flag blockers" scope vs Engineer's 2-week feasibility may produce one scope-trim decision (e.g., "blocker detection = keyword + explicit `@blocked`, NLP deferred to roadmap"). One resolved disagreement satisfies criterion 4.

**Expected generation + budget:** initial run = `planning/` + README + STATUS + PLAN_SUMMARY + eager `00` + `12`. **Initial run ≤ ~26K, hard cap 35K.** Then read ≤3 more docs on demand, each <3K, typical total ~30K.

---

## EVAL 2 — Consumer App (Vague Consumer)

**Prompt:** "Something like Duolingo but for financial literacy."

**Expected Discovery:** must *narrow the vagueness* — probe target audience (adults? teens?), platform (mobile-first likely), whether accounts/user data exist, monetization intent, success metric (retention? lessons completed?). Stays ≤8 questions; if audience is <18, probing rubric triggers a minor-data question. Confirmation likely Yellow (consumer ideas start sparse) with `gaps_to_clarify` populated.

**Expected roster proposal:** **PM + Engineer + UX** (consumer-facing, >1 user type). **Security proposed** if the Brief indicates auth or stored user data (accounts, progress) — for a Duolingo-like app it should fire, since progress + accounts = user data. Expect the proposal to *recommend Security the user didn't ask for* and explain why — this exercises the "teaches when it recommends" property.

**Example expected UX output (`ux.json`, abridged):**
```json
{
  "summary": "Mobile-first; 3 core flows: onboard→placement, daily-lesson, streak/review. Accessibility floor: WCAG AA contrast, dynamic type.",
  "traces_to": ["brief.target_users.u1","brief.goals.g2"],
  "personas": ["new-to-money adult","budgeting-anxious young adult"],
  "primary_flows": ["onboarding+goal-set","daily lesson loop","progress/streak review"],
  "challenges_to_brief": [{"brief_section_id":"brief.success_metrics.s1","concern":"'lessons completed' rewards volume not retention","recommendation":"track 7-day return + concept retention","impact":"high"}]
}
```

**Expected Consensus escalation:** the UX `high` challenge on the success metric surfaces to the user (materiality: it changes a success metric). PM vs UX on onboarding length (placement test vs quick start) is a resolvable scope decision. Expect **one surfaced challenge + one resolved conflict.**

**Expected budget:** initial ~34K (cap 45K); typical read ~40K.

---

## EVAL 3 — Regulated (Technically Ambitious)

**Prompt:** "Semantic caching layer for LLM apps handling customer prompts."

**Expected Discovery:** probes data sensitivity (customer prompts = PII risk), compliance regime, latency budget, model provider, cache-hit correctness tolerance, deployment surface (SaaS? self-hosted?). AI-native + customer-data triggers both the compliance and the latency/inference-cost probes. Likely Green after 7–8 questions.

**Expected roster proposal:** **full five.** Security **mandatory** (customer prompts = personal data + production deployment). Justification recorded.

**Expected specialist behavior (the assertions that matter):**
- **Security must fire on data-handling** — customer prompts cached = a threat model (cache poisoning, cross-tenant leakage, prompt exfiltration), plus a compliance mapping. A pass produces ≥1 concrete threat the Brief ignored.
- **Engineer must push back on latency claims** — a semantic cache adds an embedding + vector-search hop; if the Brief implies "faster than the model always," Engineer fires a `challenges_to_brief` (impact `high`: it changes a success metric / architectural claim).
- **At least one `challenges_to_brief` must fire** across the roster.

**Example expected Security output (`security.json`, abridged):**
```json
{
  "summary": "Multi-tenant cache of customer prompts is the crown-jewel risk. Mandatory tenant isolation on cache keys; encrypt at rest; no cross-tenant semantic match. Compliance: likely GDPR + SOC2 in scope.",
  "traces_to": ["brief.target_users.u1","brief.constraints.c2","brief.assumptions.a1"],
  "threats": ["cross-tenant semantic collision leaks prompts","cache poisoning returns attacker text","PII retention beyond policy"],
  "challenges_to_brief": [{"brief_section_id":"brief.assumptions.a1","concern":"assumes cache entries are non-sensitive; prompts routinely contain PII/secrets","recommendation":"treat all cached prompts as sensitive; add TTL + tenant scoping","impact":"high"}],
  "complexity_justification": [{"recommendation":"dedicated vector store + per-tenant KMS keys","why_needed":"tenant isolation is a compliance requirement (brief.constraints.c2)","simpler_alternative_considered":"single shared index","why_rejected":"shared index enables cross-tenant leakage"}]
}
```
Note: on the **Regulated** profile the wider ceiling means a vector store + KMS is appropriate — but it **still** carries a `complexity_justification` grounded in a Brief constraint. This exercises "ceiling scales with profile, enforcement never disappears."

**Expected Consensus:** Engineer's latency challenge + Security's PII challenge batch into **one** user escalation. Simplifier pass verifies each `complexity_justification` cites a Brief constraint (not "best practices"); any that don't → `simplification_candidates`.

**Expected budget (explicit target):** **initial run stays under ~46K** by generating only `planning/` + README + STATUS + PLAN_SUMMARY + eager `00` + `12`. The test then **reads 4 additional docs on demand**, validates each render lands **under 3K**, and confirms the full "typical read" total stays **under ~52K** (hard cap 55K).

---

## EVAL 4 — Amendment (from EVAL 2's completed output)

**Prompt:** `/ideafoundry amend "We just learned we need to support offline mode."` (starting from the completed Consumer App run).

**Expected behavior:**
1. Writes `planning/amendments/001-offline-mode.json`.
2. Traceability backward-walk identifies invalidated IDs — offline touches `architecture.json` (sync/storage), `product.json` (offline lesson caching feature + roadmap), possibly `ux.json` (offline states). **2–3 specialist outputs marked stale.**
3. **PM and Engineer rerun** (UX may rerun if offline-state flows are affected) against the amended Brief. Security untouched.
4. **4–5 docs marked stale** in README (`02-technical-design`, `04-database-schema`, `01-product-requirements`, `09-roadmap`, maybe `06-ux-specification`) — **not eagerly regenerated**. They regenerate on next read.
5. Untouched artifacts (`security.json` if present, `qa.json`, unaffected docs) are **byte-identical** to pre-amendment.

**Pass criteria:**
- Correct staleness set (no over-marking: `13-risk-register` need only update if a new risk emerged).
- Only affected specialists rerun; upstream decisions preserved.
- **Amendment token cost under 15K** (target 8–12K).
- A run that reruns the whole team or eagerly regenerates all docs → **FAIL** (that's a rerun, not an amendment).

---

## Roster-graceful-degradation test (cross-cutting, runs on EVAL 1)

Render a template with an **optional dependency** on the absent Security specialist against EVAL 1's Weekend Hack output. **Pass:** the security-referencing section is **omitted with a note**, and there are **zero broken references to `planning.security.*`**. **Fail:** any dangling reference, any "N/A" stub filler, or a render error.

---

## Reporting format (every eval emits)

```
EVAL <n> — <profile>
  Discovery: <n questions>, confidence <band>
  Roster: <included> | declined: <excluded + reasons present? y/n>
  Challenges fired: <count high/med/low>, surfaced: <high only? y/n>
  Consensus: <conflicts resolved>/<total>, escalations <count>
  Complexity-ceiling violations (unjustified): <count>   ← must be 0
  Tokens: per-phase [...]  |  profile total <N>K  |  hard cap <M>K  |  PASS/FAIL
  Docs generated: <list>  |  absent-specialist docs flagged correctly? y/n
```

A single unjustified ceiling violation, a blown budget, or a broken absent-specialist reference fails the eval regardless of output quality.
