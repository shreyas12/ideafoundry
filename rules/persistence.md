# Persistence — export / continue / resume

<!-- token-budget: <=1K -->
<!-- Loaded on `/ideafoundry export` and `/ideafoundry continue`. The planning/ folder is the ONLY state; this file moves it. -->

The `planning/` folder **is** the project state — nothing important lives only in the conversation. Persistence moves that folder between sessions and machines. There is no database, no server; the bundle is a plain JSON blob the user can paste anywhere.

## `/ideafoundry export`
Serialize the whole `planning/` folder (plus root `STATUS.md`) into a single `planning-bundle.json`:
```json
{
  "schema_version": 1,
  "exported_from": "<meta.profile> run",
  "files": {
    "planning/meta.json": { ...verbatim contents... },
    "planning/brief.json": { ... },
    "planning/product.json": { ... },
    "...": "one key per file, value = its parsed JSON (or string for markdown)",
    "STATUS.md": "…markdown string…"
  }
}
```
Keys are **exact folder-relative paths**; values are the file contents. This one file is the only thing a user needs to keep. Rendered `docs/` are **not** bundled — they regenerate from `planning/`, so the bundle stays small.

## `/ideafoundry continue` — two modes
- **With a pasted bundle:** reconstitute the folder by writing each `files` key back to disk verbatim, then regenerate views (`README.md` doc index + eager `00`/`12`) from the restored `planning/`. **Round-trip is byte-exact** for the `planning/` files — export→continue reproduces the folder. This is the teammate handoff: a fresh session with only the bundle can `render tickets` immediately.
- **Without a bundle (resume):** read `planning/state.json`, report `last_completed_phase`, and ask whether to resume from the next phase. This is the abandoned-run recovery path (RECOVERY case 3).

## Rules
- **The bundle is the whole contract.** If a flow needs state the bundle doesn't carry, the bundle schema is wrong — fix it, don't reach into chat scrollback.
- **Don't bundle derived docs.** They're a function of `planning/`; bundling them risks staleness and bloats the blob. Regenerate on `continue`.
- **Don't reinvent VCS.** Versioning across amendments is `git` on the folder / successive bundles — not a merge engine inside the Skill.
