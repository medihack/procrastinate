"""Migration: Add Foreign Key Index

Revision ID: 0011
Revises: 0010
Create Date: Auto-generated

SQL Migration: 00.12.00_01_add_foreign_key_index.sql
"""
from alembic import op

from procrastinate.contrib.alembic import get_migration_sql


# revision identifiers, used by Alembic.
revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the 00.12.00_01_add_foreign_key_index.sql migration."""
    op.execute(get_migration_sql("00.12.00_01_add_foreign_key_index.sql"))


def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
