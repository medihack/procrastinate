# Use Procrastinate with Alembic

Procrastinate provides built-in support for [Alembic](https://alembic.sqlalchemy.org/), the database migration tool for SQLAlchemy. This integration allows you to manage Procrastinate schema migrations alongside your application's migrations.

```{toctree}
---
maxdepth: 1
---
alembic/basic_usage
alembic/migrations
```

## Overview

The Alembic integration provides:

- Pre-built migration versions for all Procrastinate schema changes
- Utilities to load and execute Procrastinate SQL migrations
- Support for zero-downtime deployments with pre/post migrations
- Template files for easy project integration

## Installation

Install Procrastinate with Alembic support:

```console
$ pip install "procrastinate[sqlalchemy]" alembic
```

Note: While Procrastinate's Alembic migrations work with SQLAlchemy, you don't need to use SQLAlchemy as your Procrastinate connector. The migrations are pure SQL and can be used with any PostgreSQL connector (psycopg, psycopg2, aiopg, etc.).

## Quick Start

1. Initialize Alembic in your project (if not already done):

```console
$ alembic init alembic
```

2. Copy Procrastinate migration versions to your project:

```console
$ python -c "import procrastinate.contrib.alembic as pa, shutil; shutil.copytree(pa.__path__[0] + '/versions', 'alembic/versions_procrastinate', dirs_exist_ok=True)"
```

3. Configure your `alembic/env.py` to include Procrastinate migrations by setting the version locations:

```python
# In your alembic/env.py
config.set_main_option(
    'version_locations',
    'alembic/versions alembic/versions_procrastinate'
)
```

4. Run migrations:

```console
$ alembic upgrade head
```

## Learn More

- {doc}`alembic/basic_usage` - Integration patterns and setup options
- {doc}`alembic/migrations` - Understanding and managing Procrastinate migrations
- {doc}`production/migrations` - Migration strategies for production deployments
