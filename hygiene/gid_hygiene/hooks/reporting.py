"""Pre-commit-framework-style terminal output: section banners and per-hook status lines."""

import shutil
import sys

_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_RESET = "\033[0m"
_USE_COLOR = sys.stdout.isatty()

_STATUS_COLORS = {"Passed": _GREEN, "Failed": _RED, "Skipped": _YELLOW}
_WIDTH_FRACTION = 0.75


def _render_width() -> int:
    return int(shutil.get_terminal_size(fallback=(80, 24)).columns * _WIDTH_FRACTION)


def print_banner(title: str) -> None:
    """Print a `title` banner padded with `=` to the render width."""

    print("\n" + f" {title} ".center(_render_width(), "="), flush=True)


def print_hook_line(label: str, status: str, reason: str | None = None) -> None:
    """Print one hook result line: `label`, dot-padded, an optional `(reason)`, then `status`."""

    suffix = f"({reason}) " if reason else ""
    coloured_status = f"\033[1m{_STATUS_COLORS[status]}{status}{_RESET}" if _USE_COLOR else status
    dots = "." * max(1, _render_width() - len(label) - len(suffix) - len(status))
    print(f"{label}{dots}{suffix}{coloured_status}", flush=True)
