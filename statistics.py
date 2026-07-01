"""
statistics.py — Folder Statistics

Walks a directory tree and collects metrics: total files, total folders,
category breakdowns, folder size, and largest / smallest files.

Optionally exports the report to a CSV file.
"""

import csv
import os
from datetime import datetime

from config import EXTENSION_MAP, DEFAULT_CATEGORY, Color
from logger import get_logger
from utils import format_size

log = get_logger()


def _categorize(filename: str) -> str:
    """Return the category name for *filename*."""
    _, ext = os.path.splitext(filename)
    return EXTENSION_MAP.get(ext.lower(), DEFAULT_CATEGORY)


def gather_statistics(folder: str) -> dict | None:
    """Walk *folder* and return a statistics dictionary.

    Returns ``None`` if the folder is empty or inaccessible.

    Keys in the returned dict:
        total_files, total_folders, category_counts,
        total_size, largest_file, smallest_file
    """
    log.info("STATS | Started — target: %s", folder)

    stats: dict = {
        "total_files": 0,
        "total_folders": 0,
        "category_counts": {},
        "total_size": 0,
        "largest_file": ("", 0),
        "smallest_file": ("", float("inf")),
    }

    try:
        for dirpath, dirnames, filenames in os.walk(folder):
            stats["total_folders"] += len(dirnames)

            for fname in filenames:
                filepath = os.path.join(dirpath, fname)

                try:
                    size = os.path.getsize(filepath)
                except OSError:
                    size = 0

                stats["total_files"] += 1
                stats["total_size"] += size

                # Category tally
                cat = _categorize(fname)
                stats["category_counts"][cat] = (
                    stats["category_counts"].get(cat, 0) + 1
                )

                # Largest / smallest tracking
                if size > stats["largest_file"][1]:
                    stats["largest_file"] = (fname, size)
                if size < stats["smallest_file"][1]:
                    stats["smallest_file"] = (fname, size)

        # Edge case: no files found
        if stats["total_files"] == 0:
            stats["smallest_file"] = ("N/A", 0)
            stats["largest_file"] = ("N/A", 0)

        log.info(
            "STATS | Completed — %d files, %d folders, %s total",
            stats["total_files"],
            stats["total_folders"],
            format_size(stats["total_size"]),
        )
        return stats

    except PermissionError:
        log.error("STATS | Permission denied: %s", folder)
        print(Color.err("Permission denied on the target folder."))
    except OSError as exc:
        log.error("STATS | Unexpected OS error: %s", exc)
        print(Color.err(f"Unexpected error: {exc}"))

    return None


def display_statistics(folder: str) -> None:
    """Pretty-print folder statistics to the terminal."""
    stats = gather_statistics(folder)
    if stats is None:
        return

    cat = stats["category_counts"]
    largest_name, largest_size = stats["largest_file"]
    smallest_name, smallest_size = stats["smallest_file"]

    rows = [
        ("📁 Total Files", str(stats["total_files"])),
        ("📂 Total Folders", str(stats["total_folders"])),
        ("", ""),  # spacer
        ("🖼  Images", str(cat.get("Images", 0))),
        ("📄 Documents", str(cat.get("Documents", 0))),
        ("🎬 Videos", str(cat.get("Videos", 0))),
        ("🎵 Music", str(cat.get("Music", 0))),
        ("📦 Archives", str(cat.get("Archives", 0))),
        ("⚙  Programs", str(cat.get("Programs", 0))),
        ("📎 Others", str(cat.get("Others", 0))),
        ("", ""),
        ("💾 Total Size", format_size(stats["total_size"])),
        ("🔺 Largest File", f"{largest_name} ({format_size(largest_size)})"),
        ("🔻 Smallest File", f"{smallest_name} ({format_size(smallest_size)})"),
    ]

    # Determine column widths
    label_w = max(len(r[0]) for r in rows if r[0]) + 2

    for label, value in rows:
        if not label:
            print()
            continue
        print(f"    {Color.CYAN}{label:<{label_w}}{Color.RESET} {value}")

    print()


# ──────────────────────────────────────────────
# CSV export (extra feature)
# ──────────────────────────────────────────────

def export_statistics_csv(folder: str, output_dir: str | None = None) -> str | None:
    """Export folder statistics to a CSV file.

    Parameters:
        folder: Target directory to analyse.
        output_dir: Where to write the CSV.  Defaults to *folder* itself.

    Returns:
        The path of the generated CSV, or ``None`` on failure.
    """
    stats = gather_statistics(folder)
    if stats is None:
        return None

    if output_dir is None:
        output_dir = folder

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"folder_stats_{timestamp}.csv")

    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Files", stats["total_files"]])
            writer.writerow(["Total Folders", stats["total_folders"]])
            writer.writerow(["Total Size (bytes)", stats["total_size"]])
            writer.writerow(["Largest File", stats["largest_file"][0]])
            writer.writerow(["Largest File Size", stats["largest_file"][1]])
            writer.writerow(["Smallest File", stats["smallest_file"][0]])
            writer.writerow(["Smallest File Size", stats["smallest_file"][1]])

            writer.writerow([])
            writer.writerow(["Category", "Count"])
            for cat_name, count in sorted(stats["category_counts"].items()):
                writer.writerow([cat_name, count])

        log.info("STATS | Exported CSV to %s", csv_path)
        print(Color.ok(f"Statistics exported to {csv_path}"))
        return csv_path

    except OSError as exc:
        log.error("STATS | CSV export failed: %s", exc)
        print(Color.err(f"Could not export CSV: {exc}"))
        return None
