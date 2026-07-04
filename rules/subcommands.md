# Subcommands — help / status

<!-- token-budget: <=0.5K -->
<!-- Loaded on `/ideafoundry help` and `/ideafoundry status`. Both are cheap, read-only views. -->

## `/ideafoundry help`
Print the subcommand table and the current phase (read `planning/state.json` → `last_completed_phase`; if no `planning/` exists yet, say "no active project — start with `/ideafoundry`").

```
IdeaFoundry — plan before the code. Current phase: <state.last_completed_phase or "none">

  /ideafoundry [<profile>]   start a new plan (Discovery → … → Generation)
  render <doc-id> | render all   render a doc on demand (see README for the doc list)
  amend "<note>"             re-plan only what a change touches
  status                     print STATUS.md
  export                     write planning-bundle.json (portable state)
  continue                   resume from state.json, or paste a bundle to restore
  help                       this list

Profiles: weekend-hack · internal-tool · consumer-app · regulated (default: proposed from your Brief)
```

## `/ideafoundry status`
Print the current `STATUS.md` verbatim (it's already the human dashboard — don't regenerate it, just show it). If none exists, say there's no active project.

## Rules
- Both are **read-only** — they never mutate `planning/` or trigger a phase.
- `help` shows the live phase so a returning user knows where they left off without running anything.
- Keep the help text in sync with the router's dispatch table in `SKILL.md`.
