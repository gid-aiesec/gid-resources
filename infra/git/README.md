# `infra/git`

A local git hook that rejects a bad branch name before you ever push, so you don't find out from a failed CI run.
It's the fast, local half of branch naming enforcement - [`infra/branch`](../branch/README.md) is the CI-side
backstop that runs the same rule for anyone who skipped installing this hook.

## Installing it

Git doesn't version-control hooks, so this has to be copied in manually per clone:

```bash
cp infra/git/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Or, to point git at this directory directly instead of copying (works if `infra/git` stays at that path in your
repo):

```bash
git config core.hooksPath infra/git
```

## Checks

| Check | Purpose |
|---|---|
| Branch Name | Enforces `authorName/type-short-desc` convention for branches, e.g. `authorName/feature-add-hooks` |

## Customizing

The prefix list and pattern are duplicated in
[`hygiene/hooks/hygiene/branch_name.py`](../../hygiene/hooks/hygiene/branch_name.py) - a plain shell
script can't import a Python module, so if you add or rename a prefix, update both.
