"""Migration: Null Locks Excluded

Revision ID: 0022
Revises: 0021
Create Date: Auto-generated

SQL Migration: 00.23.00_01_null_locks_excluded.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0022"
down_revision = "0021"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.23.00_01_null_locks_excluded.sql migration."""
    op.execute(get_migration_sql("00.23.00_01_null_locks_excluded.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
