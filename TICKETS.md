# IdeaFoundry — TICKETS.md

> **Implementation backlog.** Thin vertical slices; every phase ends with a working demo. Format per ticket: **ID · Phase · Size · Description · Acceptance Criteria · Dependencies · Traces to (PLAN.md §)**. Size = S (≤½ day), M (1–2 days), L (3+ days) of prompt-engineering/authoring work — this is a Skill, so "work" means writing and calibrating prompt files, schemas, rubrics, and templates, then measuring token cost.
>
> **Definition of Done (global).** Every prompt/template/rules file declares a token budget at its top and is reviewed against PLAN.md §23. Every JSON schema declares `schema_version: 1`. No file loads more than it declares. Happy path never loads `RECOVERY.md` or `examples/`.

**Phase map**
- **Phase 1 — Walking skeleton (F-001…F-013).** Discovery → Brief → Roster → *one* specialist → render → STATUS. End-to-end for a trivial idea on Weekend Hack. Demo: `/ideafoundry` produces a Brief, a proposed roster, one PM output, and a rendered `12-developer-tickets.md`.
- **Phase 2 — Full team + Consensus + Profiles (F-014…F-030).** All five specialists, conflict detection, decision log, `challenges_to_brief`, all templates with roster gating, all four profiles, export/continue.
- **Phase 3 — Amendment + Recovery + Eval (F-031…F-041).** Amendment, failure handling, RECOVERY.md, worked example, eval harness.

---

## Phase 1 — Walking Skeleton

### F-001 · Phase 1 · S · Repository scaffold
Create the directory tree from PLAN.md §24 with placeholder files and a top-level `README.md` describing the SDK.
**AC:** tree matches §24 exactly; every dir present; `README.md` explains what IdeaFoundry is and how to invoke it. **Deps:** none. **Traces:** §24.

### F-002 · Phase 1 · M · Lean router SKILL.md
Author `SKILL.md` as a ~250-token phase dispatch table + core rules + trigger recognition. No phase logic inline — only "for phase X, load file Y."
**AC:** measured ≤300 tokens; contains the phase→file map for all phases; contains the three triggers (`/ideafoundry`, `/foundry`, `plan with IdeaFoundry`); explicitly says examples/RECOVERY load only on condition. **Deps:** F-001. **Traces:** §6, §7.

### F-003 · Phase 1 · S · WORKFLOW.md (human phase graph)
The one file a human reads to understand the whole phase graph that the lean router deliberately omits.
**AC:** describes lifecycle §8 end-to-end; names the artifact each phase persists. **Deps:** F-002. **Traces:** §7, §8.

### F-004 · Phase 1 · M · Discovery: mandatory questions + probing rubric
Author `discovery/mandatory-questions.md` (Stage 1 six questions) and `discovery/probing-rubric.md` (Stage 2 heuristics). Encode the 8-question hard cap and Stage-3 confirmation.
**AC:** Stage 1 covers problem/user/platform/success/timeline/team; rubric is heuristics not a decision tree; 8-Q cap stated; overflow routes to `gaps_to_clarify`; buttons vs free-text guidance present. **Deps:** F-002. **Traces:** §9.

### F-005 · Phase 1 · M · Project Brief schema + IDs
Define the Brief JSON schema (`planning/brief.json`) with all §10 sections and stable section IDs (`brief.goals.g1`). Encode the no-restatement / cite-by-ID rule.
**AC:** all 12 sections present with ID convention; `gaps_to_clarify` supported; schema_version:1; token budget ≤1.5K declared. **Deps:** F-004. **Traces:** §10.

### F-006 · Phase 1 · S · Planning Confidence (traffic light)
Add the Red/Yellow/Green evaluation to the Discovery→Brief handoff; Red loops back to Discovery automatically.
**AC:** Red when a mandatory field is missing; Yellow/Green defined; Red auto-loops; band written into `state.json`/`STATUS.md`. **Deps:** F-005. **Traces:** §11.

### F-007 · Phase 1 · S · state.json + STATUS.md writer
Define `planning/state.json` (last completed phase, ~50t) and the `STATUS.md` overwrite template (§20). Write both at every phase boundary.
**AC:** `state.json` one-line; `STATUS.md` matches §20 shape; replaced not appended; ~200t/write. **Deps:** F-005. **Traces:** §19, §20.

### F-008 · Phase 1 · S · Weekend Hack profile YAML
Author `roster/profiles/weekend-hack.yaml`: specialists `[PM, Engineer]`, doc set (5), and the full `complexity_ceiling` from PLAN.md §13.
**AC:** matches §13 YAML; `reject_unless_justified` + `prefer` lists present; declares doc set. **Deps:** F-001. **Traces:** §13.

### F-009 · Phase 1 · M · Roster rubric + proposal/confirm flow
Author `roster/rubric.md` and the proposal→confirmation interaction; persist `planning/roster.json` with reasoning + overrides.
**AC:** rubric heuristics from §12; proposes with per-specialist reasoning; user can override; `roster.json` records inclusion/exclusion reasoning. For Phase 1, Weekend Hack proposes PM+Engineer. **Deps:** F-006, F-008. **Traces:** §12.

### F-010 · Phase 1 · L · Product Manager specialist
Author `specialists/product-manager.md` and the PM output schema (`planning/product.json`) with all five cross-cutting fields (`summary`, `gaps_to_clarify`, `challenges_to_brief`, `complexity_justification`, `traces_to`) and PM-specific content (features, user stories, MVP cut, roadmap, product risks). Declare needed Brief sections (partial load) and re-anchoring.
**AC:** partial Brief load (`goals, non_goals, target_users, success_metrics`); cites by ID, no restatement; produces MVP cut that visibly drops scope; all five cross-cutting fields; re-anchors from `meta.json`+deps only; token budget ≤2K. **Deps:** F-005, F-009. **Traces:** §15.

### F-011 · Phase 1 · M · Document Generator core + normalized folder
Author `generation/document-generator.md`: reads `roster.json`, loads only a template's declared `loads:` planning files, slot-fills (no re-reading specialist outputs), enforces 3K/doc cap and conditional-section omission.
**AC:** folder-based load (not blob); per-template `loads:` respected; omits (not stubs) absent sections; 3K cap enforced. **Deps:** F-010. **Traces:** §17.

### F-012 · Phase 1 · M · Templates: 12-developer-tickets + 00-executive-summary + PLAN_SUMMARY
Author the two eager-render templates plus `generation/plan-summary-template.md`. Each declares `requires:` + `loads:`. Tickets carry required `traces_to`.
**AC:** `12` loads `meta+goals+product+decisions`; every ticket has `traces_to` a goal ID; `00` is a summary ≤3K; `PLAN_SUMMARY.md` matches §17 sections; all render from `planning/` only. **Deps:** F-011. **Traces:** §17, §21.

### F-013 · Phase 1 · M · Initial-run orchestration + README index
Wire the initial run to emit `planning/` + `README.md` (doc index with status flags) + `STATUS.md` + `PLAN_SUMMARY.md` + eager `00` & `12`. Measure total tokens on a trivial Weekend Hack idea.
**AC:** end-to-end `/ideafoundry` run on a trivial idea produces all five initial artifacts; README lists all 14 docs with `available`/`not in roster`/`not yet rendered` flags; **measured initial run ≤35K** (Weekend Hack hard cap); measurement recorded to update §23. **Deps:** F-012. **Traces:** §13, §17, §23. **← Phase 1 demo.**

---

## Phase 2 — Full Team + Consensus + Profiles

### F-014 · Phase 2 · L · Senior Engineer specialist
`specialists/senior-engineer.md` + `planning/architecture.json`. Architecture/stack/APIs/schema/complexity/eng-risks. Partial Brief (`goals, constraints, timeline, team`). Enforce `complexity_justification` against the active profile ceiling.
**AC:** cites by ID; any ceiling-exceeding recommendation carries full justification quad; defaults to simplest option otherwise; ≤2K. **Deps:** F-010. **Traces:** §13, §15.

### F-015 · Phase 2 · L · UX Designer specialist
`specialists/ux-designer.md` + `planning/ux.json`. Personas, primary flows, navigation, accessibility floor, UX risks.
**AC:** cites by ID; all five cross-cutting fields; ≤2K. **Deps:** F-010. **Traces:** §15.

### F-016 · Phase 2 · L · Security Engineer specialist
`specialists/security-engineer.md` + `planning/security.json`. Threat model, authN/authZ, secrets, compliance mapping, security risks. Must *push back*, not rubber-stamp.
**AC:** cites by ID; fires `challenges_to_brief` when data-handling contradicts the Brief; compliance section gated on `brief.compliance`; ≤2K. **Deps:** F-010. **Traces:** §15.

### F-017 · Phase 2 · L · QA Engineer specialist
`specialists/qa-engineer.md` + `planning/qa.json`. Test strategy, edge cases, acceptance skeletons, release risks.
**AC:** cites by ID; all five cross-cutting fields; ≤2K. **Deps:** F-010. **Traces:** §15.

### F-018 · Phase 2 · M · Dependency-summary loading between specialists
Implement partial-context passing: a specialist loads only the `summary` fields of prior specialists it declares as dependencies (not full outputs).
**AC:** e.g. Engineer sees PM `summary` only; no full-output load unless a later conflict pull; re-anchoring preserved. **Deps:** F-014. **Traces:** §15.

### F-019 · Phase 2 · L · Consensus Coordinator — summary-first conflict detection
`consensus/coordinator.md`. Round 2: read summaries → `planning/conflicts.json`; pull full outputs only for conflicting sections.
**AC:** reads summaries first; `conflicts.json` produced; full-output pulls only on genuine disagreement; measured extra cost only when conflict exists. **Deps:** F-016, F-017, F-018. **Traces:** §16.

### F-020 · Phase 2 · M · Consensus — resolution + decisions.json + escalation batching
Round 3: resolve mechanical conflicts with rationale; batch all `challenges_to_brief` (+ any user-facing conflicts) into one escalation; write `planning/decisions.json`. 3-round hard cap.
**AC:** mechanical conflicts resolved with written reasoning; challenges + conflicts batched into a single user escalation; unresolved documented; never loops past round 3. **Deps:** F-019. **Traces:** §16.

### F-021 · Phase 2 · M · Consensus — Simplifier pass
Add the Round-3 check: every `complexity_justification` must show a real simpler alternative rejected on a **Brief constraint**; failures → `simplification_candidates` in `decisions.json`.
**AC:** "best practices"/"future-proofing" justifications flagged; Brief-grounded ones pass; ~200t cost. **Deps:** F-020. **Traces:** §16, §22.

### F-022 · Phase 2 · M · challenges_to_brief materiality gate + Brief update
Enforce the gate: only `high` surfaces to the user; `medium`/`low` → `planning/challenges_log.json`. If user accepts a high challenge, Consensus updates the Brief and re-tags affected traces.
**AC:** high = changes ≥1 MVP feature / arch choice / success metric; medium/low logged not surfaced; accepted challenge mutates `brief.json` and marks downstream stale. **Deps:** F-020. **Traces:** §15, §22.

### F-023 · Phase 2 · S · Internal Tool profile YAML
`roster/profiles/internal-tool.yaml`: `[PM, Engineer, Security]`, 8 docs, mid-width complexity ceiling.
**AC:** ceiling wider than Weekend Hack, narrower than Regulated; declares doc set. **Deps:** F-008. **Traces:** §13.

### F-024 · Phase 2 · S · Consumer App profile YAML
`roster/profiles/consumer-app.yaml`: `[PM, Engineer, UX]`, 8 docs; Security proposed if Brief indicates auth/user data.
**AC:** ceiling defined; roster rubric adds Security on auth/user-data signal. **Deps:** F-023, F-009. **Traces:** §13.

### F-025 · Phase 2 · S · Regulated profile YAML
`roster/profiles/regulated.yaml`: all five, 14 docs, wide ceiling (enterprise patterns allowed).
**AC:** all five specialists; ceiling permits queues/orchestration when justified; declares full doc set. **Deps:** F-023. **Traces:** §13.

### F-026 · Phase 2 · L · Remaining doc templates (01–11, 13) with roster gating
Author all remaining templates. Each declares `requires:` (specialists) + `loads:` (planning files). Templates referencing absent specialist output omit gracefully.
**AC:** 06 requires UX, 07 requires Security, 08 requires QA; each drops cleanly when its specialist is absent; no broken `planning.security.*` refs in a Weekend Hack render; each ≤3K. **Deps:** F-014…F-017, F-011. **Traces:** §14, §17.

### F-027 · Phase 2 · M · On-demand render (`render <doc-id>` / `render all`)
Implement `/ideafoundry render <doc-id>` (loads only declared planning files + template) and `/ideafoundry render all` (eager, with a ceiling warning on Regulated).
**AC:** single render ~2K and ≤3K; `render all` warns before proceeding on Regulated; README status flags update after render. **Deps:** F-026. **Traces:** §6, §17.

### F-028 · Phase 2 · M · Export / Continue (portable bundle)
`/ideafoundry export` → `planning-bundle.json` (keys = filenames). `/ideafoundry continue` reconstitutes the folder from a pasted bundle and regenerates views.
**AC:** round-trip export→continue reproduces the folder byte-for-byte; teammate flow works (continue on a fresh session → render tickets); bundle is the only state needed. **Deps:** F-013. **Traces:** §5.

### F-029 · Phase 2 · S · help / status subcommands
`/ideafoundry help` (subcommand list + current phase) and `/ideafoundry status` (print STATUS.md).
**AC:** help lists all subcommands from §6 and shows current phase; status prints STATUS.md. **Deps:** F-007, F-013. **Traces:** §6, §20.

### F-030 · Phase 2 · M · Full-team Regulated run + budget measurement
Run all four profiles end-to-end; measure per-phase and per-profile tokens; reconcile against §23 (within ~10%); update the tables with the calibration multiplier.
**AC:** Regulated initial run ≤55K; each profile within its hard cap; per-phase table reconciles with per-profile totals ±10%; §23 updated with measured numbers. **Deps:** F-021…F-027. **Traces:** §23. **← Phase 2 demo.**

---

## Phase 3 — Amendment + Recovery + Evaluation

### F-031 · Phase 3 · L · Traceability graph + backward staleness walk
Formalize the `traces_to` graph across Brief → specialist outputs → docs; implement backward-walk to find everything downstream of a changed field.
**AC:** given a changed Brief ID, returns the set of stale specialist outputs + docs; used by both Amendment and challenge-accept. **Deps:** F-022. **Traces:** §18, §21.

### F-032 · Phase 3 · L · Amendment phase
`/ideafoundry amend <note>` → write `planning/amendments/NNN-note.json`, compute invalidated IDs, tag `stale:true` on affected planning files, rerun only affected specialists, mark derived docs stale in README (no eager regen).
**AC:** typical amendment touches 3–8 IDs, reruns 1–2 specialists; docs marked stale not regenerated; measured ≤15K. **Deps:** F-031. **Traces:** §18.

### F-033 · Phase 3 · S · Lazy stale-doc regeneration on read
A doc marked stale regenerates on next `render`, then clears its stale flag.
**AC:** rendering a stale doc regenerates from current `planning/` and flips flag to `available`. **Deps:** F-032, F-027. **Traces:** §17, §18.

### F-034 · Phase 3 · M · RECOVERY.md + error artifacts
`rules/RECOVERY.md` (~1K), loaded only on an error condition. Cover the five §19 cases; define `planning/errors/<role>.json`.
**AC:** each §19 case has a documented behavior; malformed JSON re-prompts once then degrades; token-exceed writes `WARNINGS.md`, never silent; RECOVERY not loaded on happy path. **Deps:** F-019. **Traces:** §19.

### F-035 · Phase 3 · S · Resumption via state.json
`/ideafoundry continue` (no bundle) reads `state.json`, reports last completed phase, asks whether to proceed.
**AC:** after an abandoned mid-run, continue finds the last phase and offers resume. **Deps:** F-007, F-028. **Traces:** §19.

### F-036 · Phase 3 · S · planning-rules.md + mvp-rules.md
Author the shared rules files specialists reference for MVP-cutting discipline and general planning constraints.
**AC:** MVP rules force a real scope cut; planning rules encode cite-by-ID, no-restatement, simplest-default; each declares a token budget. **Deps:** F-010. **Traces:** §3, §22.

### F-037 · Phase 3 · L · Worked example: Internal Tool run (on-disk only)
Author `examples/internal-tool-run/` — a complete `planning/` folder + rendered docs for one Internal Tool idea. `examples/README.md` describes the other profiles' run shapes in prose.
**AC:** example is structurally valid against all schemas; on-disk only (zero runtime tokens); SKILL.md references it only when an output looks structurally wrong. **Deps:** F-026. **Traces:** §25.

### F-038 · Phase 3 · M · Eval harness + fixtures
Build `evals/` runner that executes the four EVAL.md test-idea prompts, captures per-phase + profile token usage, and checks rubric assertions.
**AC:** runs all four evals; reports token usage per phase and per profile; asserts pass criteria including the complexity-ceiling check. **Deps:** F-030, F-032. **Traces:** EVAL.md.

### F-039 · Phase 3 · M · Anti-over-engineering eval (Weekend Hack)
Implement EVAL #1 assertions: Engineer must not recommend Kubernetes/Redis/microservices/custom-auth/queue without a Brief-grounded `complexity_justification`; defaults must be SQLite/single-instance/library-auth/cron.
**AC:** run fails if any ceiling item appears unjustified; passes on simplest-default output; UX+Security proposed-and-declined with captured reasoning. **Deps:** F-038. **Traces:** EVAL §1, §13.

### F-040 · Phase 3 · M · Roster-graceful-degradation eval
Assert a template with optional deps renders cleanly with the specialist absent — no `planning.security.*` refs when Security isn't in the roster.
**AC:** Weekend Hack render of a security-referencing template omits the section with a note; zero broken references. **Deps:** F-038, F-026. **Traces:** §14, EVAL.

### F-041 · Phase 3 · M · Amendment eval + budget gate
Implement EVAL #4: from a completed Consumer App run, `amend "support offline mode"` → 2–3 outputs stale, PM+Engineer rerun, 4–5 docs regenerated on read, others untouched, total <15K.
**AC:** correct staleness set; only affected specialists rerun; untouched artifacts byte-identical; measured <15K; run fails if budget exceeded even with good docs. **Deps:** F-032, F-038. **Traces:** §18, EVAL §4. **← Phase 3 demo.**

---

**Backlog total: 41 tickets** (13 / 17 / 11). Sizing: 9 L, 18 M, 14 S. No filler — each ticket is a real, demoable slice.
