"""Ruff lint/format and mypy type checks."""

import subprocess
import sys


def run_ruff_lint(target_path: str, *, check: bool) -> int:
    """Lint `target_path` with ruff; autofixes unless `check`."""

    args = ["check"] if check else ["check", "--fix"]
    return subprocess.run([sys.executable, "-m", "ruff", *args, target_path], check=False).returncode


def run_ruff_format(target_path: str, *, check: bool) -> int:
    """Format `target_path` with ruff; only reports diffs if `check`."""

    args = ["format", "--check", "--diff"] if check else ["format"]
    return subprocess.run([sys.executable, "-m", "ruff", *args, target_path], check=False).returncode


def run_mypy(target_path: str) -> int:
    """Type check `target_path` with mypy."""

    return subprocess.run([sys.executable, "-m", "mypy", target_path], check=False).returncode
