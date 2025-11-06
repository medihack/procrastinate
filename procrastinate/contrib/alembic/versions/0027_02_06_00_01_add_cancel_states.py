"""Migration: Add Cancel States

Revision ID: 0027
Revises: 0026
Create Date: Auto-generated

SQL Migration: 02.06.00_01_add_cancel_states.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0027"
down_revision = "0026"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 02.06.00_01_add_cancel_states.sql migration."""
    op.execute(get_migration_sql("02.06.00_01_add_cancel_states.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
