# Basic Alembic Integration

This guide covers different ways to integrate Procrastinate migrations with Alembic in your project.

## Integration Options

There are three main approaches to using Procrastinate migrations with Alembic:

### Option 1: Multiple Version Locations (Recommended)

This approach keeps Procrastinate migrations separate from your application migrations, making upgrades easier.

**Setup:**

1. Create a directory for Procrastinate migrations:

```console
$ mkdir -p alembic/versions_procrastinate
```

2. Copy Procrastinate migration versions:

```python
# One-time setup script or in your deployment
import procrastinate.contrib.alembic as pa
import shutil
from pathlib import Path

src = Path(pa.__path__[0]) / "versions"
dst = Path("alembic/versions_procrastinate")
shutil.copytree(src, dst, dirs_exist_ok=True)
```

3. Update `alembic.ini` or `env.py` to use multiple version locations:

```python
# In alembic/env.py, before calling run_migrations_*()
config.set_main_option(
    'version_locations',
    'alembic/versions alembic/versions_procrastinate'
)
```

**Pros:**
- Clean separation between application and Procrastinate migrations
- Easy to upgrade (just replace the versions_procrastinate directory)
- Both sets of migrations tracked in the same Alembic history

**Cons:**
- Need to remember to copy migrations when upgrading Procrastinate

### Option 2: Import Procrastinate Migrations Directly

Use Procrastinate migrations from their installed location without copying.

**Setup:**

1. Update `alembic.ini` or `env.py` to include Procrastinate's versions directory:

```python
# In alembic/env.py
import procrastinate.contrib.alembic as pa
from pathlib import Path

procrastinate_versions = str(Path(pa.__path__[0]) / "versions")

config.set_main_option(
    'version_locations',
    f'alembic/versions {procrastinate_versions}'
)
```

**Pros:**
- No need to copy files
- Always up-to-date with installed Procrastinate version
- Simplest setup

**Cons:**
- Migrations are outside your project directory
- May be confusing where migrations come from

### Option 3: Separate Alembic Environment

Create a completely separate Alembic environment just for Procrastinate migrations.

**Setup:**

1. Create a separate directory:

```console
$ mkdir -p alembic_procrastinate/versions
```

2. Copy template files:

```console
$ python -c "import procrastinate.contrib.alembic as pa; import shutil; shutil.copy(pa.__path__[0] + '/env.py.template', 'alembic_procrastinate/env.py')"
$ python -c "import procrastinate.contrib.alembic as pa; import shutil; shutil.copy(pa.__path__[0] + '/script.py.mako', 'alembic_procrastinate/script.py.mako')"
```

3. Copy migration versions:

```console
$ python -c "import procrastinate.contrib.alembic as pa; import shutil; shutil.copytree(pa.__path__[0] + '/versions', 'alembic_procrastinate/versions', dirs_exist_ok=True)"
```

4. Create or update `alembic_procrastinate.ini` to point to this directory

5. Run migrations with:

```console
$ alembic -c alembic_procrastinate.ini upgrade head
```

**Pros:**
- Complete isolation between Procrastinate and application migrations
- Can manage Procrastinate migrations independently
- Clear ownership of migration state

**Cons:**
- Need to manage two separate Alembic environments
- More complex deployment process

## Configuration Examples

### Using with SQLAlchemy

If you're using SQLAlchemy with Procrastinate:

```python
# In your alembic/env.py
from procrastinate.contrib.sqlalchemy import App

# Configure Procrastinate App
app = App(connection_uri="postgresql://localhost/mydb")

# Use app's engine for migrations
with app.engine.begin() as connection:
    context.configure(
        connection=connection,
        target_metadata=None  # Procrastinate manages its own schema
    )

    with context.begin_transaction():
        context.run_migrations()
```

### Using with Other Connectors

Procrastinate migrations are pure SQL and work with any PostgreSQL connection:

```python
# In your alembic/env.py
import psycopg2

# Your regular database connection
conn = psycopg2.connect("postgresql://localhost/mydb")

# Alembic can use this connection
context.configure(
    connection=conn,
    target_metadata=None
)

with context.begin_transaction():
    context.run_migrations()
```

## Upgrading Procrastinate

When upgrading to a new Procrastinate version:

1. Check the [release notes](https://github.com/procrastinate-org/procrastinate/releases) for new migrations
2. Update your Procrastinate migrations:
   - **Option 1/3**: Re-copy the versions directory
   - **Option 2**: No action needed (automatically uses new versions)
3. Run `alembic upgrade head`

## Next Steps

- Learn about {doc}`migrations` for managing Procrastinate schema changes
- Read about {doc}`../production/migrations` for production deployment strategies
