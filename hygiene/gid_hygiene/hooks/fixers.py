"""End-of-file and trailing-whitespace fixers. Both lack a native check-only mode, so `check` runs them against
throwaway copies via `utils.run_ci_fixers` instead of the real files."""

import subprocess
import sys

from .reporting import print_hook_line
from .utils import TEXT_EXTENSIONS, git_tracked_files, run_ci_fixers


def run_eof_fixer(target_path: str, *, check: bool) -> int:
    """Ensure tracked text files under `target_path` end in exactly one newline."""

    return _run_fixer("fix end of files", "pre_commit_hooks.end_of_file_fixer", target_path, check=check)


def run_whitespace_fixer(target_path: str, *, check: bool) -> int:
    """Strip trailing whitespace from tracked text files under `target_path`."""

    return _run_fixer(
        "trim trailing whitespace", "pre_commit_hooks.trailing_whitespace_fixer", target_path, check=check
    )


def _run_fixer(label: str, module: str, target_path: str, *, check: bool) -> int:
    files = git_tracked_files(target_path, *TEXT_EXTENSIONS)
    if not files:
        print_hook_line(label, "Skipped", reason="no text files")
        return 0

    if check:
        returncode, output = run_ci_fixers(module, files)
    else:
        result = subprocess.run([sys.executable, "-m", module, *files], capture_output=True, text=True, check=False)
        returncode, output = result.returncode, result.stdout + result.stderr

    print_hook_line(label, "Passed" if returncode == 0 else "Failed")
    if returncode:
        print(output, end="", flush=True)
    return returncode
