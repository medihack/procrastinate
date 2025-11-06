"""Migration: Close Fetch Job Race Condition

Revision ID: 0008
Revises: 0007
Create Date: Auto-generated

SQL Migration: 00.10.00_01_close_fetch_job_race_condition.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.10.00_01_close_fetch_job_race_condition.sql migration."""
    op.execute(get_migration_sql("00.10.00_01_close_fetch_job_race_condition.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
