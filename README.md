# IdeaFoundry

**Turn an incomplete software idea into an execution-ready planning package.**

IdeaFoundry is a [Claude Skill](https://docs.claude.com/en/docs/claude-code/skills): a reusable software-planning **SDK** — prompt files, schemas, rubrics, and templates — that coordinates a virtual product team (PM, Engineer, UX, Security, QA) to produce *the plan that comes before the code*. It never writes application code. The product is **clarity**.

It scales **down** to an indie dev's weekend hack and **up** to a regulated production build without changing what it is — same methodology, a different roster.

## Install

Copy this folder into your Claude skills directory (or point Claude Code at it as a project skill). No dependencies, no server, no build step — it is prompt files and rules.

## Use

```
/ideafoundry            # new session — Discovery + profile picker
/foundry                # short form
plan with IdeaFoundry   # natural-language fallback
```

Answer ≤8 Discovery questions → confirm a proposed roster → receive a `planning/` folder plus `PLAN_SUMMARY.md`, `README.md` (doc index), `STATUS.md`, and eager renders of `00-executive-summary.md` + `12-developer-tickets.md`. Every invocation stays **under 60K tokens**.

### Subcommands

| Command | Purpose |
|---|---|
| `/ideafoundry` | New session (Discovery + profile picker) |
| `/ideafoundry <profile>` | Start with a named profile (`weekend-hack`, `internal-tool`, `consumer-app`, `regulated`) |
| `/ideafoundry amend <note>` | Re-plan when reality changes |
| `/ideafoundry render <doc-id>` | Render one on-demand doc |
| `/ideafoundry render all` | Render every roster doc eagerly (opt-in) |
| `/ideafoundry status` | Print current `STATUS.md` |
| `/ideafoundry export` | Package `planning/` for download |
| `/ideafoundry continue` | Resume from a pasted bundle |
| `/ideafoundry help` | List subcommands + current phase |

## How it works

1. **Discovery** — ≤8 conversational questions (six mandatory + adaptive probing) → confirmed **Brief** (single source of truth, stable section IDs).
2. **Roster** — the Skill *proposes* a right-sized team with per-specialist reasoning; you confirm or override.
3. **Specialists** — each runs one-per-turn in a fresh context, re-anchoring from files (not chat history), emitting a **structured JSON planning object** that cites the Brief by ID and never restates it.
4. **Consensus** — a coordinator reads *summaries first*, detects conflicts, batches challenges into a single escalation, runs a simplifier pass, and writes `decisions.json`.
5. **Generation** — renders a normalized `planning/` folder plus a few eager docs; the rest render **lazily** on demand.
6. **Amendment** — when reality changes, `amend` walks the traceability graph, marks only what's stale, and re-runs only the affected specialists.

The whole phase graph is in **[`WORKFLOW.md`](WORKFLOW.md)**. The design rationale is in **[`PLAN.md`](PLAN.md)**; the backlog in **[`TICKETS.md`](TICKETS.md)**; the acceptance evals in **[`EVAL.md`](EVAL.md)**.

## Design principles (enforced, not decorative)

- **Right-sized, never over-scoped.** Each profile declares a *complexity ceiling*; a specialist recommending Kubernetes for a habit tracker must justify it against a Brief constraint or it's a schema violation.
- **Mostly-lazy generation.** Only the 2 docs 90% of people open first are rendered eagerly; you pay tokens for what you read.
- **Challenges, gated.** Specialists can push back on the Brief, but only *material* (high-impact) challenges surface; the rest are logged.
- **Portable state.** The `planning/` folder is the crown jewel; `export`/`continue` move it between sessions and teammates as a single JSON bundle.
- **Token budget is a forcing function.** Every file declares a budget; every invocation stays under 60K.

## Repository layout

```
ideafoundry/
  SKILL.md              lean router (~250 tokens, loaded every turn)
  WORKFLOW.md           whole phase graph, for humans
  discovery/            mandatory questions, probing rubric, Brief schema
  roster/               roster rubric + profile YAMLs (with complexity ceilings)
  specialists/          PM / Engineer / UX / Security / QA prompts + schemas
  consensus/            coordinator (conflict detection, decisions, simplifier)
  generation/           document generator + templates (each declares requires:/loads:)
  rules/                planning-rules, mvp-rules, RECOVERY (loaded only on error)
  examples/             one worked Internal-Tool run (on-disk only, zero runtime tokens)
  evals/                eval harness + fixtures
```

Version: **schema v1**. Every artifact carries `schema_version: 1`.
