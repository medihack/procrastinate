"""Migration: Pre Cancel Notification

Revision ID: 0030
Revises: 0029
Create Date: Auto-generated

SQL Migration: 03.00.00_01_pre_cancel_notification.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0030"
down_revision = "0029"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 03.00.00_01_pre_cancel_notification.sql migration."""
    op.execute(get_migration_sql("03.00.00_01_pre_cancel_notification.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
