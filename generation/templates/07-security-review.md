# Template — 07-security-review.md

<!-- token-budget: <=3K output -->
<!-- requires: [security] -->
<!-- loads: [meta, brief, security, decisions] -->
<!-- eager: no -->

The security review. **Rendered only when Security is in the roster.** Slot-fill from `security.json`. The `compliance` section is gated a second time *within* the template: if `security.compliance` is absent (non-regulated domain), omit it entirely — never stub "N/A". Dropped whole if Security absent.

---

## Render shape

```markdown
# <brief.vision title> — Security Review

**Crown-jewel risk.** <security.summary>

## Threat model
<for th in security.threats: - **[<th.severity>] <th.threat>** — mitigation: <th.mitigation>>

## Authentication & authorization
- **AuthN:** <security.authn>
- **AuthZ boundary:** <security.authz>

## Secrets & data protection
- **Secrets:** <security.secrets>
- **At rest:** <security.data_protection.at_rest> · **In transit:** <security.data_protection.in_transit>
- **Tenant isolation:** <security.data_protection.tenant_isolation>

## Compliance
<!-- render this whole section ONLY if security.compliance is present -->
- **Regime:** <security.compliance.regime>
- **Requirements:** <for r in security.compliance.requirements: - <r>>
<!-- if security.compliance absent: omit the entire Compliance section, no heading, no "N/A" -->

## Challenges to the Brief
<for c in security.challenges_to_brief: - **[<c.impact>]** on <c.brief_section_id>: <c.concern> → <c.recommendation>>
<if any accepted in decisions.accepted_challenges: mark "✓ accepted — Brief updated">

## Security risks
<for sr in security.security_risks: - **<sr.risk>** — <sr.mitigation>>
```

## Rules
- **Double gate:** template exists only if `security` ∈ roster; the *Compliance* section renders only if `security.compliance` is populated. Two independent omissions, both silent (no stub).
- Surface `challenges_to_brief` with their impact band — a `high` here is what drove a Consensus escalation; show whether it was accepted (`decisions.accepted_challenges`).
- Any enterprise control in `security.complexity_justification` should already be visible in `05-architecture-decisions.md`; don't duplicate the ADR, reference it.
- ≤3K.
