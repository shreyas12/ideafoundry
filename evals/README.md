# Evals

IdeaFoundry is a Skill (prompts + schemas), so an eval has two halves:

1. **The run (manual).** A human invokes `/ideafoundry` with a fixture's `prompt`, participates in the workshop, and saves the resulting `planning/` folder plus a `tokens.json` recording per-phase token usage. This half is a Claude session — it is *not* automated here.
2. **The check (automated).** `check.py` loads that saved `planning/` folder and the fixture, runs the structural + rubric assertions, and prints the EVAL.md reporting block with a PASS/FAIL. This half is deterministic and dependency-free (Python stdlib only).

> These files are **authored, not run** — the checker is provided so a run *can* be validated, but nothing here executes an eval on its own. Running requires a live `/ideafoundry` session to produce the `planning/` folder first.

## Layout
```
evals/
  README.md                     ← this file
  check.py                      ← the assertion runner (stdlib only)
  fixtures/
    eval-1-weekend-hack.json     prompt + expected roster + banned ceiling terms + budget
    eval-2-consumer-app.json
    eval-3-regulated.json
    eval-4-amendment.json
  eval-1-weekend-hack.md         ← human spec: expected behavior + assertions + pass criteria
  eval-2-consumer-app.md
  eval-3-regulated.md
  eval-4-amendment.md
  eval-0-roster-degradation.md   ← cross-cutting F-040 test (runs on EVAL 1's output)
```

## The four evals (map to EVAL.md)
| Eval | Profile | Decisive assertion |
|---|---|---|
| 1 · Weekend Hack | weekend-hack | **anti-over-engineering** — zero unjustified ceiling items |
| 2 · Consumer App | consumer-app | UX challenge on a success metric surfaces; Security proposed on user-data signal |
| 3 · Regulated | regulated | Security fires ≥1 concrete threat/challenge; ceiling deviations stay Brief-justified |
| 4 · Amendment | consumer-app + amend | only affected specialists rerun; cost < 15K; untouched files byte-identical |

## Global pass criteria (all evals, EVAL.md §"Global pass criteria")
A run passes iff: reasoned roster; only-roster docs (absent-specialist docs flagged, never broken); ≥1 Consensus-resolved disagreement; every ticket `traces_to` a goal; **total tokens under the profile hard cap**; STATUS.md updated each phase; **zero unjustified complexity-ceiling violations**. A single unjustified ceiling item, a blown budget, or a broken absent-specialist reference **fails the eval regardless of output quality**.

## Running the checker (once a run exists)
```
python3 evals/check.py --fixture evals/fixtures/eval-1-weekend-hack.json \
                       --planning path/to/run/planning \
                       --tokens  path/to/run/tokens.json
```
It prints the EVAL.md reporting block and exits non-zero on any hard failure. To self-test the checker's shape against the shipped example, point `--planning` at `examples/internal-tool-run/planning` (note: that folder is the Internal Tool profile, not one of the four eval profiles, so ceiling/roster fixtures won't all match — it exercises the *loader and reporter*, not the pass criteria).
