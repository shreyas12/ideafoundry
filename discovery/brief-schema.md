# Project Brief — Schema (`planning/brief.json`)

<!-- token-budget: <=1.5K -->
<!-- schema_version: 1 -->

The Brief is the **single source of truth**. Every specialist works exclusively from it and **cites sections by ID**. Restating Brief content in a specialist output is a **schema violation** (see `rules/planning-rules.md`).

## Section IDs
Every section carries a **stable ID**. List sections get per-item IDs: `brief.goals.g1`, `brief.constraints.c3`, `brief.target_users.u2`. IDs are assigned in creation order and **never renumbered** (Amendment relies on stability — append new IDs, mark old ones stale, don't reuse).

## Shape

```json
{
  "schema_version": 1,
  "vision": "one-paragraph what-and-why",
  "problem": "the pain, and for whom it hurts today",
  "target_users": [
    {"id": "u1", "label": "primary user", "description": "...", "sophistication": "novice|intermediate|expert"}
  ],
  "goals":          [{"id": "g1", "text": "business/user goal"}],
  "non_goals":      [{"id": "ng1", "text": "explicitly out of scope"}],
  "constraints":    [{"id": "c1", "text": "platform / timeline / integration / budget constraint", "kind": "platform|timeline|integration|budget|team|other"}],
  "timeline":       {"id": "t1", "horizon": "weekend|2-weeks|1-3-months|3-months-plus", "hard_deadline": "date or null"},
  "team":           {"id": "tm1", "size": "solo|small|larger", "skills": ["..."]},
  "budget":         {"id": "b1", "text": "money/infra budget or 'unspecified'"},
  "success_metrics":[{"id": "s1", "metric": "the one thing that matters", "target": "value or 'directional'"}],
  "assumptions":    [{"id": "a1", "text": "stated or inferred assumption"}],
  "risks":          [{"id": "r1", "text": "known risk from the user"}],
  "gaps_to_clarify":[{"id": "gap1", "text": "open question Discovery couldn't close", "blocks": false}],
  "confidence": "red|yellow|green",
  "domain_signals": ["regulated", "ai-native", "consumer", "..."]
}
```

## The 12 sections (per PLAN §10)
`vision · problem · target_users · goals · non_goals · constraints · timeline · team · budget · success_metrics · assumptions · risks` — plus operational fields (`gaps_to_clarify`, `confidence`, `domain_signals`).

## Mandatory vs discretionary
- **Mandatory** (Confidence Red if missing/unusable): `problem`, `target_users`, at least one `constraints` entry covering platform, `success_metrics`, `timeline`, `team`.
- **Discretionary** (sparse → Yellow): `non_goals`, `assumptions`, `risks`, `budget`.

## Rules
- **No restatement downstream.** Specialists reference `brief.goals.g1`; they do not copy its text into their output.
- **`gaps_to_clarify` with `blocks: true`** halts generation until resolved (a specialist can also add gaps during review).
- **`domain_signals`** is set from the probing rubric and drives the roster proposal.
- On **Amendment**, accepted challenges mutate this file; new IDs are appended, superseded IDs are tagged `stale: true` (not deleted).
