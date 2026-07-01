"""
main.py — Entry Point & CLI Menu

Presents a beautiful, emoji-rich menu-driven interface and dispatches
user choices to the appropriate feature module.
"""

import os
import sys

from config import APP_VERSION, Color
from logger import get_logger
from utils import print_header, separator, ask_folder, ask_text, confirm

from organizer import organize_files
from renamer import bulk_rename
from cleaner import delete_empty_folders
from statistics import display_statistics, export_statistics_csv

log = get_logger()

# ──────────────────────────────────────────────
# Menu rendering
# ──────────────────────────────────────────────

BANNER = rf"""
{Color.BOLD}{Color.CYAN}
  ╔══════════════════════════════════════════════╗
  ║                                              ║
  ║     📁  SMART  FILE  ORGANIZER  📁          ║
  ║         v{APP_VERSION}                            ║
  ║                                              ║
  ╚══════════════════════════════════════════════╝
{Color.RESET}"""

MENU = f"""
  {Color.BOLD}{Color.WHITE}  MAIN MENU{Color.RESET}
  {Color.DIM}{separator("─", 42)}{Color.RESET}

  {Color.GREEN}  1.{Color.RESET}  🗂  Organize Files by Extension
  {Color.GREEN}  2.{Color.RESET}  ✏️  Rename Multiple Files
  {Color.GREEN}  3.{Color.RESET}  🗑  Delete Empty Folders
  {Color.GREEN}  4.{Color.RESET}  📊  Display Folder Statistics
  {Color.GREEN}  5.{Color.RESET}  📋  View Operation Log
  {Color.GREEN}  6.{Color.RESET}  📤  Export Statistics to CSV
  {Color.GREEN}  0.{Color.RESET}  🚪  Exit

  {Color.DIM}{separator("─", 42)}{Color.RESET}
"""


# ──────────────────────────────────────────────
# Feature handlers
# ──────────────────────────────────────────────

def handle_organize() -> None:
    """Prompt for a folder and organize its files."""
    print_header("🗂  ORGANIZE FILES BY EXTENSION")
    folder = ask_folder("Enter the folder to organize")
    if not folder:
        return
    if confirm(f"Organize files in '{folder}'?"):
        organize_files(folder)


def handle_rename() -> None:
    """Prompt for a folder and a prefix, then bulk-rename files."""
    print_header("✏️  BULK RENAME FILES")
    folder = ask_folder("Enter the folder containing files to rename")
    if not folder:
        return
    prefix = ask_text("🏷  Enter new filename prefix (e.g., Project)")
    if confirm(f"Rename all files in '{folder}' with prefix '{prefix}'?"):
        bulk_rename(folder, prefix)


def handle_clean() -> None:
    """Prompt for a folder and remove its empty sub-directories."""
    print_header("🗑  DELETE EMPTY FOLDERS")
    folder = ask_folder("Enter the root folder to scan")
    if not folder:
        return
    if confirm(f"Delete all empty sub-folders inside '{folder}'?"):
        delete_empty_folders(folder)


def handle_statistics() -> None:
    """Prompt for a folder and display its statistics."""
    print_header("📊  FOLDER STATISTICS")
    folder = ask_folder("Enter the folder to analyse")
    if not folder:
        return
    display_statistics(folder)


def handle_view_log() -> None:
    """Display the last 40 lines of the operations log."""
    print_header("📋  OPERATION LOG (last 40 entries)")

    log_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "logs", "operations.log"
    )

    if not os.path.isfile(log_path):
        print(Color.warn("No log file found yet. Perform an operation first.\n"))
        return

    try:
        with open(log_path, encoding="utf-8") as fh:
            lines = fh.readlines()
        tail = lines[-40:] if len(lines) > 40 else lines

        for line in tail:
            # Colour-code by severity
            stripped = line.strip()
            if "| ERROR" in stripped:
                print(f"    {Color.RED}{stripped}{Color.RESET}")
            elif "| WARNING" in stripped:
                print(f"    {Color.YELLOW}{stripped}{Color.RESET}")
            else:
                print(f"    {Color.DIM}{stripped}{Color.RESET}")
        print()

    except OSError as exc:
        print(Color.err(f"Could not read log file: {exc}"))


def handle_export_csv() -> None:
    """Export folder statistics to a CSV file."""
    print_header("📤  EXPORT STATISTICS TO CSV")
    folder = ask_folder("Enter the folder to analyse")
    if not folder:
        return
    export_statistics_csv(folder)


# ──────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────

DISPATCH = {
    "1": handle_organize,
    "2": handle_rename,
    "3": handle_clean,
    "4": handle_statistics,
    "5": handle_view_log,
    "6": handle_export_csv,
}


def main() -> None:
    """Application entry point — runs the interactive menu loop."""
    # Enable ANSI colours on Windows 10+
    if sys.platform == "win32":
        os.system("")  # triggers VT100 support in cmd.exe / PowerShell

    print(BANNER)
    log.info("SESSION | Application started (v%s)", APP_VERSION)

    while True:
        print(MENU)
        choice = input(f"  {Color.YELLOW}👉 Choose an option: {Color.RESET}").strip()

        if choice == "0":
            print(f"\n  {Color.ok('Goodbye! Have a great day. 👋')}\n")
            log.info("SESSION | Application exited by user")
            break

        handler = DISPATCH.get(choice)
        if handler:
            try:
                handler()
            except KeyboardInterrupt:
                print(f"\n{Color.warn('Operation interrupted.')}\n")
                log.warning("SESSION | Operation interrupted by user (Ctrl+C)")
            except Exception as exc:
                print(Color.err(f"An unexpected error occurred: {exc}"))
                log.exception("SESSION | Unhandled exception")
        else:
            print(Color.warn("Invalid option. Please enter 0–6.\n"))


if __name__ == "__main__":
    main()
