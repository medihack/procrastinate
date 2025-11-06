"""Migration: Add Trigger On Job Deletion

Revision ID: 0015
Revises: 0014
Create Date: Auto-generated

SQL Migration: 00.17.00_01_add_trigger_on_job_deletion.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.17.00_01_add_trigger_on_job_deletion.sql migration."""
    op.execute(get_migration_sql("00.17.00_01_add_trigger_on_job_deletion.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
