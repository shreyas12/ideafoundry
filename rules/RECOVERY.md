# RECOVERY — failure handling

<!-- token-budget: <=1K -->
<!-- Loaded ONLY when SKILL.md detects an error condition. Zero cost on the happy path — never loaded on a clean run. -->

Every phase has a documented failure behavior. The rule under all of them: **complete the phase, write the artifact, never fail silently.** Errors degrade gracefully; they never abort the run.

## The five cases (PLAN §19)

### 1. Malformed specialist JSON
Re-prompt the specialist **once** with its schema. If the second attempt is still malformed, write `planning/errors/<role>.json` (the raw output + what failed), continue **without** that specialist, and note the gap. Consensus records the missing role in `decisions.unresolved`; templates requiring that specialist drop as if it were never in the roster.

### 2. Consensus can't resolve after 3 rounds
**No looping.** Whatever remains after Round 3 goes into `decisions.unresolved` and is batched into the single user escalation. The run proceeds to Generation — an unresolved conflict is documented, not a blocker.

### 3. User abandons mid-run
Every phase writes its artifact + `state.json` + `STATUS.md` **before ending**, so there's always a resumable checkpoint. `/ideafoundry continue` (no bundle) reads `state.json`, reports `last_completed_phase`, and asks whether to proceed from there (see `persistence.md`).

### 4. Template references an absent specialist
Roster gating should prevent this (templates declare `requires:`). If a reference slips through anyway, the Document Generator **omits that section with a one-line note in `README.md`** — never emit a broken `planning.<role>.*` reference and never a render error. (This is also the F-040 eval assertion.)

### 5. Token budget exceeded mid-phase
The phase **completes** its current output, then writes the overage to `WARNINGS.md` at project root (which phase, estimated tokens, the cap). The run continues. **Never silent** — and `STATUS.md` adds a `⚠️ Warnings: see WARNINGS.md` line. Do **not** raise the cap to make the warning go away; the fix is a smaller schema/template (PLAN §23).

## Error artifacts
- `planning/errors/<role>.json` — a specialist that failed twice.
- `WARNINGS.md` (root) — token overages and other non-fatal warnings, appended across the run.

## The invariant
A run always ends with a valid `planning/` folder and a truthful `STATUS.md`. Missing pieces are **recorded** (errors/unresolved/warnings), never hidden. Partial output the user can see and act on beats a clean abort.
