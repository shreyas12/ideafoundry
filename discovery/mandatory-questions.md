# Discovery — Mandatory Questions (Stage 1)

<!-- token-budget: <=1.2K -->
<!-- phase: Discovery · loaded first on /ideafoundry -->

Discovery is a **conversation, not a form**. Ask the six mandatory questions below, then hand off to `probing-rubric.md` for Stage 2. **Hard cap across Stages 1+2: 8 questions total.** Reaching for Q9 is the signal to stop, draft the Brief, and record the gap in `gaps_to_clarify`.

## Interaction rules
- Prefer **buttons** (`ask_user_input_v0`) for closed-set answers (platform, team size, timeline) and **free-text** for open ones (problem, success). Guidance per question below.
- **One question at a time** when the answer shapes the next; you may batch 2–3 obviously-independent closed questions into a single turn to save the user's energy.
- A **follow-up is allowed** only when an answer changes the framing (e.g. "kids' app" → applicable-law follow-up). A follow-up counts against the 8-question cap.
- Never ask something the user already told you in their opening description — extract it and confirm instead of re-asking.

## Stage 1 — the six mandatory questions

Each maps to a Brief section (see `brief-schema.md`). If the opening idea already answers one, skip the question and mark it for confirmation in Stage 3.

| # | Question | Maps to | Format |
|---|---|---|---|
| 1 | **What problem does this solve, and for whom does it hurt today?** | `brief.problem`, seed for `brief.target_users` | free-text |
| 2 | **Who is the target user?** (role, sophistication, are there multiple user types?) | `brief.target_users` | free-text |
| 3 | **What platform / surface?** (web, mobile, CLI, Slack app, API, desktop…) | `brief.constraints` | buttons + "other" |
| 4 | **What does success look like in 3 months?** (the one metric that matters) | `brief.success_metrics` | free-text |
| 5 | **What's the timeline / deadline?** | `brief.timeline` | buttons (weekend · 2 wks · 1–3 mo · 3 mo+) |
| 6 | **Who's building it?** (solo · small team · larger team; any specialist skills?) | `brief.team` | buttons + free-text |

These six populate the **mandatory** Brief fields. If any comes back empty or unusable, Confidence is **Red** and Discovery cannot complete (see `confidence.md`).

## After Stage 1
1. Run `probing-rubric.md` for adaptive Stage-2 questions (respect the 8-cap: you have `8 − (questions asked so far)` remaining).
2. Run **Stage 3 — Confirmation**: summarize everything into a draft Brief, show it to the user in prose, and ask them to correct anything before you proceed. Only after confirmation do you write the final `planning/brief.json` and move to Roster.
3. Propose non-goals proactively during confirmation. If the user's idea has obvious scope creep risks, name candidate `non_goals` and let them confirm — a Brief with an empty `non_goals` on a consumer idea usually means Discovery under-probed.
