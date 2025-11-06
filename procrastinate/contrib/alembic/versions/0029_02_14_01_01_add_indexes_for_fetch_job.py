"""Migration: Add Indexes For Fetch Job

Revision ID: 0029
Revises: 0028
Create Date: Auto-generated

SQL Migration: 02.14.01_01_add_indexes_for_fetch_job.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0029"
down_revision = "0028"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 02.14.01_01_add_indexes_for_fetch_job.sql migration."""
    op.execute(get_migration_sql("02.14.01_01_add_indexes_for_fetch_job.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
