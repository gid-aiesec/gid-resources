"""Individual precommit hooks (code quality, file checks, fixers, hygiene) and their terminal reporting."""

from .code_quality import run_mypy, run_ruff_format, run_ruff_lint
from .files import (
    run_check_json,
    run_check_toml,
    run_check_yaml,
    run_json_format,
    run_large_file_check,
    run_markdown_lint,
)
from .fixers import run_eof_fixer, run_whitespace_fixer
from .hygiene_checks import run_branch_name_check, run_case_check, run_debug_stmt_check, run_illegal_windows_check
from .repo_wide import REPO_WIDE_HOOK_NAMES, run_repo_wide_hooks
from .reporting import print_banner

__all__ = [
    "REPO_WIDE_HOOK_NAMES",
    "print_banner",
    "run_branch_name_check",
    "run_case_check",
    "run_check_json",
    "run_check_toml",
    "run_check_yaml",
    "run_debug_stmt_check",
    "run_eof_fixer",
    "run_illegal_windows_check",
    "run_json_format",
    "run_large_file_check",
    "run_markdown_lint",
    "run_mypy",
    "run_repo_wide_hooks",
    "run_ruff_format",
    "run_ruff_lint",
    "run_whitespace_fixer",
]
