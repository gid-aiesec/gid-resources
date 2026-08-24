# `infra/js`

CI and editor setup for a JS/TS project: lint, format, typecheck, and a file-size gate, wired into
[`ci.yml`](ci.yml) as a single `frontend-checks` job. Pair this with [`infra/python`](../python/README.md) for a
Python backend, or drop it in on its own for a JS/TS-only repo.

This directory doesn't ship ESLint/Prettier/TypeScript config -- those are your project's own. It only supplies
the CI job, the size-check script, and the `package.json` scripts that tie them together.

## What to add to your `package.json`

```json
"scripts": {
    "lint": "eslint",
    "lint:fix": "eslint --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "check:size": "node scripts/check-file-size.mjs",
    "check": "npm run lint:fix && npm run format && npm run typecheck && npm run check:size",
    "check:ci": "npm run lint && npm run format:check && npm run typecheck && npm run check:size"
}
```

| Command | What it does | When to use it |
| --- | --- | --- |
| `npm run lint` / `lint:fix` | ESLint (report-only / autofix) | Before pushing |
| `npm run format` / `format:check` | Prettier (write / check-only) | Before pushing |
| `npm run typecheck` | `tsc --noEmit` | Before pushing |
| `npm run check:size` | Fails on tracked files over the size limit (500KB default) | Before pushing |
| `npm run check` | Lint/format autofix + typecheck + size check | Before every push - what you run locally |
| `npm run check:ci` | Same, but report-only (writes nothing to disk) | What CI runs |

If your project generates types (e.g. Next.js route types), add that step before `tsc --noEmit` in `typecheck` -
see the sibling projects' `typecheck` scripts for an example.

Copy [`check-file-size.mjs`](check-file-size.mjs) into your project (e.g. `scripts/check-file-size.mjs`, matching
the `check:size` script above) - it walks `git ls-files` and fails on anything over `MAX_FILE_SIZE_KB`, checking
files on disk so it also catches something you've staged but haven't committed yet.

## CI

[`ci.yml`](ci.yml) is a standalone `frontend-checks` job. Copy it into your `.github/workflows/ci.yml` directly,
or merge it into a combined workflow - see [`templates/unified-ci.yml`](../../templates/unified-ci.yml) for what
that looks like alongside the Python jobs. Before copying, set:

- `working-directory` (both under `defaults.run` and `cache-dependency-path`) - the directory containing your
  `package.json`. Defaults to `Frontend`.
- `node-version` - pinned to `lts/*` by default; pin an exact version if your project needs one.

## Checks

What `frontend-checks` runs, via `npm run check:ci`:

| Check | Purpose |
|---|---|
| ESLint | Enforces your project's lint ruleset |
| Prettier Format | Enforces consistent formatting |
| TypeScript Type Check | Enforces static type correctness (`tsc --noEmit`) |
| File Size | Fails if a tracked file exceeds `MAX_FILE_SIZE_KB` (500KB default) in [`check-file-size.mjs`](check-file-size.mjs) |

## Editor setup (optional)

Install the [Prettier extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) for
VS Code to get the same formatting `npm run format` applies, inline as you type. Scope it per-language in your
`settings.json` so it doesn't take over a Python backend's files in the same repo:

```json
{
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```
