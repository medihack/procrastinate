"""Migration: Add Queueing Lock Column

Revision ID: 0007
Revises: 0006
Create Date: Auto-generated

SQL Migration: 00.08.01_01_add_queueing_lock_column.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.08.01_01_add_queueing_lock_column.sql migration."""
    op.execute(get_migration_sql("00.08.01_01_add_queueing_lock_column.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
