"""
renamer.py — Bulk File Renaming

Renames every file in a directory using a user-supplied prefix and a
zero-padded sequential counter, preserving the original extension.

Example: ``Report_001.pdf``, ``Report_002.docx``, …
"""

import os

from config import Color
from logger import get_logger
from utils import progress_bar

log = get_logger()


def bulk_rename(folder: str, prefix: str) -> int:
    """Rename all files in *folder* to ``<prefix>_NNN.<ext>``.

    Parameters:
        folder: Absolute path to the target directory.
        prefix: The new filename prefix (e.g., ``Project``).

    Returns:
        Number of files successfully renamed.
    """
    log.info("RENAME | Started — folder: %s, prefix: '%s'", folder, prefix)
    renamed = 0

    try:
        entries = sorted(
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        )

        if not entries:
            print(Color.warn("No files found in the folder."))
            log.info("RENAME | No files to rename in %s", folder)
            return 0

        total = len(entries)
        # Zero-pad width based on total count (at least 3 digits)
        pad = max(3, len(str(total)))

        print(f"  {Color.info(f'Renaming {total} file(s)…')}\n")

        for idx, old_name in enumerate(entries, start=1):
            _, ext = os.path.splitext(old_name)
            new_name = f"{prefix}_{str(idx).zfill(pad)}{ext}"

            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)

            try:
                # Avoid overwriting an existing file with the same name
                if os.path.exists(new_path) and old_path != new_path:
                    counter = 1
                    base_new = f"{prefix}_{str(idx).zfill(pad)}"
                    while os.path.exists(new_path):
                        new_name = f"{base_new}_{counter}{ext}"
                        new_path = os.path.join(folder, new_name)
                        counter += 1
                    log.warning(
                        "RENAME | Collision resolved — '%s' → '%s'",
                        old_name, new_name,
                    )

                os.rename(old_path, new_path)
                renamed += 1
                log.info("RENAME | '%s' → '%s'", old_name, new_name)

            except PermissionError:
                log.error("RENAME | Permission denied: %s", old_name)
                print(Color.err(f"Permission denied: {old_name}"))
            except OSError as exc:
                log.error("RENAME | OS error for '%s': %s", old_name, exc)
                print(Color.err(f"Error renaming {old_name}: {exc}"))

            progress_bar(idx, total)

        print(f"\n  {Color.ok(f'{renamed} file(s) renamed successfully.')}\n")
        log.info("RENAME | Completed — %d file(s) renamed", renamed)

    except PermissionError:
        log.error("RENAME | Permission denied on folder: %s", folder)
        print(Color.err("Permission denied on the target folder."))
    except OSError as exc:
        log.error("RENAME | Unexpected OS error: %s", exc)
        print(Color.err(f"Unexpected error: {exc}"))

    return renamed
