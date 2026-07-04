# state.json + STATUS.md writer

<!-- token-budget: <=0.5K -->

Two always-on artifacts written at **every phase boundary** (before the turn ends). Together ~1.5K per full run.

## `planning/state.json` (~50 tokens)
One line, machine-read by `continue`/`help`. Overwritten, never appended.

```json
{"schema_version":1,"last_completed_phase":"consensus","profile":"weekend-hack","confidence":"green","next":"generation"}
```

`last_completed_phase` ∈ `discovery | brief | roster | specialists:<role> | consensus | generation | amendment:NNN`.

## `STATUS.md` (project root, ~200 tokens/write)
Human orientation *while planning*. **Overwritten (replaced), not appended.** Shape (PLAN §20):

```
Phase: Consensus (3/5 conflicts resolved)
Roster: PM, Engineer, Security
Confidence: 🟢 Green
Open escalations: 2
Last update: <ISO timestamp>
Next: user decides on auth approach → resume with `/ideafoundry continue`
```

## Rules
- Write **both** at the end of every phase, including partial/abandoned runs (so `continue` can resume).
- `STATUS.md` is a *view* — never the source of truth. The `planning/` folder is.
- Keep `Next:` actionable: name the exact subcommand the user should type.
- If a token warning fired this phase, add a `⚠️ Warnings: see WARNINGS.md` line.
