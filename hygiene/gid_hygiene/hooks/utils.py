"""Shared helpers: repo-root resolution, git file listing, and generic hook-process runners."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .reporting import print_hook_line

TEXT_EXTENSIONS = (".py", ".md", ".json", ".toml", ".yml", ".yaml")


def repo_root() -> str:
    """Absolute path to the repository root, regardless of the caller's cwd."""

    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def git_tracked_files(target_path: str, *extensions: str) -> list[str]:
    """List git-tracked files under `target_path`, optionally filtered by `extensions` (e.g. `".py"`)."""

    result = subprocess.run(["git", "ls-files", "--", target_path], capture_output=True, text=True, check=True)
    files = result.stdout.splitlines()
    return [f for f in files if not extensions or f.endswith(extensions)]


def run_hook_process(label: str, files: list[str], args: list[str], *, skip_reason: str = "no files to check") -> int:
    """Run a `python -m` command (`args`) against `files`, printing a status line for `label`."""

    if not files:
        print_hook_line(label, "Skipped", reason=skip_reason)
        return 0

    result = subprocess.run([sys.executable, "-m", *args, *files], capture_output=True, text=True, check=False)
    print_hook_line(label, "Passed" if result.returncode == 0 else "Failed")
    if result.returncode:
        print(result.stdout + result.stderr, end="", flush=True)
    return result.returncode


def run_ci_fixers(module: str, files: list[str]) -> tuple[int, str]:
    """
    Run fixer `module` against throwaway copies of `files` so nothing on disk changes - for fixers with no
    native check-only mode (end-of-file-fixer, trailing-whitespace-fixer).
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_to_original = {}
        for file in files:
            tmp_path = Path(tmp_dir) / file.replace("/", "__")
            shutil.copyfile(file, tmp_path)
            tmp_to_original[str(tmp_path)] = file

        result = subprocess.run(
            [sys.executable, "-m", module, *tmp_to_original], capture_output=True, text=True, check=False
        )
        output = result.stdout + result.stderr
        for tmp_file, original in tmp_to_original.items():
            output = output.replace(tmp_file, original)
        return result.returncode, output
