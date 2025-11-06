"""Migration: Add Finish Job And Retry Job Functions

Revision ID: 0014
Revises: 0013
Create Date: Auto-generated

SQL Migration: 00.16.00_01_add_finish_job_and_retry_job_functions.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.16.00_01_add_finish_job_and_retry_job_functions.sql migration."""
    op.execute(get_migration_sql("00.16.00_01_add_finish_job_and_retry_job_functions.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
