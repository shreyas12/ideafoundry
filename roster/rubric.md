# Roster Rubric — Proposal + Confirmation

<!-- token-budget: <=1.2K -->
<!-- phase: Roster · loaded after Brief is confirmed -->

Not every project needs all five specialists. Forcing a 50K full-team run on a weekend hack is why over-scoped tools go unused. **The Skill proposes a roster with per-specialist reasoning; the user confirms or overrides.** Neither pure-auto (paternalistic) nor pure-manual (users don't know what they don't know — the person building a health app skips Security *because* they aren't thinking about HIPAA).

## Procedure
1. Load the chosen `roster/profiles/<profile>.yaml` (or infer a profile from `brief.domain_signals` + timeline if the user didn't name one).
2. Start from the profile's `specialists` list.
3. Apply the heuristics below to **add** or **note-droppable** specialists.
4. Present the proposal: for **each** of the five specialists, state **in** (why) or **out** (why). Recommending a specialist the user didn't ask for is a feature — it **teaches**.
5. User confirms or overrides. Persist `planning/roster.json` with reasoning for every inclusion **and** exclusion, plus any override.

## Heuristics (judgment, not branches)

| Condition | Effect |
|---|---|
| Regulated domain (health, finance, kids, EU personal data, hiring) | **Security mandatory** |
| Any production deployment with real users | **Security mandatory**, regardless of domain |
| Consumer-facing with >1 user type | **UX mandatory** |
| Consumer app with auth / stored user data / payments / minor audience | **Propose Security** (explain why) |
| Solo dev + weekend timeline | **QA droppable**; PM + Engineer suffice |
| Internal tool, small known user base | **UX droppable** |
| Idea stores/handles PII the Brief treats as non-sensitive | **Propose Security** + flag for a `challenges_to_brief` later |

**Security is never silently dropped on a regulated or production Brief** — if the user overrides to remove it, record the override and its stated reason in `roster.json`, and keep the security-relevant `challenges` surfacing anyway.

## `planning/roster.json` shape
```json
{
  "schema_version": 1,
  "profile": "weekend-hack",
  "included": [
    {"role": "pm", "reason": "always — owns MVP cut and scope"},
    {"role": "engineer", "reason": "always — owns feasibility and stack"}
  ],
  "excluded": [
    {"role": "ux", "reason": "single Slack surface, no bespoke UI — Slack affordances suffice"},
    {"role": "security", "reason": "no user data beyond Slack-scoped messages, no external deploy surface; revisit if storing transcripts"},
    {"role": "qa", "reason": "solo dev, 2-week timeline — PM acceptance criteria cover release confidence"}
  ],
  "overrides": []
}
```

The active profile's `complexity_ceiling` governs every specialist for the whole run — record `profile` so specialists and the Consensus simplifier can load it.
