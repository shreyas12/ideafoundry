# IdeaFoundry — WORKFLOW (the whole phase graph)

<!-- token-budget: reference doc — loaded by humans and on amend/export/continue, not every turn -->

`SKILL.md` is a lean router and deliberately omits phase logic. **This is the one file that describes the entire lifecycle** so a human (or Claude, when it needs the big picture) can follow it end to end. Each phase produces a **persisted artifact** in `planning/`; nothing important lives only in the conversation.

```
User describes an idea
  → Discovery (≤8 questions)                → planning/brief.json (draft)
  → Brief confirmation + Confidence band    → planning/brief.json (confirmed), STATUS.md
  → Roster Selection (propose + confirm)    → planning/roster.json
  → Specialist Review (one per turn)        → planning/<role>.json  (per specialist)
  → Consensus (coordinator, ≤3 rounds)      → planning/conflicts.json, planning/decisions.json
  → Generation (planning/ + 2 eager docs)   → README.md, PLAN_SUMMARY.md, docs/00, docs/12
  → Execution-ready project
  ↺ Amendment (when reality changes)        → planning/amendments/NNN-*.json, stale flags
```

Every phase also: overwrites `STATUS.md` (§20) and updates `planning/state.json` (last completed phase) **before ending**.

---

## Phase 1 — Discovery
Load `discovery/mandatory-questions.md` then `discovery/probing-rubric.md`.
- **Stage 1:** six mandatory questions (problem, user, platform, success, timeline, team).
- **Stage 2:** adaptive probing governed by the *rubric* (heuristics, not a decision tree). Hard cap: **8 questions total**. Overflow → `gaps_to_clarify`, not a 9th question.
- **Stage 3:** summarize into a draft Brief, show the user, allow correction.
- Compute the **Confidence band** (`discovery/confidence.md` logic, inlined in Brief handoff): Red (mandatory field missing → loop back to Discovery), Yellow (proceed with warnings), Green.
- **Artifact:** `planning/brief.json` (schema: `discovery/brief-schema.md`).

## Phase 2 — Brief
The confirmed Brief is the single source of truth. Every section carries a stable ID (`brief.goals.g1`). Specialists **cite by ID and never restate Brief content** (see `rules/planning-rules.md`). Write `planning/meta.json` (version, roster placeholder, timestamps, schema_version) and `planning/goals.json` (business goals + traceability roots).

## Phase 3 — Roster Selection
Load `roster/rubric.md` + the chosen `roster/profiles/<profile>.yaml`.
- The Skill **proposes** a roster with per-specialist *inclusion and exclusion* reasoning.
- The user **confirms or overrides**.
- **Artifact:** `planning/roster.json` (specialist list + reasoning + overrides). The active profile's `complexity_ceiling` governs the whole run.

## Phase 4 — Specialist Review
Load `specialists/<role>.md`, **one specialist per turn, in a separate context.** Each specialist:
- Re-anchors from `planning/meta.json` + its declared dependency files **only** (ignore prior conversation).
- Loads only its declared Brief sections (partial load).
- Sees only the `summary` fields of prior specialists it depends on (not full outputs).
- Emits a structured JSON object with the five cross-cutting fields: `summary`, `gaps_to_clarify`, `challenges_to_brief`, `complexity_justification`, `traces_to`.
- **Artifact:** `planning/<role>.json`.

Order: PM → Engineer → UX → Security → QA (skipping any not in the roster).

## Phase 5 — Consensus
Load `consensus/coordinator.md`. A *coordinator*, not a specialist. **Hard cap: 3 rounds, no looping.**
- **Round 1** already done (specialists wrote their files).
- **Round 2:** read specialist *summaries* → detect conflicts → `planning/conflicts.json`. Pull full outputs **only** for genuinely disagreeing sections.
- **Round 3:** resolve mechanical conflicts with written rationale; batch **all** `high` challenges + user-facing conflicts into **one** escalation; run the **Simplifier pass** (every `complexity_justification` must cite a Brief constraint, else → `simplification_candidates`). Apply the **materiality gate** (only `high` challenges surface; medium/low → `challenges_log.json`).
- **Artifact:** `planning/decisions.json` (+ `challenges_log.json`).

## Phase 6 — Generation
Load `generation/document-generator.md`. Reads `roster.json`, drops templates whose `requires:` are unsatisfied, gates sections within survivors, slot-fills from the normalized `planning/` folder (never re-reads specialist outputs).
- **Initial run emits:** `planning/` folder, `README.md` (doc index with status flags), `STATUS.md`, `PLAN_SUMMARY.md`, and **eager renders** of `docs/00-executive-summary.md` + `docs/12-developer-tickets.md`.
- Everything else stays **lazy** — `/ideafoundry render <doc-id>` renders one doc on demand; `/ideafoundry render all` is the opt-in escape hatch.
- **Caps:** no single doc > 3K tokens; conditional sections **omitted, not stubbed**.

## Amendment (`/ideafoundry amend <note>`)
Not a rerun — a targeted re-plan.
1. Write `planning/amendments/NNN-note.json` (description + timestamp).
2. Walk the **traceability graph backward** from the change to find invalidated Brief sections + specialist outputs; tag them `stale: true` (`rules/traceability.md`). Typical: 3–8 IDs.
3. Re-run **only** the affected specialists (usually 1–2) against the amended Brief.
4. Mark derived docs **stale in README.md** — do **not** eagerly regenerate. They regenerate on next `render`.
- Target cost: **8–12K**, never over 15K.

## Persistence (`export` / `continue`)
- `/ideafoundry export` → `planning-bundle.json`: one JSON object, keys = folder filenames, values = file contents. Single downloadable file.
- `/ideafoundry continue` — with a pasted bundle, reconstitute the folder + regenerate views; without one, read `state.json`, report the last completed phase, and offer to resume.

## Recovery
Load `rules/RECOVERY.md` **only when an error condition is detected** (malformed specialist JSON, unresolved conflicts after 3 rounds, abandoned run, absent-specialist reference, token budget exceeded). Zero cost on the happy path.
