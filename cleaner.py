"""
cleaner.py — Delete Empty Folders

Recursively walks a directory tree (bottom-up) and removes any folder
that contains no files or sub-directories.
"""

import os

from config import Color
from logger import get_logger

log = get_logger()


def delete_empty_folders(folder: str) -> int:
    """Remove all empty directories under *folder* (inclusive).

    The scan is **bottom-up** so that nested empty folders are removed
    before their parents are checked.

    Parameters:
        folder: Absolute path to the root directory to scan.

    Returns:
        Number of empty folders deleted.
    """
    log.info("CLEAN | Started — target: %s", folder)
    deleted = 0

    try:
        # os.walk with topdown=False ensures children are visited first
        for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
            # Skip the root folder itself to avoid deleting the user's target
            if os.path.abspath(dirpath) == os.path.abspath(folder):
                continue

            try:
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
                    deleted += 1
                    log.info("CLEAN | Deleted empty folder: %s", dirpath)
                    print(f"    {Color.DIM}🗑  Removed: {dirpath}{Color.RESET}")

            except PermissionError:
                log.error("CLEAN | Permission denied: %s", dirpath)
                print(Color.err(f"Permission denied: {dirpath}"))
            except OSError as exc:
                log.error("CLEAN | OS error for '%s': %s", dirpath, exc)
                print(Color.err(f"Error deleting {dirpath}: {exc}"))

        if deleted:
            print(f"\n  {Color.ok(f'{deleted} empty folder(s) deleted.')}\n")
        else:
            print(f"  {Color.info('No empty folders found.')}\n")

        log.info("CLEAN | Completed — %d folder(s) deleted", deleted)

    except PermissionError:
        log.error("CLEAN | Permission denied on root folder: %s", folder)
        print(Color.err("Permission denied on the target folder."))
    except OSError as exc:
        log.error("CLEAN | Unexpected OS error: %s", exc)
        print(Color.err(f"Unexpected error: {exc}"))

    return deleted
