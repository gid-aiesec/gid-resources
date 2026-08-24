"""Repo-wide branch naming and file hygiene gate, run as its own CI job."""

import argparse
import sys

from .hooks import print_banner, run_check_json, run_repo_wide_hooks
from .hooks.utils import repo_root


def main() -> None:
    """
    `branchcheck [--check]` - every repo-wide hygiene check (see `hooks.repo_wide`), unconditionally, plus a
    JSON syntax check. `--check` writes nothing to disk. See `hygiene/README.md` for why this is split from
    `precommit`.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parsed_args = parser.parse_args()
    check = parsed_args.check
    root = repo_root()

    print_banner("Running Branch & Repo-Wide File Checks")
    codes = run_repo_wide_hooks(root, check=check)
    codes.append(run_check_json(root))

    if any(codes):
        sys.exit(1)

    print("")
