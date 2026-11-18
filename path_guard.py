import os
import posixpath
import re
from urllib.parse import unquote

BASE = "/srv/data"

_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:[\\/]")


def _validate(user_path):
    if not isinstance(user_path, str):
        raise ValueError("path must be a string")

    decoded = unquote(user_path)

    if not decoded:
        raise ValueError("empty path")
    if "\x00" in decoded:
        raise ValueError("null byte is not allowed in path")
    if "\\" in decoded:
        raise ValueError("backslash is not allowed in path")
    if _WINDOWS_DRIVE_RE.match(decoded):
        raise ValueError("windows drive path is not allowed")
    if posixpath.isabs(decoded):
        raise ValueError("absolute path is not allowed")

    return decoded


def _is_within_base(resolved, base):
    return resolved == base or resolved.startswith(base + os.sep)


def resolve_path(user_path):
    decoded = _validate(user_path)

    normalized = posixpath.normpath(decoded)
    if normalized == ".." or normalized.startswith("../"):
        raise ValueError("path escapes base directory")

    base = os.path.abspath(str(BASE))
    resolved = os.path.normpath(os.path.join(base, normalized))

    if not _is_within_base(resolved, base):
        raise ValueError("path escapes base directory")

    return resolved


def is_allowed(user_path):
    try:
        resolve_path(user_path)
    except (ValueError, TypeError):
        return False
    return True
