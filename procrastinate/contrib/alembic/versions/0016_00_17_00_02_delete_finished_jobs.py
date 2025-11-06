"""Migration: Delete Finished Jobs

Revision ID: 0016
Revises: 0015
Create Date: Auto-generated

SQL Migration: 00.17.00_02_delete_finished_jobs.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0016"
down_revision = "0015"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.17.00_02_delete_finished_jobs.sql migration."""
    op.execute(get_migration_sql("00.17.00_02_delete_finished_jobs.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
