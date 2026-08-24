# `templates`

Files meant to be copied whole into a downstream repo, rather than read for reference.

## `unified-ci.yml`

All three [`infra/`](../infra/README.md) CI jobs (branch checks, backend checks, frontend checks) merged into one
workflow. Copy it to `.github/workflows/ci.yml` in your repo, then work through the `CONFIGURE` comments inside -
each job's `working-directory` needs to point at wherever your `pyproject.toml` / `package.json` actually live.
If you only need one or two of the three jobs (e.g. a Python-only repo with no frontend), delete the job you
don't need, or start from the individual fragment in `infra/<branch|js|python>/ci.yml` instead.

## `PULL_REQUEST_TEMPLATE.md`

Copy it to `.github/PULL_REQUEST_TEMPLATE.md` - GitHub attaches it to every new PR automatically, no other
config needed. The section headers are a menu, not a fixed structure: the comment block at the top of the file
explains how to trim, rename, or add sections per-PR. To change the *default* set of sections for every future
PR, edit the template file itself rather than the comment.
