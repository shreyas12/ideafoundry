# Template — 04-database-schema.md

<!-- token-budget: <=3K output -->
<!-- requires: [engineer] -->
<!-- loads: [meta, architecture] -->
<!-- eager: no -->

The data model, expanded from `architecture.data_schema` into implementable table/collection definitions. Slot-fill from the Engineer's entities — this doc formats and lightly elaborates (types, keys, relationships), it does **not** design new entities. Dropped if Engineer absent.

---

## Render shape

```markdown
# <brief.vision title> — Data Schema

**Store.** <architecture.stack.db>  ·  **Model:** <relational | document | KV — infer from db>

## Entities
<for d in architecture.data_schema:>
### <d.entity>
| field | type | notes |
|---|---|---|
<for kf in d.key_fields: | <kf> | <inferred type> | <key/index if implied> |>
<any additional fields implied by d.notes>
- **Notes:** <d.notes>
<end for>

## Relationships
<derive from shared key fields across entities — e.g. "message.team_id → team.id (many-to-one)">

## Indexes & constraints
<the 1–3 that matter for the primary flows — e.g. lookup keys, uniqueness, tenant scoping if Security flagged it>
```

## Rules
- **No new entities.** Only elaborate what `architecture.data_schema` lists. Types are inferred from field names/notes; mark anything uncertain as `<type?>` rather than guessing precisely.
- Infer relationships from shared keys the Engineer named — don't fabricate joins.
- If the Engineer's schema is intentionally thin (weekend hack), keep this doc thin too — proportionality over completeness.
- ≤3K.
