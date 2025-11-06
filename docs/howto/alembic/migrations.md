# Use Procrastinate Migrations with Alembic

Procrastinate comes with pre-built Alembic migrations that wrap the underlying SQL migrations, ensuring your database schema stays in sync with your Procrastinate version.

## Migration Types

Procrastinate provides two types of Alembic migrations:

### Standard Migrations

Most migrations are standard schema changes that can be applied anytime:

```
0001_00.00.00_01_initial.py
0002_00.05.00_01_drop_started_at_column.py
...
```

These migrations create tables, add columns, update functions, and modify indexes needed by Procrastinate.

### Pre and Post Migrations

For zero-downtime deployments, some migrations are split into `pre` and `post` versions:

```
0030_03.00.00_01_pre_cancel_notification.py
0031_03.00.00_50_post_cancel_notification.py
```

- **Pre migrations** (e.g., `01_pre_*`): Must be applied **before** deploying new code
- **Post migrations** (e.g., `50_post_*`): Must be applied **after** deploying new code

The `_50_` serial number in post migrations ensures they come after the corresponding pre migration in the sequence.

## Understanding Migration Revisions

Each Alembic migration has a revision ID (e.g., `0001`, `0002`) that:

- Forms a linear chain via `down_revision` links
- Corresponds to a specific SQL migration file
- Is kept in sync with Procrastinate versions

Example migration structure:

```python
"""Migration: Initial

Revision ID: 0001
Revises: None
Create Date: Auto-generated

SQL Migration: 00.00.00_01_initial.sql
"""
from alembic import op
from procrastinate.contrib.alembic import get_migration_sql

revision = "0001"
down_revision = None

def upgrade():
    """Apply the 00.00.00_01_initial.sql migration."""
    op.execute(get_migration_sql("00.00.00_01_initial.sql"))

def downgrade():
    """Downgrade is not supported for Procrastinate migrations."""
    raise NotImplementedError(
        "Downgrading Procrastinate migrations is not supported. "
        "Please restore from a database backup if needed."
    )
```

## Running Migrations

### Check Current Status

```console
$ alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
0030 (head)
```

### Upgrade to Latest

```console
$ alembic upgrade head
INFO  [alembic.runtime.migration] Running upgrade 0030 -> 0031, Migration: Post Cancel Notification
INFO  [alembic.runtime.migration] Running upgrade 0031 -> 0032, Migration: Pre Add Heartbeat
...
```

### Upgrade to Specific Revision

```console
$ alembic upgrade 0025
```

### View Migration History

```console
$ alembic history --verbose
```

### Show Pending Migrations

```console
$ alembic history -r current:head
```

## Zero-Downtime Deployments

When deploying Procrastinate upgrades without service interruption:

### 1. Identify Pre/Post Migrations

Check release notes or migration filenames for `pre` and `post` indicators:

```console
$ ls alembic/versions_procrastinate/ | grep -E "(pre|post)"
0030_03.00.00_01_pre_cancel_notification.py
0031_03.00.00_50_post_cancel_notification.py
0032_03.01.00_01_pre_add_heartbeat.py
0033_03.01.00_50_post_add_heartbeat.py
...
```

### 2. Apply Pre Migrations

Before deploying new code:

```console
# Upgrade to the last pre migration for your target version
$ alembic upgrade 0032  # Example: upgrading to 3.1.0
```

### 3. Deploy New Code

Deploy your application with the new Procrastinate version. The pre migrations ensure compatibility.

### 4. Apply Post Migrations

After deployment is complete:

```console
# Continue to head or next post migration
$ alembic upgrade head
```

## Migration Strategies

### With Service Interruption (Simpler)

1. Stop all services (workers and task deferrers)
2. Run `alembic upgrade head`
3. Deploy new application code
4. Start services

This is simpler but requires downtime.

### Without Service Interruption (Recommended for Production)

1. Apply pre migrations: `alembic upgrade <pre_revision>`
2. Deploy new code (old code continues running)
3. Verify deployment
4. Apply post migrations: `alembic upgrade head`

See {doc}`../production/migrations` for detailed production deployment strategies.

## Troubleshooting

### Migration Already Applied

If Alembic reports a migration is already applied:

```console
$ alembic stamp head
```

This updates Alembic's version table without running migrations.

### Migration Fails

If a migration fails:

1. Check PostgreSQL logs for errors
2. Verify database connectivity
3. Ensure no conflicting schema changes
4. Check that you're not downgrading (not supported)

### Starting Fresh

If you need to start over:

```console
# Drop Alembic version table
$ psql -d mydb -c "DROP TABLE IF EXISTS alembic_version;"

# Re-run migrations
$ alembic upgrade head
```

## Downgrade Not Supported

Procrastinate migrations do not support downgrading via Alembic's `downgrade()` function. This is intentional because:

- Database downgrades are complex and error-prone
- Data loss may occur during schema downgrades
- Better to restore from a backup if needed

If you must rollback:

1. Restore from a database backup taken before the migration
2. Deploy the previous Procrastinate version

## Keeping Migrations in Sync

Procrastinate's Alembic migrations are always kept in sync with your installed Procrastinate version:

- Migrations are shipped with each Procrastinate release
- Check release notes for new migrations when upgrading
- Test migrations in a staging environment before production

## Learn More

- {doc}`basic_usage` - Integration patterns and setup
- {doc}`../production/migrations` - Production deployment strategies
- [Alembic Documentation](https://alembic.sqlalchemy.org/) - Full Alembic reference
