# Procrastinate Alembic Integration

This package provides Alembic migration support for Procrastinate, allowing you to manage Procrastinate schema migrations using Alembic alongside your application's migrations.

## Overview

Similar to the Django integration, Procrastinate's Alembic migrations are wrappers around the SQL migration files located in `procrastinate/sql/migrations/`. This ensures consistency across different migration frameworks and maintains a single source of truth for the database schema.

## Setup

### 1. Initialize Alembic (if not already done)

If you haven't already initialized Alembic in your project:

```bash
alembic init alembic
```

### 2. Configure Alembic to use Procrastinate migrations

You have two options:

#### Option A: Use Procrastinate migrations in your existing Alembic setup

Import and use the provided migration versions in your Alembic `versions/` directory. The Procrastinate Alembic migrations are located in `procrastinate.contrib.alembic.versions`.

You can reference them in your own migrations as dependencies, or copy them into your project's versions directory.

#### Option B: Use a separate Alembic environment for Procrastinate

Create a separate Alembic configuration specifically for Procrastinate migrations:

1. Create a new directory for Procrastinate migrations:
   ```bash
   mkdir -p alembic_procrastinate/versions
   ```

2. Copy the template files:
   ```bash
   cp $(python -c "import procrastinate.contrib.alembic as pa; print(pa.__path__[0])")/env.py.template alembic_procrastinate/env.py
   cp $(python -c "import procrastinate.contrib.alembic as pa; print(pa.__path__[0])")/script.py.mako alembic_procrastinate/script.py.mako
   ```

3. Copy the migration versions:
   ```bash
   cp -r $(python -c "import procrastinate.contrib.alembic as pa; print(pa.__path__[0])")/versions/* alembic_procrastinate/versions/
   ```

4. Create an `alembic.ini` for Procrastinate or update your existing one to point to this directory.

### 3. Run migrations

```bash
# Check current status
alembic current

# Upgrade to latest
alembic upgrade head

# Upgrade to a specific revision
alembic upgrade <revision>
```

## Pre and Post Migrations

Similar to the standalone SQL migrations, some Alembic migrations are marked as `pre` or `post` migrations:

- **Pre migrations**: Must be applied BEFORE deploying new code
- **Post migrations**: Must be applied AFTER deploying new code

Migration file names follow the pattern: `{version}_{serial}_{pre|post}_{description}.py`

For zero-downtime deployments:

1. Apply all `pre` migrations
2. Deploy new application code
3. Apply all `post` migrations

See the [Procrastinate documentation](https://procrastinate.readthedocs.io/) for more information on migration strategies.

## How it works

Each Alembic migration in the `versions/` directory corresponds to a SQL migration file in `procrastinate/sql/migrations/`. The migrations use the `get_migration_sql()` function to load and execute the SQL content.

Example:
```python
from procrastinate.contrib.alembic import get_migration_sql

def upgrade():
    op.execute(get_migration_sql("00.00.00_01_initial.sql"))
```

## Keeping migrations in sync

The Procrastinate Alembic migrations are kept in sync with the SQL migrations in each Procrastinate release. When upgrading Procrastinate, make sure to:

1. Check the release notes for new migrations
2. Update your Alembic versions to include the new migrations
3. Run the migrations before or after deploying (depending on pre/post designation)

## Testing

To test that all SQL migrations have corresponding Alembic migrations:

```python
from procrastinate.contrib.alembic import list_migration_files

# List all available SQL migrations
sql_migrations = list_migration_files()
print(f"Found {len(sql_migrations)} SQL migrations")
```
