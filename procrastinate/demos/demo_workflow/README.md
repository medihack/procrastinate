# Workflow Demo - Job Dependencies

This demo shows how to use job dependencies in Procrastinate to create workflows where jobs must execute in a specific order.

## What are Job Dependencies?

Job dependencies allow you to specify that a job should only run after one or more parent jobs have completed successfully. This is useful for:

- Data processing pipelines
- Multi-step workflows
- Tasks that depend on the output of previous tasks
- Orchestrating complex job sequences

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

## Key Behavior

- **Jobs with unfulfilled dependencies**: Will remain in the queue but won't be picked up by workers
- **Failed parent jobs**: If a parent job fails, child jobs will never run
- **Multiple workers**: Dependencies work correctly even with multiple workers running concurrently
- **Cascade on delete**: If a parent or child job is deleted, the dependency relationship is automatically cleaned up
