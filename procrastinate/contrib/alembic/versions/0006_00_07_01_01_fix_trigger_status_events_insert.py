"""Migration: Fix Trigger Status Events Insert

Revision ID: 0006
Revises: 0005
Create Date: Auto-generated

SQL Migration: 00.07.01_01_fix_trigger_status_events_insert.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.07.01_01_fix_trigger_status_events_insert.sql migration."""
    op.execute(get_migration_sql("00.07.01_01_fix_trigger_status_events_insert.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
