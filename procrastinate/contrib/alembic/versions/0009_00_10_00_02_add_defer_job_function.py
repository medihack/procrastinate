"""Migration: Add Defer Job Function

Revision ID: 0009
Revises: 0008
Create Date: Auto-generated

SQL Migration: 00.10.00_02_add_defer_job_function.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.10.00_02_add_defer_job_function.sql migration."""
    op.execute(get_migration_sql("00.10.00_02_add_defer_job_function.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
