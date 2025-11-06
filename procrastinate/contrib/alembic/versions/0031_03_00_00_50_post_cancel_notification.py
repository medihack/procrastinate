"""Migration: Post Cancel Notification

Revision ID: 0031
Revises: 0030
Create Date: Auto-generated

SQL Migration: 03.00.00_50_post_cancel_notification.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0031"
down_revision = "0030"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 03.00.00_50_post_cancel_notification.sql migration."""
    op.execute(get_migration_sql("03.00.00_50_post_cancel_notification.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
