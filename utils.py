"""
utils.py — Shared Utility Functions

Provides path validation, formatting helpers, a simple progress bar,
and other reusable pieces used across feature modules.
"""

import os
import sys

from config import Color


# ──────────────────────────────────────────────
# Path validation
# ──────────────────────────────────────────────

def validate_folder(path: str) -> str:
    """Return the absolute path if *path* is a valid directory.

    Raises:
        FileNotFoundError: Path does not exist.
        NotADirectoryError: Path exists but is not a directory.
        PermissionError: Insufficient permissions to access the directory.
    """
    abs_path = os.path.abspath(path)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Path does not exist: {abs_path}")

    if not os.path.isdir(abs_path):
        raise NotADirectoryError(f"Path is not a directory: {abs_path}")

    # Quick read-access check
    if not os.access(abs_path, os.R_OK):
        raise PermissionError(f"No read permission: {abs_path}")

    return abs_path


# ──────────────────────────────────────────────
# Formatting helpers
# ──────────────────────────────────────────────

def format_size(size_bytes: int | float) -> str:
    """Convert bytes to a human-readable string (KB / MB / GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / 1024 ** 2:.2f} MB"
    else:
        return f"{size_bytes / 1024 ** 3:.2f} GB"


def separator(char: str = "═", length: int = 50) -> str:
    """Return a visual separator line."""
    return char * length


def print_header(title: str) -> None:
    """Print a boxed section header."""
    line = separator()
    print(f"\n{Color.BOLD}{Color.CYAN}{line}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}  {title}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}{line}{Color.RESET}\n")


# ──────────────────────────────────────────────
# Progress bar
# ──────────────────────────────────────────────

def progress_bar(current: int, total: int, bar_length: int = 30) -> None:
    """Render an in-place progress bar on stdout."""
    if total == 0:
        return
    fraction = current / total
    filled = int(bar_length * fraction)
    bar = "█" * filled + "░" * (bar_length - filled)
    percent = fraction * 100
    sys.stdout.write(f"\r  {Color.CYAN}[{bar}] {percent:5.1f}%{Color.RESET}")
    sys.stdout.flush()
    if current == total:
        sys.stdout.write("\n")


# ──────────────────────────────────────────────
# User input helpers
# ──────────────────────────────────────────────

def ask_folder(prompt: str = "Enter folder path") -> str:
    """Prompt the user for a folder path with validation.

    Returns the validated absolute path, or raises SystemExit on 'q'.
    """
    while True:
        raw = input(f"  {Color.YELLOW}📂 {prompt} (or 'q' to cancel): {Color.RESET}").strip()
        if raw.lower() == "q":
            print(Color.info("Cancelled.\n"))
            return ""
        try:
            return validate_folder(raw)
        except (FileNotFoundError, NotADirectoryError, PermissionError) as exc:
            print(Color.err(str(exc)))


def ask_text(prompt: str) -> str:
    """Prompt the user for a non-empty text string."""
    while True:
        raw = input(f"  {Color.YELLOW}{prompt}: {Color.RESET}").strip()
        if raw:
            return raw
        print(Color.warn("Input cannot be empty. Try again."))


def confirm(prompt: str = "Proceed?") -> bool:
    """Ask for a yes/no confirmation."""
    ans = input(f"  {Color.YELLOW}{prompt} [y/N]: {Color.RESET}").strip().lower()
    return ans in ("y", "yes")
