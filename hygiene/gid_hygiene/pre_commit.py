"""Run ruff, mypy, and a set of hygiene checks as a single pre-commit gate."""

import argparse
import sys

from .hooks import (
    REPO_WIDE_HOOK_NAMES,
    print_banner,
    run_case_check,
    run_debug_stmt_check,
    run_json_format,
    run_mypy,
    run_repo_wide_hooks,
    run_ruff_format,
    run_ruff_lint,
)

SKIPPABLE_HOOK_NAMES = (*REPO_WIDE_HOOK_NAMES, "json")


def main() -> None:
    """
    `precommit [PATH] [--check] [--skip HOOKS]` - ruff, mypy, JSON formatting, and the repo-wide hygiene checks
    on `PATH` (default `.`), plus case-conflict and debug-statement checks. `--check` writes nothing to disk;
    anything fixable instead fails the run. See `hygiene/README.md` for the full behaviour.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--skip",
        default="",
        help=f"Comma-separated hooks to exclude: {', '.join(SKIPPABLE_HOOK_NAMES)}",
    )
    parsed_args = parser.parse_args()
    path = parsed_args.path
    check = parsed_args.check
    skip = frozenset(name for name in parsed_args.skip.split(",") if name)

    print_banner("Running Ruff checks and formatting")
    lint_code = run_ruff_lint(path, check=check)
    format_code = run_ruff_format(path, check=check)

    print_banner("Running MyPy checks")
    mypy_code = run_mypy(path)

    print_banner("Running Pre-Commit Hooks")
    hook_codes = run_repo_wide_hooks(path, check=check, skip=skip)
    if "json" not in skip:
        hook_codes.append(run_json_format(path, check=check))
    hook_codes.append(run_case_check(path))
    hook_codes.append(run_debug_stmt_check(path))

    if any([lint_code, format_code, mypy_code, *hook_codes]):
        sys.exit(1)

    print("")
