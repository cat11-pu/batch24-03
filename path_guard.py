import os

BASE = "/srv/data"


def resolve_path(user_path):
    return os.path.join(BASE, user_path)


def is_allowed(user_path):
    resolved = resolve_path(user_path)
    return resolved.startswith(BASE)
