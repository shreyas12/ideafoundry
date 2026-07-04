# Specialist Output — Shared Contract

<!-- token-budget: <=1K -->
<!-- Loaded once alongside any specialist file. Defines the five cross-cutting fields + execution rules common to all specialists. -->

Every specialist answers **one crisp question** and emits a **structured JSON object** (never prose). Each specialist file (`specialists/<role>.md`) adds its own content fields; this file defines what they all share.

## The five cross-cutting fields (required on every specialist output)

```json
{
  "schema_version": 1,
  "role": "pm|engineer|ux|security|qa",
  "summary": "≤150-token précis of conclusions + stakes-in-the-ground. Consensus and downstream specialists read THIS to decide whether to pull the full output. Cheap conflict detection lives here.",
  "traces_to": ["brief.goals.g1", "brief.constraints.c2"],
  "gaps_to_clarify": [
    {"id":"gap1","text":"Brief was silent on X, needed for Y","blocks": true}
  ],
  "challenges_to_brief": [
    {"brief_section_id":"brief.success_metrics.s1","concern":"...","recommendation":"...","impact":"high|medium|low"}
  ],
  "complexity_justification": [
    {"recommendation":"...","why_needed":"cites a Brief constraint id","simpler_alternative_considered":"...","why_rejected":"grounded in the Brief, not 'best practices'"}
  ]
}
```

- **`summary`** — the load-bearing field for summary-first Consensus. Must be trustworthy; it stands in for the full output.
- **`traces_to`** — Brief IDs this output derives from. Powers Amendment staleness (walk backward from a changed ID to find stale outputs).
- **`gaps_to_clarify`** — Brief silent on something needed. `blocks: true` **halts generation** until resolved.
- **`challenges_to_brief`** — the Brief itself looks wrong. **Materiality gate:** only `impact: high` surfaces to the user (via Consensus, batched); `medium`/`low` → `planning/challenges_log.json`. `high` = "if accepted, changes ≥1 MVP feature, ≥1 architectural choice, or ≥1 success metric." Do **not** manufacture challenges — LLMs challenge *something* every run; fire only on genuine error.
- **`complexity_justification`** — any recommendation exceeding the active profile's `complexity_ceiling.reject_unless_justified` **must** carry this quad. Anything not listed is presumed the simplest option satisfying the Brief. Empty array = "I stayed within the ceiling" (the good default).

## Execution rules (all specialists)
- **Re-anchor** from `planning/meta.json` + your declared dependency files **only**. **Prior conversation is not consulted** — this sidesteps long-conversation degradation across a 15+ turn run.
- **Partial Brief load:** load only the Brief sections your file declares. Do not reason over `brief.budget` unless you declared it.
- **Dependency summaries only:** if you depend on a prior specialist, load its `summary` field — **not** its full output. (Consensus does full-output pulls later, only on conflict.)
- **Cite, don't restate.** Reference `brief.goals.g1`; never copy its text into your output. Restatement is a schema violation.
- **Default to the simplest thing that satisfies the Brief.** The ceiling is a floor for scrutiny, not a target.
- Write your output to `planning/<role>.json`, then hand back to the router (next specialist or Consensus).
