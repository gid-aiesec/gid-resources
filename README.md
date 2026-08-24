<div style="display: flex; justify-content: center;">
    <img
        src="assets/GIDlogo2.svg"
        alt="GID Logo"
        width="400"
    />
</div>

# GID Resources

Shared infrastructure and templates for GID repositories - CI checks, git hooks, and PR conventions meant to be
copied into a project rather than reinvented per-repo.

## Layout

| Directory | What's in it |
| --- | --- |
| [`infra/`](infra/README.md) | CI job fragments (branch, git hook, JS/TS, Python) - copy what applies to your stack |
| [`hygiene/`](hygiene/README.md) | The Python package behind `infra/python`'s and `infra/branch`'s CI jobs |
| [`templates/`](templates/README.md) | Files meant to be copied whole: a combined CI workflow, a PR template |

Start with [`infra/README.md`](infra/README.md) if you're wiring CI into a new repo, or
[`templates/README.md`](templates/README.md) if you just want the combined workflow and PR template dropped in
as-is.

## More Docs

| Doc | Covers |
| --- | --- |
| [`infra/README.md`](infra/README.md) | Overview of the four CI/hook pieces and how they combine |
| [`infra/branch/README.md`](infra/branch/README.md) | CI-side branch naming + repo-wide file hygiene |
| [`infra/git/README.md`](infra/git/README.md) | Local pre-commit hook for branch naming |
| [`infra/js/README.md`](infra/js/README.md) | JS/TS lint, format, typecheck, file-size CI job |
| [`infra/python/README.md`](infra/python/README.md) | Python ruff/mypy/hygiene CI job + config |
| [`hygiene/README.md`](hygiene/README.md) | The `precommit`/`branchcheck` scripts themselves |
| [`templates/README.md`](templates/README.md) | Installing the combined CI workflow and PR template |

## Developer Guides
[aies.ec/developer-guides](https://aies.ec/developer-guides)
