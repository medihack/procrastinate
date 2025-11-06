"""Migration: Pre Priority Lock Fetch Job

Revision ID: 0036
Revises: 0035
Create Date: Auto-generated

SQL Migration: 03.03.00_01_pre_priority_lock_fetch_job.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0036"
down_revision = "0035"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 03.03.00_01_pre_priority_lock_fetch_job.sql migration."""
    op.execute(get_migration_sql("03.03.00_01_pre_priority_lock_fetch_job.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
