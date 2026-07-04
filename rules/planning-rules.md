# Planning Rules — the constraints every specialist obeys

<!-- token-budget: <=1K -->
<!-- Loaded during Brief phase and referenced by every specialist. The general discipline; MVP-specific cutting lives in mvp-rules.md. -->

These are the non-negotiable rules that make IdeaFoundry outputs traceable, cheap, and honest. A specialist output that violates one is a **schema violation**, not a style preference.

## 1. Cite by ID, never restate
Reference `brief.goals.g1`, `brief.constraints.c2`. **Never copy Brief text into your output.** Restatement duplicates content, breaks staleness tracking, and taxes every render. If you need a Brief fact, cite its ID and let the reader resolve it.

## 2. Don't invent — surface gaps instead
If the Brief is silent on something you need, do **not** guess a plausible value. Add it to `gaps_to_clarify`. If it blocks your output, set `blocks: true` (this halts generation until resolved). Inventing a constraint the user never stated is the failure mode that makes a plan quietly wrong.

## 3. Simplest default that satisfies the Brief
The correct answer is the **least** machinery that meets the stated goals and constraints — SQLite over Postgres, cron over queues, library-default auth over custom, single-instance over autoscaling, server-rendered over SPA. The profile's `complexity_ceiling` is a **floor for scrutiny, not a target**: anything on `reject_unless_justified` requires a `complexity_justification` quad grounded in a Brief constraint ID. "Best practices", "future-proofing", and "scale we might hit" are **not** valid justifications — Consensus will flag them.

## 4. Challenge only on genuine error (materiality-gated)
You may disagree with the Brief via `challenges_to_brief` — but only when it's genuinely wrong, and you must tag `impact`. `high` = "if accepted, changes ≥1 MVP feature, ≥1 architectural choice, or ≥1 success metric." Manufactured or stylistic challenges are noise; the materiality gate exists because LLMs challenge *something* every run.

## 5. Re-anchor from files, not conversation
Your only inputs are `planning/meta.json`, your declared Brief sections, and the `summary` fields of declared dependencies. **Prior conversation is not consulted.** This keeps turn 15 as sharp as turn 1.

## 6. Structured JSON, then hand back
Emit your `planning/<role>.json`, self-check against your file's pass criteria, then return control. You do not render markdown (that's Generation) and you do not reconcile with other specialists (that's Consensus).

## 7. Traceability is mandatory
Every output carries `traces_to` (the Brief IDs it derives from). Every ticket carries `traces_to` a goal. The graph is load-bearing — Amendment walks it backward to find what a change invalidates (see `traceability.md`).
