"""Migration: Post Batch Defer Jobs

Revision ID: 0035
Revises: 0034
Create Date: Auto-generated

SQL Migration: 03.02.00_50_post_batch_defer_jobs.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0035"
down_revision = "0034"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 03.02.00_50_post_batch_defer_jobs.sql migration."""
    op.execute(get_migration_sql("03.02.00_50_post_batch_defer_jobs.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
