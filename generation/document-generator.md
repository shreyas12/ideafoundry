# Document Generator — Normalized planning/, Mostly Lazy

<!-- token-budget: <=2K -->
<!-- phase: Generation · loaded on initial run and on every `render` -->
<!-- reads: planning/roster.json + each template's declared loads: -->

Specialists emit structured objects; you render them to markdown — **not eagerly, and not from a single blob.** Everything you need is already in the normalized `planning/` folder. **You never re-read specialist reasoning or the conversation** — rendering is slot-fill, not synthesis.

## The normalized folder (never a monolith)
```
planning/
  meta.json  brief.json  goals.json  roster.json
  product.json  architecture.json  ux.json  security.json  qa.json   (present iff in roster)
  decisions.json  challenges_log.json  conflicts.json  state.json
```
A single `planning.json` would balloon to 15–20K on a Regulated build and break the on-demand render math. Each template declares the files it needs; it pays only for those.

## Template contract
Every template in `templates/` declares two headers:
```
requires: [engineer, security]     # specialists whose presence the template needs
loads: [meta, brief, security, decisions]   # planning files to load (nothing else)
```

## Generation algorithm
1. Read `planning/roster.json`.
2. For each template: if any `requires:` specialist is **absent from the roster**, **drop the template** (README marks it `not in roster`).
3. For surviving templates, load **only** the declared `loads:` files.
4. **Slot-fill** the template from those files. **Conditional sections** gated by Brief/planning flags: if `brief.compliance` is absent, **omit the compliance section entirely — do not stub "N/A"** (filler is a token tax paid every render).
5. If a template references an absent specialist's output that slipped through gating (`planning.security.*` with no Security), **omit that section with a one-line note in README** — never emit a broken reference or a render error.
6. **Enforce the 3K/doc cap.** If a doc wants to be larger, split it or push detail into `planning/` (where it lives once, referenced by ID).

## Initial run — emit exactly five things
1. the `planning/` folder (already written by prior phases)
2. `README.md` — the **doc index** with per-doc status flags (below)
3. `STATUS.md` (via `rules/status-writer.md`)
4. `PLAN_SUMMARY.md` (via `plan-summary-template.md`)
5. **eager renders** of `docs/00-executive-summary.md` + `docs/12-developer-tickets.md` — the two docs 90% read first

**Everything else stays lazy.** This turns the first impression from "the AI didn't do the work" into "here's my plan."

## README doc index — status flags
List all of the active profile's `doc_set`, each flagged:
- `available` — rendered, path shown
- `not yet rendered` — in roster, render with `/ideafoundry render <id>`
- `not in roster` — its specialist wasn't selected
- `stale` — an amendment invalidated it; regenerates on next render

## On-demand render (`/ideafoundry render <doc-id>`)
Load only that template's `loads:` files + the template → produce the doc (~1.5–2.5K, ≤3K). Update its README flag to `available`. A typical user reads 3–5 of 14 docs, so most doc cost is never paid.

## `/ideafoundry render all`
Escape hatch (handing off to a coding assistant / exporting for a client). Costs the equivalent of eager generation; **on Regulated, warn it may approach the ceiling before proceeding.**

## Stale-doc regeneration (post-Amendment)
A doc flagged `stale` regenerates from the **current** `planning/` on its next `render`, then flips its flag back to `available`. Amendment never eagerly regenerates docs.
