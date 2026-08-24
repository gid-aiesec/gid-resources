"""JSON/TOML/YAML syntax, JSON formatting, markdown lint, and large-file checks."""

import subprocess
import sys

from .reporting import print_hook_line
from .utils import git_tracked_files, repo_root, run_hook_process


def run_check_json(target_path: str) -> int:
    """Check that JSON files under `target_path` parse. Syntax-only - see `run_json_format` for style."""

    files = git_tracked_files(target_path, ".json")
    return run_hook_process("check json", files, ["pre_commit_hooks.check_json"], skip_reason="no .json files")


def run_json_format(target_path: str, *, check: bool) -> int:
    """
    Check that JSON files under `target_path` are consistently formatted, autofixing unless `check`.

    Passes `--no-sort-keys` so it normalizes whitespace without reordering keys.
    """

    label = "pretty format json"
    files = git_tracked_files(target_path, ".json")
    if not files:
        print_hook_line(label, "Skipped", reason="no .json files")
        return 0

    args = ["--no-sort-keys"] if check else ["--autofix", "--no-sort-keys"]
    result = subprocess.run(
        [sys.executable, "-m", "pre_commit_hooks.pretty_format_json", *args, *files],
        capture_output=True,
        text=True,
        check=False,
    )
    print_hook_line(label, "Passed" if result.returncode == 0 else "Failed")
    if result.returncode:
        print(result.stdout + result.stderr, end="", flush=True)
    return result.returncode


def run_check_toml(target_path: str) -> int:
    """Check that TOML files under `target_path` parse."""

    files = git_tracked_files(target_path, ".toml")
    return run_hook_process("check toml", files, ["pre_commit_hooks.check_toml"], skip_reason="no .toml files")


def run_check_yaml(target_path: str) -> int:
    """Check that YAML files under `target_path` parse."""

    files = git_tracked_files(target_path, ".yml", ".yaml")
    return run_hook_process("check yaml", files, ["pre_commit_hooks.check_yaml"], skip_reason="no .yml/.yaml files")


def run_large_file_check(target_path: str) -> int:
    """Check that no tracked file under `target_path` exceeds 500KB."""

    files = git_tracked_files(target_path)
    return run_hook_process("check for added large files", files, ["pre_commit_hooks.check_added_large_files"])


def run_markdown_lint(*, check: bool) -> int:
    """
    Lint every markdown file in the repo with pymarkdown, always repo-wide regardless of `target_path` scoping
    elsewhere. Autofixes first unless `check`, then re-scans - pymarkdown's `fix` exit code means "changed
    something", not "still broken", so a scan is the only way to get a real pass/fail signal.
    """

    label = "markdown lint"
    files = git_tracked_files(repo_root(), ".md")
    if not files:
        print_hook_line(label, "Skipped", reason="no .md files")
        return 0

    if not check:
        subprocess.run([sys.executable, "-m", "pymarkdown", "fix", *files], capture_output=True, text=True, check=False)
    result = subprocess.run(
        [sys.executable, "-m", "pymarkdown", "scan", *files], capture_output=True, text=True, check=False
    )
    print_hook_line(label, "Passed" if result.returncode == 0 else "Failed")
    if result.returncode:
        print(result.stdout + result.stderr, end="", flush=True)
    return result.returncode
