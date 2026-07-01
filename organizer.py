"""
organizer.py — Organize Files by Extension

Scans a target folder, creates category sub-folders (Images, Documents,
Videos, Music, Archives, Programs, Others), and moves each file into the
matching category based on its extension.
"""

import os
import shutil

from config import EXTENSION_MAP, DEFAULT_CATEGORY, ALL_CATEGORIES, Color
from logger import get_logger
from utils import progress_bar

log = get_logger()


def _get_category(filename: str) -> str:
    """Determine the category for *filename* based on its extension."""
    _, ext = os.path.splitext(filename)
    return EXTENSION_MAP.get(ext.lower(), DEFAULT_CATEGORY)


def organize_files(folder: str) -> int:
    """Organize every file in *folder* into category sub-directories.

    Parameters:
        folder: Absolute path to the target directory.

    Returns:
        Number of files successfully moved.
    """
    log.info("ORGANIZE | Started — target: %s", folder)
    moved = 0

    try:
        # Collect only files (skip directories and our own category folders)
        entries = [
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        ]

        if not entries:
            print(Color.warn("No files found in the folder."))
            log.info("ORGANIZE | No files to organize in %s", folder)
            return 0

        total = len(entries)
        print(f"  {Color.info(f'Found {total} file(s). Organizing…')}\n")

        # Pre-create all category folders so the progress bar is smooth
        for cat in ALL_CATEGORIES:
            os.makedirs(os.path.join(folder, cat), exist_ok=True)

        for idx, filename in enumerate(entries, start=1):
            src = os.path.join(folder, filename)
            category = _get_category(filename)
            dest_dir = os.path.join(folder, category)
            dest = os.path.join(dest_dir, filename)

            try:
                # Handle duplicate filenames
                if os.path.exists(dest):
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(dest):
                        dest = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                        counter += 1
                    log.warning(
                        "ORGANIZE | Duplicate detected — renamed to %s",
                        os.path.basename(dest),
                    )

                shutil.move(src, dest)
                moved += 1
                log.info(
                    "ORGANIZE | Moved '%s' → %s/", filename, category
                )

            except PermissionError:
                log.error("ORGANIZE | Permission denied: %s", filename)
                print(Color.err(f"Permission denied: {filename}"))
            except OSError as exc:
                log.error("ORGANIZE | OS error for '%s': %s", filename, exc)
                print(Color.err(f"Error moving {filename}: {exc}"))

            progress_bar(idx, total)

        print(f"\n  {Color.ok(f'{moved} file(s) organized successfully.')}\n")
        log.info("ORGANIZE | Completed — %d file(s) moved", moved)

    except PermissionError:
        log.error("ORGANIZE | Permission denied on folder: %s", folder)
        print(Color.err("Permission denied on the target folder."))
    except OSError as exc:
        log.error("ORGANIZE | Unexpected OS error: %s", exc)
        print(Color.err(f"Unexpected error: {exc}"))

    return moved
