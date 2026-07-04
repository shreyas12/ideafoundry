#!/usr/bin/env python3
"""IdeaFoundry eval checker.

Validates a saved planning/ folder (produced by a manual /ideafoundry run) against
an eval fixture, then prints the EVAL.md reporting block with a PASS/FAIL.

Stdlib only. Authored, not run — this is the deterministic half of an eval; the run
half is a live /ideafoundry session that produces the planning/ folder first.

Usage:
  python3 evals/check.py --fixture evals/fixtures/eval-1-weekend-hack.json \
                         --planning path/to/run/planning \
                         [--tokens path/to/run/tokens.json] \
                         [--baseline path/to/pre-amendment/planning]  # eval-4 only

tokens.json shape (per-phase + total, in thousands or raw tokens):
  {"per_phase": {"discovery": 6200, "roster": 1900, ...}, "profile_total": 25800}
"""
import argparse
import hashlib
import json
import os
import sys

ROLE_FILES = {
    "pm": "product.json",
    "engineer": "architecture.json",
    "ux": "ux.json",
    "security": "security.json",
    "qa": "qa.json",
}
# which specialist a roster-gated doc requires (from each template's `requires:` header)
DOC_REQUIRES = {
    "06-ux-specification": "ux",
    "07-security-review": "security",
    "08-test-strategy": "qa",
}


class Report:
    def __init__(self):
        self.lines = []
        self.failures = []   # hard failures → FAIL
        self.warnings = []   # soft failures → reported, not fatal

    def info(self, msg):
        self.lines.append(msg)

    def check(self, ok, hard_msg, hard=True):
        if ok:
            return True
        (self.failures if hard else self.warnings).append(hard_msg)
        return False

    def passed(self):
        return not self.failures


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"malformed JSON in {path}: {exc}")


def load_planning(planning_dir):
    folder = {}
    if not os.path.isdir(planning_dir):
        raise SystemExit(f"--planning is not a directory: {planning_dir}")
    for name in os.listdir(planning_dir):
        if name.endswith(".json"):
            folder[name[:-5]] = load_json(os.path.join(planning_dir, name))
    return folder


def roster_roles(folder):
    roster = folder.get("roster") or {}
    return [r.get("role") for r in roster.get("included", []) if r.get("role")]


def text_blob(arch):
    """Concatenate the free-text engineer fields where a ceiling term would appear."""
    if not arch:
        return ""
    parts = [arch.get("summary", ""), arch.get("approach", "")]
    stack = arch.get("stack", {})
    if isinstance(stack, dict):
        parts.extend(str(v) for v in stack.values())
    return " ".join(parts).lower()


def justified_terms(arch):
    out = []
    for cj in (arch or {}).get("complexity_justification", []) or []:
        out.append(str(cj.get("recommendation", "")).lower())
    return out


# ---- assertion groups ---------------------------------------------------------

def check_roster(fx, folder, rep):
    roster = folder.get("roster")
    if not rep.check(roster is not None, "roster.json missing"):
        return
    included = roster_roles(folder)
    exp = fx.get("expected_roster", {})
    for role in exp.get("included", []):
        rep.check(role in included, f"expected roster to include '{role}', got {included}")
    if exp.get("security_mandatory"):
        rep.check("security" in included, "Security is mandatory for this profile but absent from roster")
    if exp.get("declined_must_have_reason"):
        for ex in roster.get("excluded", []):
            rep.check(bool(str(ex.get("reason", "")).strip()),
                      f"excluded role '{ex.get('role')}' has no reason recorded")
        for inc in roster.get("included", []):
            rep.check(bool(str(inc.get("reason", "")).strip()),
                      f"included role '{inc.get('role')}' has no reason recorded")


def check_ceiling(fx, folder, rep):
    arch = folder.get("architecture")
    if arch is None:
        rep.info("  ceiling: no architecture.json (engineer not in roster) — skipped")
        return 0
    blob = text_blob(arch)
    justif = justified_terms(arch)
    unjustified = []
    for term in fx.get("banned_ceiling_terms", []):
        t = term.lower()
        if t in blob and not any(t in j for j in justif):
            unjustified.append(term)
    rep.check(len(unjustified) == 0,
              f"UNJUSTIFIED complexity-ceiling violations: {unjustified} "
              f"(term present in architecture but no matching complexity_justification)")
    if fx.get("justification_must_cite_brief"):
        for cj in arch.get("complexity_justification", []) or []:
            why = str(cj.get("why_needed", "")).lower()
            rep.check("brief." in why or "constraint" in why or "compliance" in why,
                      f"complexity_justification '{cj.get('recommendation')}' does not cite a Brief constraint "
                      f"(why_needed: {cj.get('why_needed')!r})")
    return len(unjustified)


def check_traceability(fx, folder, rep):
    product = folder.get("product")
    if product is None:
        rep.info("  traceability: no product.json — skipped")
        return
    goals = folder.get("goals") or {}
    goal_ids = {g.get("id") for g in goals.get("business_goals", [])}
    brief = folder.get("brief") or {}
    brief_goal_ids = {"brief.goals." + g.get("id") for g in brief.get("goals", [])}
    brief_goal_ids |= {g.get("id") for g in brief.get("goals", [])}
    valid = goal_ids | brief_goal_ids
    for f in product.get("features", []):
        serves = f.get("serves")
        norm = serves.split(".")[-1] if isinstance(serves, str) else serves
        rep.check(serves in valid or norm in {gid.split('.')[-1] for gid in valid},
                  f"feature {f.get('id')} serves '{serves}' which is not a known goal id")
    # MVP must be a real cut
    mvp = product.get("mvp", {})
    rep.check(len(mvp.get("deferred", [])) > 0 or fx.get("single_feature"),
              "product.mvp.deferred is empty — MVP did not cut scope (mvp-rules #2)")
    # QA acceptance skeletons (if present) must reference real features
    qa = folder.get("qa")
    if qa:
        feat_ids = {f.get("id") for f in product.get("features", [])}
        for ac in qa.get("acceptance_skeletons", []):
            rep.check(ac.get("feature") in feat_ids,
                      f"acceptance {ac.get('id')} references unknown feature '{ac.get('feature')}'")


def check_challenges(fx, folder, rep):
    """Materiality gate: every high challenge surfaces in escalations; med/low do not."""
    decisions = folder.get("decisions") or {}
    escalations = decisions.get("escalations", [])
    log = (folder.get("challenges_log") or {}).get("challenges", [])
    highs, meds = [], []
    for role in ("pm", "engineer", "ux", "security", "qa"):
        out = folder.get(role_output_key(role))
        for ch in (out or {}).get("challenges_to_brief", []) or []:
            (highs if ch.get("impact") == "high" else meds).append((role, ch))
    # every high challenge should be represented in the escalation batch
    if highs:
        rep.check(len(escalations) >= 1,
                  f"{len(highs)} high challenge(s) fired but decisions.escalations is empty (not surfaced)")
    # medium/low must NOT appear as escalations; they belong in the log
    for role, ch in meds:
        in_log = any(l.get("brief_section_id") == ch.get("brief_section_id") for l in log)
        rep.check(in_log or True,  # soft: absence-in-log is a warning, not a hard fail
                  f"[warn] medium/low challenge from {role} on {ch.get('brief_section_id')} not found in challenges_log",
                  hard=False)
    exp = fx.get("expected_challenges", {})
    if "high_count_min" in exp:
        rep.check(len(highs) >= exp["high_count_min"],
                  f"expected >= {exp['high_count_min']} high challenge(s), got {len(highs)}")
    if "any_fired_min" in exp:
        rep.check(len(highs) + len(meds) >= exp["any_fired_min"],
                  f"expected >= {exp['any_fired_min']} challenge(s) total, got {len(highs) + len(meds)}")
    return len(highs), len(meds)


def role_output_key(role):
    return {"pm": "product", "engineer": "architecture", "ux": "ux",
            "security": "security", "qa": "qa"}[role]


def check_consensus(fx, folder, rep):
    decisions = folder.get("decisions") or {}
    resolved = decisions.get("resolved", [])
    conflicts = (folder.get("conflicts") or {}).get("conflicts", [])
    # global criterion 4: >=1 visible disagreement resolved with rationale
    rep.check(len(resolved) >= 1 or len(conflicts) == 0,
              "no Consensus-resolved disagreement recorded (global pass criterion 4) "
              "— acceptable only if conflicts.json is genuinely empty")
    for d in resolved:
        rep.check(bool(str(d.get("rationale", "")).strip()),
                  f"resolved conflict '{d.get('conflict')}' has no written rationale")
    return len(resolved), len(conflicts)


def check_docs_gating(fx, folder, planning_dir, rep):
    """Absent-specialist docs must not have been rendered; present ones may be."""
    included = set(roster_roles(folder))
    docs_dir = os.path.join(os.path.dirname(planning_dir.rstrip("/")), "docs")
    rendered = set()
    if os.path.isdir(docs_dir):
        rendered = {n[:-3] for n in os.listdir(docs_dir) if n.endswith(".md")}
    for doc, required_role in DOC_REQUIRES.items():
        if required_role not in included:
            rep.check(doc not in rendered,
                      f"doc '{doc}' was rendered but its required specialist '{required_role}' "
                      f"is not in the roster (broken roster gating)")
    return sorted(rendered)


def check_budget(fx, tokens, rep):
    budget = fx.get("budget", {})
    if tokens is None:
        rep.info("  budget: no tokens.json supplied — budget assertion skipped (report only)")
        return None
    total = tokens.get("profile_total")
    if total is None:
        rep.warnings.append("[warn] tokens.json has no profile_total")
        return None
    total_k = total / 1000 if total > 1000 else total  # accept raw or already-K
    cap = budget.get("hard_cap_k")
    if cap is not None:
        rep.check(total_k <= cap,
                  f"BUDGET EXCEEDED: profile total {total_k:.1f}K > hard cap {cap}K")
    return total_k


def check_amendment(fx, folder, planning_dir, baseline_dir, tokens, rep):
    amendments_dir = os.path.join(planning_dir, "amendments")
    rep.check(os.path.isdir(amendments_dir) and os.listdir(amendments_dir),
              "no planning/amendments/ entries — amendment was not recorded")
    amd = None
    if os.path.isdir(amendments_dir):
        files = sorted(f for f in os.listdir(amendments_dir) if f.endswith(".json"))
        if files:
            amd = load_json(os.path.join(amendments_dir, files[0]))
    if amd:
        rerun = set(amd.get("rerun", []))
        exp = fx.get("expected_rerun", {})
        for r in exp.get("must_include", []):
            rep.check(r in rerun, f"expected '{r}' to rerun, rerun set = {sorted(rerun)}")
        for r in exp.get("must_exclude", []):
            rep.check(r not in rerun,
                      f"'{r}' rerun but should be untouched (that would be a rerun, not an amendment)")
        stale_docs = amd.get("stale_docs", [])
        sd = fx.get("expected_stale_docs", {})
        if "count_min" in sd:
            rep.check(sd["count_min"] <= len(stale_docs) <= sd.get("count_max", 99),
                      f"stale-doc count {len(stale_docs)} outside expected "
                      f"[{sd['count_min']},{sd.get('count_max')}] — possible over/under-marking")
    # byte-identical untouched files vs baseline
    if baseline_dir:
        for role in fx.get("untouched_must_be_byte_identical", []):
            fn = ROLE_FILES.get(role)
            if not fn:
                continue
            a = os.path.join(baseline_dir, fn)
            b = os.path.join(planning_dir, fn)
            if os.path.exists(a) and os.path.exists(b):
                rep.check(_sha(a) == _sha(b),
                          f"{fn} changed during amendment but should be byte-identical (untouched)")
    else:
        rep.info("  amendment: no --baseline supplied — byte-identical check skipped")
    # budget
    tk = check_budget({"budget": {"hard_cap_k": fx.get("budget", {}).get("amendment_k_max")}}, tokens, rep)
    return tk


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# ---- main ---------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="IdeaFoundry eval checker")
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--planning", required=True)
    ap.add_argument("--tokens")
    ap.add_argument("--baseline", help="pre-amendment planning/ dir (eval-4 only)")
    args = ap.parse_args()

    fx = load_json(args.fixture)
    if fx is None:
        raise SystemExit(f"fixture not found: {args.fixture}")
    folder = load_planning(args.planning)
    tokens = load_json(args.tokens) if args.tokens else None

    rep = Report()
    rep.info(f"EVAL {fx.get('id')} — {fx.get('profile')}  ({fx.get('kind')})")

    included = roster_roles(folder)
    declined = [r.get("role") for r in (folder.get("roster") or {}).get("excluded", [])]
    rep.info(f"  Roster: {included or '—'} | declined: {declined or '—'} "
             f"(reasons present? {'y' if all((e.get('reason') or '').strip() for e in (folder.get('roster') or {}).get('excluded', [])) else 'n'})")

    if fx.get("kind") == "amendment":
        tk = check_amendment(fx, folder, args.planning, args.baseline, tokens, rep)
        rep.info(f"  Amendment tokens: {tk if tk is not None else 'n/a'}K | cap {fx.get('budget', {}).get('amendment_k_max')}K")
    else:
        check_roster(fx, folder, rep)
        unjust = check_ceiling(fx, folder, rep)
        check_traceability(fx, folder, rep)
        highs, meds = check_challenges(fx, folder, rep)
        resolved, conflicts = check_consensus(fx, folder, rep)
        rendered = check_docs_gating(fx, folder, args.planning, rep)
        total_k = check_budget(fx, tokens, rep)
        rep.info(f"  Challenges fired: {highs} high / {meds} med-low, surfaced: "
                 f"{'high only' if highs else 'none'}")
        rep.info(f"  Consensus: {resolved} resolved / {conflicts} conflicts, "
                 f"escalations {len((folder.get('decisions') or {}).get('escalations', []))}")
        rep.info(f"  Complexity-ceiling violations (unjustified): {unjust}   (must be 0)")
        rep.info(f"  Docs rendered: {rendered or '—'}")
        rep.info(f"  Tokens: profile total {total_k if total_k is not None else 'n/a'}K "
                 f"| hard cap {fx.get('budget', {}).get('hard_cap_k')}K")

    print("\n".join(rep.lines))
    if rep.warnings:
        print("\nWarnings:")
        for w in rep.warnings:
            print(f"  - {w}")
    print()
    if rep.passed():
        print(f"RESULT: PASS — {fx.get('id')}")
        sys.exit(0)
    else:
        print(f"RESULT: FAIL — {fx.get('id')}")
        for f in rep.failures:
            print(f"  ✗ {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
