"""Migration: Drop Procrastinate Version Table

Revision ID: 0004
Revises: 0003
Create Date: Auto-generated

SQL Migration: 00.05.00_03_drop_procrastinate_version_table.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.05.00_03_drop_procrastinate_version_table.sql migration."""
    op.execute(get_migration_sql("00.05.00_03_drop_procrastinate_version_table.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
