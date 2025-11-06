"""Migration: Add Periodic Job Priority

Revision ID: 0026
Revises: 0025
Create Date: Auto-generated

SQL Migration: 02.05.00_01_add_periodic_job_priority.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0026"
down_revision = "0025"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 02.05.00_01_add_periodic_job_priority.sql migration."""
    op.execute(get_migration_sql("02.05.00_01_add_periodic_job_priority.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
