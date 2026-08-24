# `infra`

CI checks and git hooks for a downstream repo, split by concern so you only take what applies to your stack.
Each subdirectory is self-contained: a `README.md` explaining what it does and what to configure, plus the actual
`ci.yml` fragment or hook to copy in.

| Directory | What it gives you |
| --- | --- |
| [`branch/`](branch/README.md) | CI job: branch naming + repo-wide file hygiene |
| [`git/`](git/README.md) | Local pre-commit hook: branch naming, before you push |
| [`js/`](js/README.md) | CI job: lint, format, typecheck, file size for a JS/TS project |
| [`python/`](python/README.md) | CI job: ruff, mypy, hygiene checks for a Python project, via [`hygiene`](../hygiene/README.md) |

None of these are wired into workflow triggers of their own once combined - see
[`templates/unified-ci.yml`](../templates/unified-ci.yml) for all four `ci.yml` fragments merged into one
ready-to-copy workflow, or copy individual fragments into your own `.github/workflows/` if you only need some of
them.

## Prerequisites

- **uv** - manages Python version, dependencies, and the `hygiene` scripts. Install it from the
  [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) (e.g.
  `curl -LsSf https://astral.sh/uv/install.sh | sh` on macOS/Linux); no separate Python or virtual env setup
  needed, uv handles both.
- **Node.js + npm / npx** - for the JS/TS side, if you're using [`js/`](js/README.md).
