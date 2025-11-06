from __future__ import annotations

import functools
from importlib import resources


@functools.cache
def list_migration_files() -> dict[str, str]:
    """
    Returns a dict of filenames and file contents for all SQL migration files.
    """
    return {
        p.name: p.read_text(encoding="utf-8")
        for p in resources.files("procrastinate.sql.migrations").iterdir()
        if p.name.endswith(".sql")
    }


def get_migration_sql(name: str) -> str:
    """
    Get the SQL content for a specific migration file.

    Args:
        name: The migration filename (e.g., "00.00.00_01_initial.sql")

    Returns:
        The SQL content of the migration file
    """
    return list_migration_files()[name]


__all__ = [
    "list_migration_files",
    "get_migration_sql",
]
