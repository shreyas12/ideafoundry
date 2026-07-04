# EVAL 0 — Roster graceful degradation (cross-cutting)

Traces: EVAL.md §"Roster-graceful-degradation test", PLAN §14 · Runs on **EVAL 1's** Weekend Hack output.

This is the F-040 assertion, factored out because it applies to every roster-gated template. It proves a template with an **optional dependency on an absent specialist** renders cleanly — or is dropped — with **zero broken references** and **no "N/A" filler**.

## Setup
Use EVAL 1's completed Weekend Hack run (roster = PM + Engineer; **no Security, no UX, no QA**).

## The test
Attempt to surface a security-referencing section against that run in two ways:

1. **Whole-template drop.** `07-security-review.md` declares `requires: [security]`. Since Security ∉ roster, the Document Generator **drops the template entirely**; `README.md` flags it `not in roster`. Assert: `docs/07-security-review.md` was **not** rendered.
2. **Within-template section gating.** Render `10-deployment-ops.md` (`requires: [engineer]`, present) — its *Configuration & secrets* hardening detail loads from `security.json`, which is absent. Assert: the hardening subsection renders the **one-line library-default fallback**, with **no** `planning.security.*` reference and **no** "N/A" stub.

## Assertions
- `check_docs_gating` in `check.py`: for every doc in `DOC_REQUIRES` whose required specialist ∉ roster, that doc **must not** appear in `docs/`.
- **Manual grep (0 hits required):** `grep -rn "planning.security" <run>/docs/` and `grep -rn "planning.ux" <run>/docs/` return nothing. Any dangling `planning.<absent-role>.*` reference = FAIL.
- **No filler:** no rendered doc contains an "N/A" stub standing in for an omitted gated section.

## Pass / fail
- **PASS:** the security-referencing section is omitted (template dropped) or degraded to the library-default line; zero broken references; zero "N/A" stubs.
- **FAIL:** any dangling `planning.security.*` / `planning.ux.*` reference, any "N/A" stub filler, or a render error.
