"""Migration: Job Id Bigint

Revision ID: 0024
Revises: 0023
Create Date: Auto-generated

SQL Migration: 01.01.01_01_job_id_bigint.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0024"
down_revision = "0023"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 01.01.01_01_job_id_bigint.sql migration."""
    op.execute(get_migration_sql("01.01.01_01_job_id_bigint.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
