"""Migration: Drop Started At Column

Revision ID: 0003
Revises: 0002
Create Date: Auto-generated

SQL Migration: 00.05.00_02_drop_started_at_column.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.05.00_02_drop_started_at_column.sql migration."""
    op.execute(get_migration_sql("00.05.00_02_drop_started_at_column.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
