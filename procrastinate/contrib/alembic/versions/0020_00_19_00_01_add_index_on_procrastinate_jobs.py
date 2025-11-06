"""Migration: Add Index On Procrastinate Jobs

Revision ID: 0020
Revises: 0019
Create Date: Auto-generated

SQL Migration: 00.19.00_01_add_index_on_procrastinate_jobs.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0020"
down_revision = "0019"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.19.00_01_add_index_on_procrastinate_jobs.sql migration."""
    op.execute(get_migration_sql("00.19.00_01_add_index_on_procrastinate_jobs.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
