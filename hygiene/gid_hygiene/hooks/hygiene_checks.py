"""Repo hygiene checks that aren't specific to any file type: branch naming, case conflicts, debug statements,
and illegal Windows filenames."""

import os
import re
import subprocess

from .reporting import print_hook_line
from .utils import git_tracked_files, run_hook_process

VALID_PREFIXES = ("feature", "fix", "chore", "docs", "refactor", "hotfix", "test", "perf", "style", "ci")
EXEMPT_BRANCHES = ("main", "staging")
_BRANCH_PATTERN = re.compile(rf"^[a-z0-9]+/({'|'.join(VALID_PREFIXES)})-[a-z0-9]+(-[a-z0-9]+)*$")

WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def run_branch_name_check() -> int:
    """Check the current branch matches `author/prefix-short-desc` (main/staging exempt)."""

    label = "check branch name"
    branch = (
        os.environ.get("GITHUB_HEAD_REF")  # CI checks out pull_request events in detached HEAD
        or subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    )

    if branch in EXEMPT_BRANCHES:
        print_hook_line(label, "Skipped", reason=f"on {branch}")
        return 0

    if not _BRANCH_PATTERN.match(branch):
        print_hook_line(label, "Failed")
        print(
            f"{branch}: doesn't match author/prefix-short-desc (prefix one of {', '.join(VALID_PREFIXES)})",
            flush=True,
        )
        return 1

    print_hook_line(label, "Passed")
    return 0


def run_case_check(target_path: str) -> int:
    """Check that no two tracked files under `target_path` differ only by case."""

    files = git_tracked_files(target_path)
    return run_hook_process("check for case conflicts", files, ["pre_commit_hooks.check_case_conflict"])


def run_debug_stmt_check(target_path: str) -> int:
    """Check that no tracked Python file under `target_path` has a leftover debugger call."""

    files = git_tracked_files(target_path, ".py")
    return run_hook_process(
        "debug statements (python)", files, ["pre_commit_hooks.debug_statement_hook"], skip_reason="no .py files"
    )


def run_illegal_windows_check(target_path: str) -> int:
    """
    Check that no tracked file under `target_path` has a Windows-illegal name: a reserved device name, or a
    name ending in a dot or space. Hand-rolled - no such hook exists in `pre-commit-hooks`.
    """

    label = "check illegal windows names"
    files = git_tracked_files(target_path)
    if not files:
        print_hook_line(label, "Skipped", reason="no files to check")
        return 0

    violations = []
    for path in files:
        name = path.rsplit("/", 1)[-1]
        stem = name.split(".", 1)[0].upper()
        if stem in WINDOWS_RESERVED_NAMES or name != name.rstrip(". "):
            violations.append(path)

    print_hook_line(label, "Failed" if violations else "Passed")
    for path in violations:
        print(f"{path}: illegal filename on Windows", flush=True)

    return 1 if violations else 0
