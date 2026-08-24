# `infra/branch`

CI-side branch naming and repo-wide file hygiene gate. Enforces the same `author/prefix-short-desc` convention as
[`infra/git/pre-commit`](../git/README.md), plus markdown, JSON/TOML/YAML syntax, large files, illegal Windows
filenames (i.e. names reserved for Windows processes), end-of-file, and trailing whitespace checks across the whole repo.

The git hook catches a bad branch name locally, before you push; this job catches it (and everything else) in
CI, as a backstop for anyone who skipped or doesn't have the local hook installed.

It runs `uv run branchcheck`, so it depends on [`hygiene`](../../hygiene/README.md) being set up in
your Python project even if the rest of your repo is JS/TS - see that package's README for what `branchcheck`
actually checks and why it's a separate job from `precommit` instead of folded into
[`infra/python`](../python/README.md)'s `backend-checks`.

## CI

Copy [`ci.yml`](ci.yml) into your `.github/workflows/ci.yml`, or merge it into a combined workflow - see
[`templates/unified-ci.yml`](../../templates/unified-ci.yml). Before copying, set `working-directory` to the
directory containing your `pyproject.toml`.

## Checks

| Check | Purpose |
|---|---|
| Branch Name | Enforces `authorName/type-short-desc` convention for branches, e.g. `authorName/feature-add-hooks` |
| Markdown Linting | Enforces clean markdown structuring and line lengths for consistency |
| YAML Syntax | Fails if a `.yml`/`.yaml` file doesn't parse |
| TOML Syntax | Fails if a `.toml` file doesn't parse |
| JSON Syntax | Fails if a `.json` file doesn't parse - style is left to your own formatter (e.g. Prettier), unlike `precommit`'s JSON check |
| Large File Size | Fails if a tracked file exceeds 500KB (see [`hygiene`](../../hygiene/README.md#what-you-can-change) to change the limit) |
| Illegal Windows Filenames | Fails on reserved device names (`CON`, `PRN`, `COM1`, ...) or names ending in a dot/space, which break checkouts on Windows |
| End-of-File Fixer | Ensures tracked text files end in exactly one newline |
| Trailing Whitespace Fixer | Strips trailing whitespace from tracked text files |

