# IdeaFoundry — PLAN.md

> **What this is.** IdeaFoundry is a Claude Skill that turns an incomplete software idea into an execution-ready planning package. It is an AI-powered virtual product team — PM, Engineer, UX, Security, QA — coordinated by a methodology, not an agent framework. The product is *clarity*, not code. IdeaFoundry never writes application code; it produces the plan that comes before code.
>
> **Read this in 15 minutes.** Sections are ordered so a Staff engineer can stop after any one and still have a coherent mental model. Every engineering decision states what else was considered and the tradeoff, one paragraph.

---

## 1. Vision

Current AI coding assistants generate code well but assume the user already knows *what* to build, *who* for, what belongs in the MVP, and how to slice the work. That assumption is usually false. IdeaFoundry fills the gap: describe an idea, participate in a right-sized workshop, receive a folder that a human team or a coding assistant can execute against. It scales down to an indie dev's weekend hack and up to a regulated production build **without changing what it is** — the same methodology, a different roster.

Success looks like: install the Skill, type `/ideafoundry`, answer ≤8 questions, confirm a proposed roster, receive `PLAN_SUMMARY.md` + `12-developer-tickets.md` + a normalized `planning/` folder — under 60K tokens, every time.

## 2. Problem Statement

Planning tools fail in four predictable ways, and IdeaFoundry is architected against each:

1. **They over-scope.** A weekend hack gets a Kubernetes recommendation. → Profile-scoped complexity ceilings + `complexity_justification` enforcement.
2. **They over-produce.** 14 documents nobody reads, paid for in tokens upfront. → Mostly-lazy generation; eager render only the 2 docs 90% of users open first.
3. **They rubber-stamp.** The LLM agrees with the user's Brief instead of challenging it. → `challenges_to_brief` with a materiality gate; Security is *mandatory* for regulated/production regardless of what the user asked.
4. **They assume one-shot execution.** Reality changes; the plan can't absorb it; the tool is used once. → Amendment is a first-class phase.

## 3. Philosophy

**Think before you build.** The methodology *is* the product; specialists are implementations of it. Design this as a structured software-planning framework that happens to be executed by an LLM — not as an "agent framework." Every principle that says "the model shouldn't do X" ships with an enforcement mechanism (see §22). Principles without mechanisms are decorative.

## 4. Runtime Constraints

IdeaFoundry is a **Claude Skill**: stateless prompt files, templates, and rules. No message bus, no persistent agent memory, no scheduler, no server. "Coordination" happens because Claude reads the artifacts folder and follows `SKILL.md`. A "round" is not a running process — it is a discrete pass that produces a **persisted artifact** on disk. Everything that must survive between turns lives in files.

The repository is a reusable planning **SDK**, not an application.

## 5. Persistence Model — planning/ as Portable State

Claude Skills have no user-controlled filesystem that persists between sessions. IdeaFoundry's persistence is explicit and honest:

- The **`planning/` folder is the portable state** — the crown jewel. Everything else (`STATUS.md`, `README.md`, `PLAN_SUMMARY.md`, rendered `docs/`) is a *view* derived from it.
- **`/ideafoundry export`** bundles the folder into `planning-bundle.json` — one JSON object whose keys are the folder's filenames and whose values are their contents. Downloadable, single file.
- **`/ideafoundry continue`** reconstitutes the folder from a pasted bundle and regenerates views. This is how a user resumes in a new chat, and how a teammate picks up a shared plan (export → send → `continue` on their own account → `render tickets`).

> **Decision — bundle over "trust the chat scrollback."** *Alternative:* rely on conversation history to carry state. *Rejected:* history is lossy, gets summarized after ~20 turns, and can't be handed to a teammate. The bundle is deterministic and portable. *Tradeoff:* the user must copy/paste a JSON blob — acceptable for a heavyweight, multi-turn tool.

## 6. Invocation Model — Explicit Triggers Only

IdeaFoundry activates **only on an explicit trigger**. Its Skill description does **not** use semantic auto-activation. Triggers:

- `/ideafoundry` — canonical.
- `/foundry` — short form for repeat users.
- `plan with IdeaFoundry` — natural-language fallback for mobile.

Absent a trigger, Claude behaves normally.

> **Decision — invert the usual "pushy trigger" advice.** *Alternative:* fire when the user "seems to want planning." *Rejected for this Skill:* IdeaFoundry is a heavyweight multi-turn commitment. A false positive (Discovery interrogation when the user wanted a two-sentence answer) is far worse than a false negative (user forgets to invoke once and re-types it). *Tradeoff:* lower discoverability, bought back by the `help` subcommand.

**Subcommand surface** (recognized only *after* the base trigger):

| Command | Purpose |
|---|---|
| `/ideafoundry` | New session (Discovery + profile picker) |
| `/ideafoundry <profile>` | Start with a named profile |
| `/ideafoundry amend <note>` | Amendment phase |
| `/ideafoundry render <doc-id>` | Render one on-demand doc |
| `/ideafoundry render all` | Render every roster doc eagerly (opt-in) |
| `/ideafoundry status` | Print current `STATUS.md` |
| `/ideafoundry export` | Package `planning/` for download |
| `/ideafoundry continue` | Resume from a pasted bundle |
| `/ideafoundry help` | List subcommands + current phase |

Every internal capability — Amendment, on-demand rendering, resumption — is **discoverable via one `help` command**. First-run confusion, "how do I get the other docs," and Amendment discovery all collapse into one learnable pattern: type `/ideafoundry` and go.

## 7. Progressive Disclosure Model

`SKILL.md` is a **lean router (~250 tokens)**: a phase dispatch table plus core rules, nothing more. It tells Claude which file to load for the current phase. Specialist prompts, templates, rubrics, rules, and examples load **on demand, never all at once**. Every turn pays the router cost, so the router stays small — that cost compounds across a 15+ turn Regulated run.

> **Decision — lean router over fat manifest.** *Alternative:* one `SKILL.md` containing all rules and phase logic. *Rejected:* it would load ~3K every turn × 15+ turns = pure waste. *Tradeoff:* logic is spread across `discovery/`, `roster/`, `specialists/`, `consensus/`, `generation/`, `rules/` — mitigated by `WORKFLOW.md`, the one file that describes the whole phase graph for a human reader.

## 8. User Lifecycle

```
User describes an idea
  → Interactive Discovery (≤8 questions)
  → Project Brief (single source of truth)
  → Roster Selection (skill proposes, user confirms)
  → Specialist Review (only the roster's specialists, one per turn)
  → Consensus (coordinator, not a specialist)
  → Document Generation (planning/ + 2 eager docs; rest lazy)
  → Execution-Ready Project
  ↺ Amendment (re-planning when reality changes)
```

The Amendment loop is not optional. A planning tool that can't absorb new information gets used once.

## 9. Discovery Architecture

Three stages, conversational (not a form). Some questions use `ask_user_input_v0` buttons, some free-text. Follow-ups allowed when an answer changes the framing.

- **Stage 1 — Mandatory questions.** Problem, target user, platform, success criteria, timeline, team size. Always asked.
- **Stage 2 — Adaptive probing.** Governed by a **probing rubric** (`discovery/probing-rubric.md`), *not* a domain decision tree. Heuristics: *regulated domain → probe compliance regime; <13 audience or health data → probe applicable law; AI-native → probe model provider, latency budget, inference cost.* The rubric encodes judgment; branches rot, rubrics generalize.
- **Stage 3 — Confirmation.** Summarize into a draft Brief, show the user, allow correction before proceeding.

**Hard cap: 8 questions.** User energy for planning falls off a cliff after Q5; Q6–Q8 are worthwhile only if genuinely load-bearing. Reaching for Q9 is the signal to stop, draft the Brief, and flag the gaps in `gaps_to_clarify` for specialists to raise later.

> **Decision — rubric over decision tree.** *Alternative:* encode "if health → ask A, B, C; if fintech → ask D, E." *Rejected:* domain trees are infinite and stale on arrival. *Tradeoff:* rubric quality depends on the model's judgment, which we accept and constrain with the ≤8 cap and the confirmation gate.

## 10. Project Brief Model

Single source of truth. Every specialist works **exclusively** from it. Contents: Vision, Problem Statement, Target Users, Goals, Non-Goals, Constraints, Timeline, Team, Budget, Success Metrics, Assumptions, Risks.

Each section carries a **stable ID** — `brief.goals.g1`, `brief.constraints.c3`. Specialists **cite by ID and must not restate Brief content**; downstream consumers dereference the ID. Restatement is a **schema violation**.

**Partial Brief loading.** Each specialist prompt declares which sections it needs — PM: `goals, non_goals, target_users, success_metrics`; Engineer: `goals, constraints, timeline, team`; Security: `constraints, target_users, assumptions`. Only those sections load into that specialist's context. Loading the whole Brief every turn is waste; a specialist doesn't reason over `brief.budget` unless flagged.

## 11. Planning Confidence — Traffic Light, Not Percentage

Three bands, no arithmetic:

- **Red** — mandatory Brief fields missing. Cannot proceed. Discovery loops back automatically.
- **Yellow** — mandatory present, discretionary sparse. Proceed with warnings.
- **Green** — both dense. Proceed.

> **Decision — bands over a percentage.** *Alternative:* "planning confidence 82%." *Rejected:* invites "why 82 and not 85" arguments and implies false precision. *Tradeoff:* less granular — which is the point.

## 12. Roster Selection — Proposal + Confirmation

Not every project needs all five specialists. Forcing a 50K full-team run on a weekend hack is why over-scoped tools go unused. After the Brief is confirmed, the Skill **proposes** a roster with per-specialist reasoning; the user **confirms or overrides**.

Proposal comes from a **roster rubric** (`roster/rubric.md`), heuristics not branches:

- Regulated domain (health, finance, kids, EU-personal-data) → **Security mandatory**.
- Consumer-facing with >1 user type → **UX mandatory**.
- Any production deployment with real users → **Security mandatory**, regardless of domain.
- Solo dev + weekend timeline → QA droppable; PM + Engineer suffice.
- Internal tool, small user base → UX droppable.

Persisted as `planning/roster.json` — specialist list, reasoning per inclusion/exclusion, user overrides.

> **Decision — proposal+confirmation over pure-auto or pure-manual.** *Pure user-picks* fails because users don't know what they don't know (the person building a health app skips Security *because* they aren't thinking about HIPAA). *Pure auto-select* is paternalistic. Proposal+confirmation preserves agency, uses Claude's judgment, and **teaches** when it recommends a specialist the user didn't ask for. *Tradeoff:* one extra confirmation turn.

## 13. Project Profiles — Roster Presets + Complexity Ceilings

Most users don't want to assemble a roster from scratch. Ship named profiles as YAML (`roster/profiles/`):

| Profile | Specialists | Docs available | Initial run | Typical read (+3–5 docs) |
|---|---|---|---|---|
| **Weekend Hack** | PM, Engineer | 5 | ~26K | ~30K |
| **Internal Tool** | PM, Engineer, Security | 8 | ~34K | ~40K |
| **Consumer App** | PM, Engineer, UX | 8 | ~34K | ~40K |
| **Regulated / Production** | all five | 14 | ~46K | ~52K |
| **Custom** | user picks | derived from roster | varies | varies |

**Initial run** always produces: the `planning/` folder, `README.md`, `STATUS.md`, `PLAN_SUMMARY.md`, and **eager renders of `00-executive-summary.md` and `12-developer-tickets.md`** (the two docs 90% read first). Everything else renders on demand.

**Complexity ceilings.** Each profile YAML declares a ceiling — architectural elements a specialist must *justify against a Brief constraint* before recommending. `weekend-hack.yaml`:

```yaml
complexity_ceiling:
  reject_unless_justified:
    - message queues
    - container orchestration (Kubernetes, Nomad)
    - multi-service architectures
    - dedicated cache layers (Redis, Memcached)
    - custom authentication systems (use library defaults)
    - distributed databases
    - event sourcing / CQRS
  prefer:
    - SQLite over Postgres
    - server-rendered HTML over SPA
    - cron over job queues
    - library defaults over custom
```

`regulated.yaml` has a wider ceiling (enterprise patterns are appropriate for regulated production); `internal-tool.yaml` sits between. Enforcement is via the `complexity_justification` field: any recommendation matching a `reject_unless_justified` entry **without** justification is a schema violation. **This is the mechanism that stops IdeaFoundry from suggesting Kubernetes for a habit tracker** — the most visible way this tool could look silly in public.

## 14. Doc Set Derivation

The 14-doc set is a **maximum, not a minimum**. The roster subtracts:

- No Security → no `07-security-review.md`.
- No UX → no `06-ux-specification.md`, and the PRD skips its UX sections.
- No QA → no `08-test-strategy.md`.

**Every template declares its dependencies at the top** — `requires: [engineer, security]` (specialists) and `loads: [meta, brief, security, decisions]` (planning files). The Document Generator reads `roster.json`, drops templates whose `requires` are unsatisfied, and gates sections within surviving templates by the same mechanism. This is a **schema-level constraint**: a template that references an absent specialist's output (`planning.security.authn_approach` when Security isn't in the roster) must fail gracefully — omit the section with a note, never emit a broken reference. Regulated-only templates must not break Weekend Hack.

## 15. Specialist Architecture

Five specialists, roster-selected per run. Each answers **one crisp question** and emits a **structured planning object (JSON)**, not prose. Each claim cites the Brief ID it draws from; no restatement.

| Specialist | Question | Owns |
|---|---|---|
| **Product Manager** | Does this solve the user's problem? | Features, user stories, MVP cut, roadmap, product risks |
| **Senior Engineer** | Can this realistically be built? | Architecture, stack, APIs, schema, complexity, engineering risks |
| **UX Designer** | Can users accomplish their goals easily? | Personas, primary flows, navigation, accessibility floor, UX risks |
| **Security Engineer** | Can this be deployed safely? | Threat model, authN/authZ, secrets, compliance mapping, security risks |
| **QA Engineer** | Can this be shipped confidently? | Test strategy, edge cases, acceptance skeletons, release risks |

**Five cross-cutting schema fields** on every specialist output:

- **`summary: string`** — ~150-token précis of conclusions and stakes-in-the-ground. Consumed by Consensus and downstream specialists to decide whether to load the full output. Cheap conflict detection lives here.
- **`gaps_to_clarify: []`** — Brief was silent on something needed. **Blocks generation** until resolved.
- **`challenges_to_brief: []`** — specialist thinks the Brief itself is wrong: `{brief_section_id, concern, recommendation, impact: high|medium|low}`. **Only `high` surfaces to the user by default; `medium`/`low` are logged to `planning/challenges_log.json`.** `high` = "if accepted, changes ≥1 MVP feature, ≥1 architectural choice, or ≥1 success metric." This **materiality gate** is the defense against pushback-as-noise — LLMs will challenge *something* every run; without a threshold, users disable the feature.
- **`complexity_justification: []`** — anti-over-engineering enforcement. Any recommendation exceeding the profile ceiling must carry `{recommendation, why_needed, simpler_alternative_considered, why_rejected}`. Anything not listed is presumed the simplest option satisfying the Brief. LLM specialists are trained on "best practices" content that assumes enterprise scale; without this field, Engineer reaches for Kubernetes on a habit tracker. With it, Engineer must justify against a Brief constraint or default to SQLite + cron.
- **`traces_to: []`** — Brief IDs this output derives from. Powers Amendment staleness.

**Re-anchoring rule.** At the start of each specialist turn, the *only* prior context that matters is `planning/meta.json` + the specialist's declared dependency files. **Prior conversation is not consulted.** This exploits file-based state to sidestep long-conversation degradation: Claude's outputs get noticeably worse after ~20 turns, and a full Regulated run has 15+ specialist turns before Consensus. Re-anchoring keeps every turn effectively fresh.

**Execution model.** Specialists run **one per turn, in separate contexts**. Each sees only: its relevant Brief sections (partial load), its own prompt (loaded on demand), and the *summaries* of prior specialists it explicitly depends on. PM does not see Engineer's prompt. **Loading all five prompts into one context is the anti-pattern.**

> **Decision — structured JSON output over prose.** *Alternative:* specialists write markdown directly. *Rejected:* prose can't be gated, cited, diffed for staleness, or rendered deterministically; it also duplicates Brief content. JSON gives us traceability, the materiality gate, and slot-fill rendering. *Tradeoff:* a rendering step is required (the Document Generator) — worth it.

## 16. Consensus Coordinator

A **coordinator, not a specialist**. Responsibilities:

1. Read specialist **summaries first** — not full outputs (that is the entire point of the `summary` field).
2. Detect conflicts from summaries → `planning/conflicts.json`; pull full outputs **only for sections that genuinely disagree**.
3. Resolve mechanical conflicts (scope disagreements) with written rationale; escalate genuine business tradeoffs to the user.
4. Batch **all** `challenges_to_brief` into the *same* user escalation; update the Brief if the user accepts a challenge.
5. Produce `planning/decisions.json` and the finalized `planning/` folder.

**Simplifier pass** (part of Round 3): for every recommendation in every `complexity_justification`, verify a simpler alternative was *actually* considered and the rejection is grounded in a **Brief constraint** — not "best practices" or "future-proofing." Failures are flagged as `simplification_candidates` in `decisions.json` for user review. This is anti-over-engineering enforcement at the coordinator level (specialists produce the justification; Consensus verifies it holds). Cost ~200 tokens, disproportionate quality impact.

**Round semantics** (each round produces a persisted artifact):

- **Round 1** — each specialist writes `planning/<role>.json` (separate turns).
- **Round 2** — Consensus reads summaries → `planning/conflicts.json`; pulls full outputs only on conflict.
- **Round 3** — Consensus resolves each conflict/challenge with written rationale → `planning/decisions.json`; unresolved items → batched user escalation.

**Hard cap: 3 rounds.** Consensus does not loop. Every unresolved conflict is documented; every decision includes reasoning.

## 17. Document Generator — Normalized planning/, Mostly Lazy

Specialists emit structured objects; something must render them to markdown — **not eagerly, and not from a single blob.**

**The planning folder is normalized, not a monolith.** A single `planning.json` on a Regulated build balloons to 15–20K, which breaks the on-demand render math. Instead:

```
planning/
  meta.json           ~0.5K  version, roster, timestamps, schema_version
  brief.json          ~1.5K  confirmed Brief
  goals.json          ~1K    business goals + traceability roots
  roster.json         ~0.5K  roster + reasoning + overrides
  product.json        ~2K    PM output
  architecture.json   ~2K    Engineer output
  ux.json             ~2K    UX output          [if in roster]
  security.json       ~2K    Security output    [if in roster]
  qa.json             ~2K    QA output          [if in roster]
  decisions.json      ~1K    Consensus resolutions
  challenges_log.json ~0.5K  medium/low challenges (on-demand only)
  conflicts.json      ~0.5K  Consensus round-2 output
  state.json          ~50t   last completed phase (resumption)
```

Each template declares the planning files it needs. `12-developer-tickets.md` loads `meta + goals + product + decisions` ≈ 4.5K. `07-security-review.md` loads `meta + brief + security + decisions` ≈ 5K. Neither pays the full-planning cost. *(Throughout this doc "`planning.json`" is shorthand for the folder.)*

**Initial run generates five things:** the `planning/` folder, `README.md`, `STATUS.md`, `PLAN_SUMMARY.md`, and **eager renders of `00-executive-summary.md` + `12-developer-tickets.md`**. These transform the first impression from "the AI didn't do the work" to "here's my plan." All other docs stay lazy.

**`PLAN_SUMMARY.md`** — auto-generated human one-pager (~2K). Sections: *what we're building* (`brief.vision`), *MVP feature list* (`product.mvp`), *timeline & approach* (`architecture.approach` + roadmap), *top-3 risks* (aggregated across specialist risk fields), *open decisions requiring input* (Consensus escalations). This is the doc the founder/PM opens; the JSON is the doc engineers open.

**On-demand rendering.** `/ideafoundry render <doc-id>` loads only that template's declared planning files + the template, produces the doc (~1.5–2.5K). A typical user reads 3–5 of 14 docs, so most doc-generation cost is never paid.

**Rendering is slot-fill, not synthesis.** The Generator does **not** re-read specialist outputs per doc — everything it needs is in the normalized folder. **Conditional sections** are gated by Brief/planning flags: if `brief.compliance = none`, compliance sections are **omitted entirely, not stubbed with "N/A"** — filler is a token tax paid every render.

**Hard cap: no single doc exceeds 3K tokens.** If a doc wants to be larger, split it or push detail into `planning/` (where it lives once, referenced by ID).

**`/ideafoundry render all`** — escape hatch for users who need the whole folder now (handing off to a coding assistant, exporting for a client). Costs the equivalent of eager generation; on Regulated it warns it may approach the ceiling.

> **Decision — normalized folder over single planning.json.** *Alternative:* one blob. *Rejected:* the blob defeats lazy rendering (every render loads everything) and blows render math on large builds. *Tradeoff:* more files to manage — handled by per-template `loads:` declarations.

## 18. Amendment Phase

The blind spot in most planning tools: they assume one-shot execution. Amendment is first-class, not a rerun.

1. User invokes `/ideafoundry amend <note>` (e.g., "Stripe rate limits are 100/sec not 1000/sec, need to rethink batching").
2. Skill writes `planning/amendments/NNN-note.json` — description + timestamp.
3. Claude walks the **traceability graph** to find which Brief sections and specialist outputs the change **invalidates**; tags them stale in the relevant `planning/` files (`architecture.json` → `stale: true`). Typical: 3–8 IDs.
4. Re-runs **only the affected specialists** (usually 1–2) against the amended Brief.
5. Marks derived docs **stale in `README.md`** but **does not regenerate them eagerly** — regeneration happens the next time each doc is read.

Token cost per typical amendment: **8–12K** (down from a full rerun; docs aren't eagerly regenerated).

**Not built:** diff engine, rollback UI, merge-conflict resolver. Amendments accumulate as a numbered folder; history is `ls planning/amendments/`; rollback is `git revert`. **Do not reinvent version control inside the Skill.**

## 19. Failure Modes and Recovery

Every phase has documented failure behavior in one file, `rules/RECOVERY.md` (~1K), **loaded only when SKILL.md detects an error condition** — zero cost on the happy path.

| Failure | Behavior |
|---|---|
| **Malformed specialist JSON** | Re-prompt once with the schema; if still bad, write `planning/errors/<role>.json` and continue without that specialist. Consensus notes the gap. |
| **Consensus can't resolve after 3 rounds** | Remaining conflicts batched as user escalation. No looping. |
| **User abandons mid-run** | Every phase writes its artifact before ending. `state.json` (one line, written after each phase) records the last completed phase; `/ideafoundry continue` reads it and asks whether to proceed. |
| **Template references absent specialist** | Roster gating handles it; if it fails anyway, doc omitted with a note in `README.md`. |
| **Token budget exceeded mid-phase** | Phase completes, writes to `WARNINGS.md`, run continues. **Never silent.** |

`state.json` is ~50 tokens, always-on, negligible.

## 20. STATUS.md — Planning Dashboard

Every session has two audiences: the person planning (Discovery-time) and the person/AI building (post-generation). The 14 docs serve the second; the first needs orientation *while planning*. At the end of **every phase**, overwrite `STATUS.md` at project root:

```
Phase: Consensus (3/5 conflicts resolved)
Roster: PM, Engineer, Security
Confidence: Green
Open escalations: 2
Last update: <timestamp>
Next: user decides on auth approach → resume with `/ideafoundry continue`
```

~200 tokens per write, **replaced not appended** (~1.5K per full run). Orientation without a UI.

## 21. Traceability Model

Every artifact connects back to the originating business goal:

```
Business Goal → Feature → Epic → Story → Ticket → Acceptance Criteria
```

Every ticket carries the goal ID it serves via a required **`traces_to`** field. The same graph powers Amendment: walking edges **backward** from a changed field identifies everything downstream that needs re-review. One graph, two uses (explainability + staleness).

## 22. Enforcement Mechanisms

Every "should not" principle maps to a mechanism. Principles without mechanisms are decorative.

| Principle | Mechanism |
|---|---|
| Specialists don't invent | Brief citations by ID; `gaps_to_clarify` blocks on silence |
| Specialists don't restate the Brief | Schema forbids Brief content in output; citations only |
| Specialists can challenge the Brief | `challenges_to_brief`, materiality-gated, batched by Consensus |
| Specialists don't over-engineer | `complexity_justification` vs profile ceiling; Consensus Simplifier pass |
| No contradictions across docs | All docs render from one `planning/` folder |
| Every ticket traces to a goal | Required `traces_to` field |
| Template must not reference absent specialist | Roster gating in template header + section gating within |
| Discovery doesn't exhaust the user | 8-question hard cap; overflow → `gaps_to_clarify` |
| Consensus doesn't loop forever | 3-round hard cap; unresolved → user escalation |
| No doc bloat | 3K per-doc cap; detail pushed into `planning/` |

## 23. Token Budget — First-Class Constraint

**Non-negotiable: every Skill invocation completes under 60K tokens.** Derived bottom-up from phase math, not top-down aspiration.

**Per-phase costs** (lean router, partial Brief loading, summary-first Consensus, normalized folder, eager 2-doc + PLAN_SUMMARY):

| Phase | Typical | Notes |
|---|---|---|
| Router (per turn) | ~0.25K | Lean SKILL.md |
| Discovery + Brief (≤8 Q) | 5–7K | Brief output 1–2K |
| Roster Selection | ~2K | Rubric + proposal + roster.json |
| Specialist turn — first (no deps) | 3–4K | Partial Brief + prompt + own output |
| Specialist turn — 1–2 dep *summaries* | 4–6K | Summaries, not full outputs |
| Full-output pull for a conflicting section | +1–2K | Only when needed |
| Consensus (2-specialist roster) | ~3K | Summary-first |
| Consensus (5-specialist roster) | ~8K | Scales with roster + conflict density |
| Initial generation (planning/ + README + STATUS + PLAN_SUMMARY + 2 eager docs) | 9–13K | Roster-independent |
| On-demand doc render (per doc) | ~2K | Pay for what you read |
| STATUS + state overhead | ~1.5K per run | Always-on |
| Amendment (1–2 specialists, docs stale) | 8–12K | Regeneration deferred |
| `/render all` (opt-in) | +10K to +25K | Only if requested |

**Per-profile totals** (bottom-up; initial run includes eager `00`, `12`, and `PLAN_SUMMARY`):

| Profile | Initial run | Hard cap | Typical read (+3–5) | Full via `render all` |
|---|---|---|---|---|
| Weekend Hack | ~26K | 35K | ~30K | ~34K |
| Internal Tool | ~34K | 45K | ~40K | ~48K |
| Consumer App | ~34K | 45K | ~40K | ~48K |
| Regulated | ~46K | 55K | ~52K | ~65K |

**Numbers must reconcile.** Adding per-phase costs for a roster must land within ~10% of the profile total. If the tables disagree, one is wrong.

The **60K ceiling holds for every single invocation** in normal use. `render all` on Regulated warns before proceeding.

**Calibration caveat.** These are pre-implementation phase math. Claude's context management, tool-use overhead, and retries typically add **15–25%** to bottom-up estimates. **Phase 1 must measure a real Weekend Hack run and update these numbers before the design is published as authoritative.**

If a phase or profile blows its cap in practice, **fix the schema** (shrink outputs, split templates, push detail into `planning/`). **Do not raise the cap** — the budget is the forcing function. Every specialist output schema, every template, every rules file declares a token budget at the top and is reviewed against it.

## 24. Repository Structure

```
ideafoundry/
  README.md
  SKILL.md                       ← lean router, ~250 tokens
  WORKFLOW.md                    ← whole phase graph, for humans
  discovery/
    mandatory-questions.md
    probing-rubric.md
  roster/
    rubric.md
    profiles/
      weekend-hack.yaml
      internal-tool.yaml
      consumer-app.yaml
      regulated.yaml
  specialists/
    product-manager.md           ← declares Brief sections + dep summaries
    senior-engineer.md
    ux-designer.md
    security-engineer.md
    qa-engineer.md
  consensus/
    coordinator.md
  generation/
    document-generator.md
    plan-summary-template.md
    templates/                   ← each declares requires: + loads:
  rules/
    planning-rules.md
    mvp-rules.md
    RECOVERY.md                  ← loaded only on error
  examples/
    internal-tool-run/           ← one full worked example (on-disk only)
    README.md                    ← describes shape of other profiles
  evals/
```

Feels like a reusable planning SDK, not a prompt dump.

## 25. Examples Policy

Ship **one** fully-worked example: the **Internal Tool** profile (3 specialists including Security — non-trivial but not overwhelming). **Do not ship one per profile.** Examples are **on-disk-only** — zero runtime tokens. `SKILL.md` instructs Claude to reference examples **only** when a specialist output looks structurally wrong; otherwise they never load. `examples/README.md` describes the shape of the other profiles' runs in prose so contributors understand coverage without paying for four full example folders.

## 26. Configuration

- **Profiles** are YAML in `roster/profiles/`; adding a profile is adding a file — no code change.
- **Complexity ceilings** live inside each profile YAML; tuning "what counts as over-engineering" is editing a list.
- **Token budgets** are declared at the top of every schema/template/rules file and reviewed against §23.
- **Model behavior** is governed by prompts + rubrics, not settings — the Skill has no runtime config surface beyond files.

## 27. Versioning

Each artifact carries `schema_version: 1`. v1 does not implement migrations — the field is a placeholder so v2 can. `meta.json` records the schema version of a run so a future `continue` can detect and (in v2+) migrate an older bundle.

## 28. Future Roadmap

**Additional specialists, no redesign** (different profiles assemble different teams): DevOps, ML Engineer, Data Engineer, Solutions Architect, Marketing, Technical Writer, Legal, Business/GTM, Ops. Naming them makes the extension path real: adding one is a `specialists/<role>.md` + a template + a roster-rubric line + profile membership.

**Deferred to v2/v3:** schema migrations (placeholder present in v1); a generated `HANDOFF.md` explaining reading order for AI coding assistants; enterprise data-handling notes; a diff view over amendments (still not a merge engine).

## 29. Key Engineering Decisions — Summary Ledger

| Decision | Alternative rejected | Tradeoff accepted |
|---|---|---|
| Explicit trigger only | Semantic auto-activation | Lower discoverability; bought back by `help` |
| Lean ~250t router | Fat single SKILL.md | Logic spread across files; `WORKFLOW.md` mitigates |
| Structured JSON specialist output | Prose | Rendering step required |
| Summary-first Consensus | Read all full outputs | Summary must be trustworthy; schema-enforced |
| Normalized planning/ folder | Single planning.json | More files; per-template `loads:` handles it |
| Mostly-lazy generation | Eager 14-doc render | Users must ask for docs; `help` + README index teach it |
| Traffic-light confidence | Percentage | Less granular (intentionally) |
| Proposal+confirm roster | Auto or manual | One extra turn |
| Profile complexity ceilings | Trust the model | Ceiling lists need maintenance |
| Materiality gate on challenges | Surface all challenges | High-bar tuning; medium/low still logged |
| Bundle export/continue | Trust chat scrollback | User copies a JSON blob |
| One worked example | One per profile | Less coverage; `examples/README.md` describes the rest |

**Overall goal.** An open-source planning operating system for software teams — usable by indie devs on weekend hacks and by product teams on regulated builds without changing what it is. Install the Skill, describe an idea, participate in a right-sized workshop, receive an execution-ready folder. When reality changes, amend rather than restart.
