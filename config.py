"""
config.py — Configuration & Constants

Centralizes file extension categories, color codes, and application
settings so every other module imports from one place.
"""

# ──────────────────────────────────────────────
# Application metadata
# ──────────────────────────────────────────────
APP_NAME = "Smart File Organizer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# ──────────────────────────────────────────────
# Extension → category mapping
# ──────────────────────────────────────────────
EXTENSION_MAP: dict[str, str] = {
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".webp": "Images", ".bmp": "Images",
    ".svg": "Images",
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".ppt": "Documents", ".pptx": "Documents",
    ".xls": "Documents", ".xlsx": "Documents", ".csv": "Documents",
    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos",
    ".avi": "Videos",
    # Music
    ".mp3": "Music", ".wav": "Music", ".flac": "Music",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives",
    ".tar": "Archives", ".gz": "Archives",
    # Programs
    ".exe": "Programs", ".msi": "Programs",
}

DEFAULT_CATEGORY = "Others"

# All possible target folders (used when creating sub-directories)
ALL_CATEGORIES: list[str] = [
    "Images", "Documents", "Videos", "Music",
    "Archives", "Programs", "Others",
]

# ──────────────────────────────────────────────
# ANSI colour helpers (no external dependency)
# ──────────────────────────────────────────────
class Color:
    """ANSI escape sequences for terminal colours."""

    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    BG_BLUE = "\033[44m"

    @staticmethod
    def ok(msg: str) -> str:
        return f"{Color.GREEN}✔ {msg}{Color.RESET}"

    @staticmethod
    def warn(msg: str) -> str:
        return f"{Color.YELLOW}⚠ {msg}{Color.RESET}"

    @staticmethod
    def err(msg: str) -> str:
        return f"{Color.RED}✖ {msg}{Color.RESET}"

    @staticmethod
    def info(msg: str) -> str:
        return f"{Color.CYAN}ℹ {msg}{Color.RESET}"

    @staticmethod
    def heading(msg: str) -> str:
        return f"{Color.BOLD}{Color.MAGENTA}{msg}{Color.RESET}"


# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
LOG_DIR = "logs"
LOG_FILE = "operations.log"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
