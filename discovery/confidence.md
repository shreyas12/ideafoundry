# Planning Confidence — Traffic Light (Discovery → Brief handoff)

<!-- token-budget: <=0.5K -->

Three bands, **no arithmetic** (a percentage invites "why 82 not 85" and implies false precision). Computed once at the Discovery→Brief handoff and re-checked if a mandatory field later empties.

| Band | Condition | Behavior |
|---|---|---|
| **🔴 Red** | Any *mandatory* Brief field missing or unusable (`problem`, `target_users`, platform `constraint`, `success_metrics`, `timeline`, `team`). | **Cannot proceed.** Discovery loops back automatically to fill the gap — ask the one missing question (still under the 8-cap; a re-ask replaces an unused slot). |
| **🟡 Yellow** | All mandatory present, but *discretionary* fields sparse (`non_goals`/`assumptions`/`risks` mostly empty) or `gaps_to_clarify` non-trivial. | **Proceed with warnings.** Specialists will raise the gaps; note them in `STATUS.md`. |
| **🟢 Green** | Mandatory *and* discretionary both dense. | **Proceed.** |

## Wiring
- Write the band into `brief.confidence`, `planning/state.json`, and `STATUS.md`.
- **Red auto-loops** — do not advance to Roster with a Red Brief. Draft-and-show (Stage 3) happens regardless of band; the band gates *advancement*, not confirmation.
- Consumer/vague ideas commonly confirm at **Yellow** — that's expected, not a failure. Don't manufacture false Green by inventing `assumptions`.
