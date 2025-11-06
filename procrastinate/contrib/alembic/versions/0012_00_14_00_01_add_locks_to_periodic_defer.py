"""Migration: Add Locks To Periodic Defer

Revision ID: 0012
Revises: 0011
Create Date: Auto-generated

SQL Migration: 00.14.00_01_add_locks_to_periodic_defer.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.14.00_01_add_locks_to_periodic_defer.sql migration."""
    op.execute(get_migration_sql("00.14.00_01_add_locks_to_periodic_defer.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
