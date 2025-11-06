"""Migration: Fix Procrastinate Fetch Job

Revision ID: 0005
Revises: 0004
Create Date: Auto-generated

SQL Migration: 00.06.00_01_fix_procrastinate_fetch_job.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.06.00_01_fix_procrastinate_fetch_job.sql migration."""
    op.execute(get_migration_sql("00.06.00_01_fix_procrastinate_fetch_job.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
