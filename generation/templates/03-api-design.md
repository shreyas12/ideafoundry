# Template — 03-api-design.md

<!-- token-budget: <=3K output -->
<!-- requires: [engineer] -->
<!-- loads: [meta, architecture] -->
<!-- eager: no -->

The API contract, expanded from `architecture.api_surface`. Slot-fill only — the Engineer already decided the surface; this doc formats it at the level a developer implements from. Dropped entirely if Engineer is absent.

---

## Render shape

```markdown
# <brief.vision title> — API Design

**Style.** <infer from architecture.stack: REST / RPC / GraphQL / Slack-events — state it in one line>
**Auth.** <architecture.stack.auth> — applied to all non-public endpoints.

## Endpoints
<for e in architecture.api_surface:>
### `<e.method> <e.path>`
- **Purpose:** <e.purpose>
- **Serves:** <e.serves>
- **Request:** <derive from purpose + related data_schema entity — fields only, not full JSON schema>
- **Response:** <success shape, one line> · **Errors:** <the 1–2 failure modes that matter>
<end for>

## Cross-cutting
- **Auth boundary:** <architecture.stack.auth> (see `07-security-review.md` if Security in roster)
- **Versioning / errors:** <sensible default for the chosen style — e.g. path prefix, problem+json>
```

## Rules
- **Derive request/response from `architecture.data_schema` + endpoint purpose** — do not invent entities the Engineer didn't name.
- Keep it implementation-level, not exhaustive OpenAPI. If the surface is large, group by resource and stay ≤3K.
- Reference `07-security-review.md` for the auth boundary **only if** Security is in the roster; otherwise state the library-default auth in one line and move on.
