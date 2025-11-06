"""Migration: Initial

Revision ID: 0001
Revises: None
Create Date: Auto-generated

SQL Migration: 00.00.00_01_initial.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.00.00_01_initial.sql migration."""
    op.execute(get_migration_sql("00.00.00_01_initial.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
