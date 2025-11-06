from __future__ import annotations

from procrastinate.contrib import alembic


def test_list_migration_files():
    """Test that migration files are properly loaded."""
    migrations = alembic.list_migration_files()

    # Check that initial migration exists
    migration = migrations["00.00.00_01_initial.sql"]
    assert migration.startswith(
        "CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;"
    )
    assert len(migration.splitlines()) == 187

    # Ensure __init__.py is excluded
    assert "__init__.py" not in migrations

    # Ensure all entries are SQL files
    for filename in migrations.keys():
        assert filename.endswith(".sql")


def test_get_migration_sql():
    """Test that individual migration SQL can be retrieved."""
    sql = alembic.get_migration_sql("00.00.00_01_initial.sql")

    assert sql.startswith(
        "CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;"
    )
    assert "CREATE TABLE procrastinate_jobs" in sql


def test_get_migration_sql_missing():
    """Test that missing migration raises KeyError."""
    try:
        alembic.get_migration_sql("nonexistent.sql")
        assert False, "Should have raised KeyError"
    except KeyError:
        pass  # Expected
