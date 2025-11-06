"""Migration: Add Checks To Finish Job

Revision ID: 0017
Revises: 0016
Create Date: Auto-generated

SQL Migration: 00.17.00_03_add_checks_to_finish_job.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.17.00_03_add_checks_to_finish_job.sql migration."""
    op.execute(get_migration_sql("00.17.00_03_add_checks_to_finish_job.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
