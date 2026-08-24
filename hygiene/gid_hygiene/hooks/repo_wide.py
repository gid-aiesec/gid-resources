"""Hooks shared between `precommit` (skippable, scoped to a path) and `branchcheck` (always all of them,
repo-wide): branch naming, markdown, YAML/TOML syntax, large files, illegal Windows names, EOF, whitespace.

JSON is excluded on purpose - `precommit` autofixes JSON formatting while `branchcheck` only checks that it
parses, since a JS/TS formatter may already own JSON style repo-wide. See `pre_commit.py`/`branch_check.py`."""

from .files import run_check_toml, run_check_yaml, run_large_file_check, run_markdown_lint
from .fixers import run_eof_fixer, run_whitespace_fixer
from .hygiene_checks import run_branch_name_check, run_illegal_windows_check

REPO_WIDE_HOOK_NAMES = ("branch_name", "markdown", "yaml", "toml", "large_file", "illegal_windows", "eof", "whitespace")


def run_repo_wide_hooks(target_path: str, *, check: bool, skip: frozenset[str] = frozenset()) -> list[int]:
    """Run every repo-wide hygiene check against `target_path`, skipping any name in `skip`."""

    codes = []
    if "branch_name" not in skip:
        codes.append(run_branch_name_check())
    if "markdown" not in skip:
        codes.append(run_markdown_lint(check=check))
    if "yaml" not in skip:
        codes.append(run_check_yaml(target_path))
    if "toml" not in skip:
        codes.append(run_check_toml(target_path))
    if "large_file" not in skip:
        codes.append(run_large_file_check(target_path))
    if "illegal_windows" not in skip:
        codes.append(run_illegal_windows_check(target_path))
    if "eof" not in skip:
        codes.append(run_eof_fixer(target_path, check=check))
    if "whitespace" not in skip:
        codes.append(run_whitespace_fixer(target_path, check=check))
    return codes
