"""Migration: Pre Batch Defer Jobs

Revision ID: 0034
Revises: 0033
Create Date: Auto-generated

SQL Migration: 03.02.00_01_pre_batch_defer_jobs.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0034"
down_revision = "0033"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 03.02.00_01_pre_batch_defer_jobs.sql migration."""
    op.execute(get_migration_sql("03.02.00_01_pre_batch_defer_jobs.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
