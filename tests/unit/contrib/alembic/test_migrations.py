from __future__ import annotations

import importlib
from pkgutil import iter_modules

from procrastinate.contrib import alembic


def test_no_missing_migration():
    """
    Ensure all SQL migrations have corresponding Alembic migration files.

    This test verifies that:
    1. Each SQL migration file has an Alembic migration that references it
    2. No SQL migration is referenced multiple times
    3. The migration chain is complete
    """
    import re
    from pathlib import Path

    # Get the versions directory path
    versions = importlib.import_module("procrastinate.contrib.alembic.versions")
    path = Path(next(iter(versions.__path__)))

    # Collect all SQL file names referenced in Alembic migrations
    referenced_sql_files = []

    for migration_file in path.glob("*.py"):
        # Skip __init__.py and non-migration files
        if migration_file.name == "__init__.py":
            continue

        # Read the file content directly instead of importing
        content = migration_file.read_text()

        # Use regex to find get_migration_sql("filename.sql")
        match = re.search(r'get_migration_sql\("([^"]+)"\)', content)
        if match:
            sql_filename = match.group(1)
            referenced_sql_files.append(sql_filename)

    # Get all SQL migrations
    sql_migrations = list(alembic.list_migration_files().keys())

    # Check that all SQL migrations are referenced
    assert set(sql_migrations) == set(referenced_sql_files), (
        "If this test fails, you probably need to add "
        "an Alembic migration file in procrastinate/contrib/alembic/versions/ "
        "referencing a SQL file recently added in procrastinate/sql/migrations/ "
        "or remove references to SQL files that no longer exist."
    )

    # Check that no SQL migration is referenced multiple times
    assert len(sql_migrations) == len(referenced_sql_files), (
        "If this test fails, you probably reference the same SQL migration "
        "file multiple times in the Alembic migrations in "
        "procrastinate/contrib/alembic/versions/"
    )


def test_migration_chain():
    """
    Verify that Alembic migrations form a proper chain.

    Each migration should have a unique revision ID and properly reference
    the previous migration via down_revision.
    """
    import re
    from pathlib import Path

    versions = importlib.import_module("procrastinate.contrib.alembic.versions")
    path = Path(next(iter(versions.__path__)))

    revisions = {}
    down_revisions = []

    for migration_file in path.glob("*.py"):
        if migration_file.name == "__init__.py":
            continue

        # Read the file content directly
        content = migration_file.read_text()

        # Extract revision and down_revision using regex
        revision_match = re.search(r'^revision = ["\']([^"\']+)["\']', content, re.MULTILINE)
        down_revision_match = re.search(
            r'^down_revision = (["\'][^"\']*["\']|None)', content, re.MULTILINE
        )

        if revision_match and down_revision_match:
            revision = revision_match.group(1)
            down_revision_str = down_revision_match.group(1)

            # Parse down_revision (it can be None or a quoted string)
            if down_revision_str == "None":
                down_revision = None
            else:
                down_revision = down_revision_str.strip('"\'')

            # Check for duplicate revision IDs
            assert revision not in revisions, (
                f"Duplicate revision ID: {revision} in "
                f"{migration_file.name} and {revisions[revision]}"
            )

            revisions[revision] = migration_file.name
            down_revisions.append(down_revision)

    # Check that the chain is continuous
    # All down_revisions (except None for the first migration) should exist as revisions
    for down_rev in down_revisions:
        if down_rev is not None:
            assert down_rev in revisions, (
                f"Broken migration chain: down_revision {down_rev} "
                f"does not exist as a revision ID"
            )
