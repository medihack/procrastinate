"""Migration: Pre Add Retry Failed Job Procedure

Revision ID: 0037
Revises: 0036
Create Date: Auto-generated

SQL Migration: 03.04.00_01_pre_add_retry_failed_job_procedure.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0037"
down_revision = "0036"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 03.04.00_01_pre_add_retry_failed_job_procedure.sql migration."""
    op.execute(get_migration_sql("03.04.00_01_pre_add_retry_failed_job_procedure.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
