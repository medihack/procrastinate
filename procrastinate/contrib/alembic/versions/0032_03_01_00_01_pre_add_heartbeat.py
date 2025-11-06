"""Migration: Pre Add Heartbeat

Revision ID: 0032
Revises: 0031
Create Date: Auto-generated

SQL Migration: 03.01.00_01_pre_add_heartbeat.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0032"
down_revision = "0031"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 03.01.00_01_pre_add_heartbeat.sql migration."""
    op.execute(get_migration_sql("03.01.00_01_pre_add_heartbeat.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
