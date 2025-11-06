"""Migration: Add Job Priority

Revision ID: 0025
Revises: 0024
Create Date: Auto-generated

SQL Migration: 02.00.03_01_add_job_priority.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0025"
down_revision = "0024"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 02.00.03_01_add_job_priority.sql migration."""
    op.execute(get_migration_sql("02.00.03_01_add_job_priority.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
