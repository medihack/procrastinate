"""Migration: Remove Old Finish Job Function

Revision ID: 0023
Revises: 0022
Create Date: Auto-generated

SQL Migration: 01.00.00_01_remove_old_finish_job_function.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0023"
down_revision = "0022"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 01.00.00_01_remove_old_finish_job_function.sql migration."""
    op.execute(get_migration_sql("01.00.00_01_remove_old_finish_job_function.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
