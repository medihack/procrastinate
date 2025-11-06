"""Migration: Add Kwargs To Defer Periodic Job

Revision ID: 0021
Revises: 0020
Create Date: Auto-generated

SQL Migration: 00.22.00_01_add_kwargs_to_defer_periodic_job.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0021"
down_revision = "0020"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.22.00_01_add_kwargs_to_defer_periodic_job.sql migration."""
    op.execute(get_migration_sql("00.22.00_01_add_kwargs_to_defer_periodic_job.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
