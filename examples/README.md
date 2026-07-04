# Examples

IdeaFoundry ships **one** fully-worked example — [`internal-tool-run/`](internal-tool-run/) — and describes the other profiles' run shapes in prose here. This is deliberate (PLAN §25): a full example folder per profile would be four times the maintenance for little added value, and examples are **on-disk-only** — they cost **zero runtime tokens** and are loaded by the Skill *only* when a specialist output looks structurally wrong and Claude needs a reference for the schema shape.

## The worked example: `internal-tool-run/`

**Idea:** "DeployGate" — an internal tool where engineers request production deployments and team leads approve/reject them, with an audit trail.

It exercises the parts of the methodology worth seeing end to end:
- **A reasoned roster** (`planning/roster.json`): PM + Engineer + Security included; UX and QA **declined with captured reasoning** — not blindly full-team.
- **A justified ceiling deviation** (`planning/architecture.json` → `complexity_justification`): Postgres over the profile's preferred SQLite, grounded in `brief.constraints.c4` (durable audit + concurrent approvers). The Consensus Simplifier passed it (`decisions.json` → `simplification_candidates: []`) because the rejection cites a Brief constraint, not "best practices" — this is what a *legitimate* deviation looks like.
- **A real specialist disagreement** (`planning/conflicts.json` → `cf1`): Security requires separation of duties; PM's approve flow didn't. Consensus resolved the mechanical part with written rationale (`decisions.json` → `resolved`).
- **A materiality-gated challenge** (`planning/security.json` → `challenges_to_brief`, impact `high`): SSO authenticates but doesn't authorize. Because it's `high`, it surfaced to the user as an escalation (`decisions.json` → `es1`); `challenges_log.json` is empty because there were no medium/low challenges to log.
- **Roster-gated docs** (`README.md` doc index): 8-doc Internal Tool set; `06-ux-specification` and `08-test-strategy` flagged `not in roster`, never rendered, never referenced brokenly.
- **Compliance omission** (`docs/07-security-review.md`): the Compliance section is **dropped entirely** (not stubbed "N/A") because the tool is internal and non-regulated.

Rendered eagerly: `docs/00-executive-summary.md`, `docs/12-developer-tickets.md`. Also rendered here for illustration: `docs/07-security-review.md`. Everything else shows as `not yet rendered` in the index to demonstrate the lazy-render model.

## Shape of the other profiles' runs (described, not shipped)

**Weekend Hack** (e.g. "Slack app that summarizes standups and flags blockers"). Roster: **PM + Engineer** only; UX and Security both proposed-and-declined with reasoning. The decisive property is **anti-over-engineering**: the Engineer defaults to SQLite / single-instance / library-auth / cron, and `complexity_justification` is empty. 5-doc set (`00, 01, 02, 09, 12`). Initial run ~26K. This is the profile most likely to make the tool look silly in public if it reached for Kubernetes — so the ceiling is tightest here.

**Consumer App** (e.g. "Duolingo for financial literacy"). Roster: **PM + Engineer + UX**, with **Security proposed when the Brief signals accounts/stored user data** (progress + accounts = user data). The interesting artifacts are `ux.json` (personas, primary flows tied to `target_users` + features, an explicit accessibility floor) and a UX `challenges_to_brief` on a success metric ("lessons completed rewards volume, not retention"). 8-doc set including `06-ux-specification`. Discovery works harder here because the idea starts vague — confidence often lands Yellow with populated `gaps_to_clarify`.

**Regulated / Production** (e.g. "Semantic caching layer for LLM apps handling customer prompts"). Roster: **all five**; Security is **mandatory** (customer prompts = personal data + production surface). The wider ceiling means enterprise patterns (a dedicated vector store, per-tenant KMS keys) are *appropriate* — but they **still** carry a `complexity_justification` grounded in a Brief/compliance constraint. This is the "ceiling scales with profile, enforcement never disappears" case. Full 14-doc set; `07-security-review.md` renders its Compliance section (GDPR/SOC2). Initial run ~46K, hard cap 55K; `render all` warns before proceeding.

**Amendment** (runs on top of a completed Consumer App). `/ideafoundry amend "support offline mode"` writes `planning/amendments/001-offline-mode.json`, walks the traceability graph backward to mark 2–3 specialist outputs stale (architecture, product, maybe ux), reruns only those specialists, and flags 4–5 docs stale in the README **without regenerating them**. Untouched files stay byte-identical. Target cost 8–12K — a whole-team rerun would be a failure, not an amendment.

## Using an example

The Skill references `internal-tool-run/` **only** when a specialist output looks structurally wrong and it needs to see a valid instance of the schema. On the happy path, nothing here is ever loaded — that's the point of keeping examples on disk.
