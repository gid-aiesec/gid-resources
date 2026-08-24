# `infra/python`

CI and editor setup for a Python project, built on [`hygiene`](../../hygiene/README.md) - the
`precommit` and `branchcheck` commands defined there. Wired into [`ci.yml`](ci.yml) as two jobs (`backend-checks`,
`branch-checks`). Pair this with [`infra/js`](../js/README.md) for a JS/TS frontend, or drop it in on its own for
a Python-only repo.

## What to add to your `pyproject.toml`

`hygiene` isn't published to PyPI - copy the [`hygiene/`](../../hygiene) directory into your
project (repo root, alongside your `pyproject.toml`), then register its entry points and dependencies:

```toml
[project.scripts]
precommit = "hygiene.pre_commit:main"
branchcheck = "hygiene.branch_check:main"

[project.optional-dependencies]
dev = [
    "ruff",
    "mypy",
    "pre-commit-hooks",
    "pymarkdownlnt",
]
```

Then `uv sync` and run via `uv run precommit` / `uv run branchcheck` (see
[`hygiene/README.md`](../../hygiene/README.md) for what each does, and for the equivalent `pip`
workflow if your project doesn't use uv).

**Scripts:**

| Command | What it runs | When to use it |
| --- | --- | --- |
| `uv run precommit [PATH] [--check]` | ruff + mypy + hygiene checks | Before every push |
| `uv run branchcheck [--check]` | branch name + repo-wide file hygiene checks | Before every PR |

## Ruff, mypy, and markdown config

Add these to your `pyproject.toml`, adjusting for your project:

```toml
[tool.ruff]
target-version = "py313" # CONFIGURE: your Python version
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "N", "C90", "ARG", "RUF"]

[tool.ruff.lint.mccabe]
max-complexity = 24

[tool.mypy]
python_version = "3.13" # CONFIGURE: your Python version
strict = true

# CONFIGURE: only if your project uses Django - drop this plugin and [tool.django-stubs] otherwise
plugins = ["mypy_django_plugin.main"]

[tool.django-stubs]
django_settings_module = "yourproject.settings"

[tool.pymarkdown]
plugins.md013.line_length = 120
plugins.md013.table_line_length = 500
plugins.md013.heading_line_length = 120
plugins.md013.code_block_line_length = 120
plugins.md033.enabled = false # allow inline HTML (e.g. <details> blocks) in your READMEs
```

## CI

[`ci.yml`](ci.yml) has two independent jobs. Copy both into your `.github/workflows/ci.yml`, or merge them into a
combined workflow - see [`templates/unified-ci.yml`](../../templates/unified-ci.yml). Before copying, set:

- `working-directory` (both jobs) - the directory containing your `pyproject.toml`. Defaults to `Backend`.
- The `env:` block in `backend-checks` - add any environment variables your app needs to import cleanly during
  type checking.
- The mypy cache `key`/`path` - update the `Backend` prefix to match `working-directory` above.

`backend-checks` runs `precommit --check`, skipping the hygiene checks that `branch-checks` already covers
repo-wide (see [`hygiene/README.md`](../../hygiene/README.md#precommit) for why they're split this
way) - update the `--skip` list there if you rename or remove any `[project.scripts]` entries.

## Checks

What `backend-checks` actually runs in CI, given the `--skip` list above:

| Check | Purpose |
|---|---|
| Ruff Lint | Enforces the lint ruleset in `[tool.ruff.lint]` |
| Ruff Format | Enforces consistent formatting per `[tool.ruff]` |
| Mypy Type Check | Enforces static type correctness per `[tool.mypy]` |
| Case Conflict | Fails if two tracked files differ only by case - breaks checkouts on case-insensitive filesystems |
| Debug Statements | Fails if a tracked `.py` file has a leftover `pdb`/`breakpoint()` call |

`precommit` can also run every check in [`infra/branch`'s Checks table](../branch/README.md#checks) (branch
naming, markdown, JSON/TOML/YAML syntax, large files, illegal Windows names, end-of-file, trailing whitespace) -
that's what happens if you run `uv run precommit` locally without `--skip`. CI skips them here since
`branch-checks` already runs them repo-wide, in parallel.

## Editor setup (optional)

Install the [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) for VS Code
to get the same lint/format feedback `uv run precommit` runs, inline as you type. Scope the formatter to
`[python]` in your `settings.json` so it doesn't take over a JS/TS frontend's files in the same repo:

```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports.ruff": "explicit",
      "source.fixAll.ruff": "explicit"
    }
  }
}
```
