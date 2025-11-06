"""Migration: Fix Finish Job Compat Issue

Revision ID: 0019
Revises: 0018
Create Date: Auto-generated

SQL Migration: 00.18.01_01_fix_finish_job_compat_issue.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0019"
down_revision = "0018"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.18.01_01_fix_finish_job_compat_issue.sql migration."""
    op.execute(get_migration_sql("00.18.01_01_fix_finish_job_compat_issue.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
