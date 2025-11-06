"""Migration: Add Additional Params To Retry Job

Revision ID: 0028
Revises: 0027
Create Date: Auto-generated

SQL Migration: 02.08.00_01_add_additional_params_to_retry_job.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0028"
down_revision = "0027"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 02.08.00_01_add_additional_params_to_retry_job.sql migration."""
    op.execute(get_migration_sql("02.08.00_01_add_additional_params_to_retry_job.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
