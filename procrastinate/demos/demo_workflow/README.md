# Workflow Demo - Job Dependencies

This demo shows how to use job dependencies in Procrastinate to create workflows where jobs must execute in a specific order.

## What are Job Dependencies?

Job dependencies allow you to specify that a job should only run after one or more parent jobs have **finished** (in any terminal status: succeeded, failed, cancelled, or aborted). This is useful for:

- Data processing pipelines
- Multi-step workflows
- Tasks that depend on the output of previous tasks
- Orchestrating complex job sequences
- Error handling workflows where you need to react to parent job failures

## How to Use

### Defining Dependencies

When deferring a job, use the `depends_on` parameter to specify which jobs must complete first:

```python
# Defer a parent job
parent_job_id = await parent_task.defer_async()

# Defer a child job that depends on the parent
child_job_id = await child_task.configure(
    depends_on=[parent_job_id]
).defer_async()
```

### Multiple Dependencies

A job can depend on multiple parent jobs. It will only run after ALL parent jobs have completed successfully:

```python
job_a_id = await task_a.defer_async()
job_b_id = await task_b.defer_async()

# This job waits for both job_a and job_b to complete
job_c_id = await task_c.configure(
    depends_on=[job_a_id, job_b_id]
).defer_async()
```

## Running the Demo

1. Make sure you have a PostgreSQL database configured
2. Apply migrations to add the job dependencies table
3. Run the demo to create the workflow:
   ```bash
   python -m procrastinate.demos.demo_workflow
   ```
4. Start a worker to execute the jobs:
   ```bash
   python -m procrastinate worker
   ```

You'll see the jobs execute in the correct order, with each job waiting for its dependencies to complete.

## Checking Parent Job Status

Jobs can check the status of their parent jobs to decide how to proceed:

```python
@app.task(pass_context=True)
async def process_data(context):
    # Get parent job statuses
    parent_statuses = await context.get_parent_statuses_async()

    # Check if all parents succeeded
    if all(status == 'succeeded' for status in parent_statuses.values()):
        # All dependencies completed successfully
        await process_normally()
    else:
        # Some parent jobs failed
        failed_jobs = [job_id for job_id, status in parent_statuses.items()
                       if status == 'failed']
        logger.warning(f"Parent jobs {failed_jobs} failed, handling gracefully")
        await handle_partial_failure()
```

## Key Behavior

- **Jobs with unfulfilled dependencies**: Will remain in the queue but won't be picked up by workers until all parent jobs reach a terminal status (succeeded, failed, cancelled, or aborted)
- **Running parent jobs**: Child jobs will NOT run while any parent job is still in 'todo' or 'doing' status
- **Failed parent jobs**: Child jobs WILL run even if parent jobs failed - the child job should check parent statuses and handle failures appropriately
- **Multiple workers**: Dependencies work correctly even with multiple workers running concurrently
- **Cascade on delete**: If a parent or child job is deleted, the dependency relationship is automatically cleaned up
