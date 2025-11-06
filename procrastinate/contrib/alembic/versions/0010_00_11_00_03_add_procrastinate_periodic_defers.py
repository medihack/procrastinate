"""Migration: Add Procrastinate Periodic Defers

Revision ID: 0010
Revises: 0009
Create Date: Auto-generated

SQL Migration: 00.11.00_03_add_procrastinate_periodic_defers.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.11.00_03_add_procrastinate_periodic_defers.sql migration."""
    op.execute(get_migration_sql("00.11.00_03_add_procrastinate_periodic_defers.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
