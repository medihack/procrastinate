# Procrastinate Canvas: Workflow Composition

Procrastinate now supports Celery-style canvas primitives for composing complex workflows. This feature allows you to chain tasks together, execute tasks in parallel, and coordinate callbacks.

## Overview

Canvas provides three main primitives:

- **Chain**: Execute tasks sequentially, passing results from one to the next
- **Group**: Execute tasks in parallel
- **Chord**: Execute tasks in parallel, then execute a callback with all results

## Signatures

A signature is a frozen task call that can be composed with other signatures:

```python
from procrastinate import App

app = App(connector=...)

@app.task
async def add(x, y):
    return x + y

# Create a signature
sig = add.s(x=2, y=3)  # or add.signature(x=2, y=3)

# Execute the signature
job_id = await sig.apply_async()
```

## Chains

Chains execute tasks sequentially, passing the result of each task to the next one.

### Using the pipe operator

```python
@app.task
async def add(x, y):
    return x + y

@app.task
async def multiply(result, factor):
    return result * factor

# Chain tasks together
workflow = add.s(x=2, y=3) | multiply.s(factor=10)
await workflow.apply_async()

# This will:
# 1. Execute add(2, 3) -> returns 5
# 2. Execute multiply(5, 10) -> returns 50
```

### Using the chain function

```python
from procrastinate import chain

workflow = chain(
    add.s(x=2, y=3),
    multiply.s(factor=10),
    add.s(y=100)
)
await workflow.apply_async()
```

### Accessing the previous result

Tasks in a chain can access the result from the previous task using the `_canvas_result` parameter:

```python
@app.task
async def process(_canvas_result):
    # _canvas_result contains the return value from the previous task
    return _canvas_result * 2
```

## Groups

Groups execute tasks in parallel:

```python
from procrastinate import group

@app.task
async def process_item(item_id):
    # Process individual item
    return f"Processed {item_id}"

# Execute multiple tasks in parallel
g = group(process_item.s(item_id=i) for i in range(10))
job_ids = await g.apply_async()

# Returns a list of job IDs for all tasks
```

## Chords

Chords execute a group of tasks in parallel, then execute a callback with all the results:

```python
from procrastinate import chord, group

@app.task
async def fetch_data(url):
    # Fetch data from URL
    return {"url": url, "data": ...}

@app.task
async def aggregate_results(_canvas_result):
    # _canvas_result is a list of all results from the header group
    # [result1, result2, result3, ...]
    return {
        "total": len(_canvas_result),
        "summary": ...
    }

# Fetch data from multiple URLs, then aggregate
workflow = chord(
    group(fetch_data.s(url=url) for url in urls),
    aggregate_results.s()
)
await workflow.apply_async()
```

## Complete Example

Here's a complete example combining all primitives:

```python
from procrastinate import App, chain, chord, group, PsycopgConnector

# Setup
connector = PsycopgConnector(host="localhost", dbname="procrastinate")
app = App(connector=connector)

# Define tasks
@app.task
async def fetch_user(user_id):
    # Fetch user data
    return {"id": user_id, "name": f"User {user_id}"}

@app.task
async def enrich_user(_canvas_result):
    # Add additional data to user
    user = _canvas_result
    user["enriched"] = True
    return user

@app.task
async def calculate_stats(users):
    # Calculate statistics from all users
    return {
        "total_users": len(users),
        "enriched_count": sum(1 for u in users if u.get("enriched"))
    }

# Create workflow
async def process_users(user_ids):
    # For each user:
    # 1. Fetch user data
    # 2. Enrich the data
    # Then aggregate all results

    workflow = chord(
        group(
            chain(fetch_user.s(user_id=uid), enrich_user.s())
            for uid in user_ids
        ),
        calculate_stats.s()
    )

    job_id = await workflow.apply_async()
    return job_id

# Execute
await process_users([1, 2, 3, 4, 5])
```

## Database Schema

Canvas uses an additional database table for chord coordination:

```sql
CREATE TABLE procrastinate_canvas_chords (
    chord_id character varying(128) PRIMARY KEY,
    header_size integer NOT NULL,
    completed_count integer DEFAULT 0 NOT NULL,
    results jsonb DEFAULT '[]' NOT NULL,
    callback_task_name character varying(128) NOT NULL,
    callback_kwargs jsonb DEFAULT '{}' NOT NULL,
    callback_options jsonb DEFAULT '{}' NOT NULL,
    created_at timestamp with time zone DEFAULT NOW() NOT NULL
);
```

Make sure to apply the migration when upgrading:

```bash
procrastinate schema --apply
```

## Important Notes

1. **Return Values**: Tasks in chains and chords should return JSON-serializable values since results are stored in the database.

2. **Error Handling**: If a task in a chain fails, the chain stops and subsequent tasks are not executed.

3. **Chord Consistency**: Chords use database-level coordination to ensure exactly-once callback execution even in the presence of failures.

4. **Canvas Result Parameter**: Tasks that receive results from previous tasks should accept a `_canvas_result` parameter. This parameter is automatically populated by the canvas system.

5. **Worker Requirements**: Make sure your workers are running and processing jobs for canvas workflows to execute properly.

## API Reference

### Signature

```python
task.s(**kwargs) -> Signature
task.signature(**kwargs) -> Signature
```

Create a signature for a task with the given arguments.

### Chain

```python
chain(*signatures) -> Chain
sig1 | sig2 | sig3 -> Chain
```

Create a chain of tasks that execute sequentially.

### Group

```python
group(*signatures) -> Group
group(iterable_of_signatures) -> Group
```

Create a group of tasks that execute in parallel.

### Chord

```python
chord(header: Group | Iterable[Signature], body: Signature) -> Chord
```

Create a chord with a header group and a body callback.

## Migration from Celery

If you're migrating from Celery, the canvas API should be familiar:

- `task.s()` → same as Celery
- `chain()` → same as Celery
- `group()` → same as Celery
- `chord()` → same as Celery
- Pipe operator (`|`) → same as Celery

Main differences:
- All operations are `async`
- Use `apply_async()` instead of `delay()`
- Results are passed via `_canvas_result` parameter instead of being prepended to args
