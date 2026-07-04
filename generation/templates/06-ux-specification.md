# Template — 06-ux-specification.md

<!-- token-budget: <=3K output -->
<!-- requires: [ux] -->
<!-- loads: [meta, brief, ux, product] -->
<!-- eager: no -->

The UX spec. **Rendered only when UX is in the roster** — on Weekend Hack / Internal Tool it is dropped entirely (README: `not in roster`). Slot-fill from `ux.json` (+ `product` to link flows to features). This is the canonical F-040 case: a template that must never render with `planning.ux.*` unresolved.

---

## Render shape

```markdown
# <brief.vision title> — UX Specification

**Shape.** <ux.summary — platform + core-flow count + a11y floor>

## Personas
<for p in ux.personas: - **<p.label>** — needs <p.need> (serves <p.serves>)>

## Primary flows
<for fl in ux.primary_flows:>
### <fl.name>
- **For:** <fl.serves persona> · **Feature:** <fl.feature> (→ product.features[fl.feature].name)
- **Steps:** <fl.steps, ordered>
- **Empty / error / loading states:** <derive from ux_risks touching this flow>
<end for>

## Navigation & information architecture
<ux.navigation>

## Accessibility floor (non-negotiable)
<for a in ux.accessibility_floor: - <a>>

## UX risks
<for ur in ux.ux_risks: - **<ur.risk>** — <ur.mitigation>>
```

## Rules
- **Existence is gated:** the generator drops this template unless `ux` ∈ roster. There is therefore no in-template "if UX absent" branch — its presence *is* the UX guarantee.
- Every flow links to a real `product.features.*` id (via `fl.feature`) and a persona — if a flow references a feature not in `product.json`, surface `⚠ flow references unknown feature` rather than silently rendering.
- Accessibility floor is rendered verbatim from `ux.accessibility_floor` — never soften it to "consider a11y".
- ≤3K.
