"""Migration: Post Add Heartbeat

Revision ID: 0033
Revises: 0032
Create Date: Auto-generated

SQL Migration: 03.01.00_50_post_add_heartbeat.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0033"
down_revision = "0032"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 03.01.00_50_post_add_heartbeat.sql migration."""
    op.execute(get_migration_sql("03.01.00_50_post_add_heartbeat.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
