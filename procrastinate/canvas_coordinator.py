from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from procrastinate import types

if TYPE_CHECKING:
    from procrastinate import app, job_context, jobs

logger = logging.getLogger(__name__)


async def handle_canvas_completion(
    job: jobs.Job,
    job_result: job_context.JobResult,
    procrastinate_app: app.App,
) -> None:
    """
    Handle canvas workflow coordination after a job completes successfully.

    This function checks if the job is part of a canvas workflow (chain or chord)
    and performs the necessary coordination:
    - For chains: defer the next task with the result
    - For chords: update completion tracking and trigger callback if complete

    Parameters
    ----------
    job : Job
        The completed job
    job_result : JobResult
        The job result containing the return value
    procrastinate_app : App
        The Procrastinate app instance
    """
    task_kwargs = job.task_kwargs

    # Check for chain continuation
    if "_canvas_chain_next" in task_kwargs and "_canvas_chain_id" in task_kwargs:
        await _handle_chain_continuation(job, job_result, procrastinate_app)

    # Check for chord coordination
    if (
        "_canvas_chord_id" in task_kwargs
        and "_canvas_chord_size" in task_kwargs
        and "_canvas_chord_callback" in task_kwargs
    ):
        await _handle_chord_completion(job, job_result, procrastinate_app)


async def _handle_chain_continuation(
    job: jobs.Job,
    job_result: job_context.JobResult,
    procrastinate_app: app.App,
) -> None:
    """Handle continuation of a chain workflow."""
    task_kwargs = job.task_kwargs
    chain_next = task_kwargs.get("_canvas_chain_next", [])

    if not chain_next:
        # End of chain
        logger.debug(
            f"Chain {task_kwargs.get('_canvas_chain_id')} completed",
            extra={"chain_id": task_kwargs.get("_canvas_chain_id")},
        )
        return

    # Get the next task in the chain
    next_task_info = chain_next[0]
    remaining_chain = chain_next[1:]

    task_name = next_task_info["task_name"]
    next_kwargs = next_task_info["kwargs"].copy()
    next_options = next_task_info["options"]

    # Pass the result from the current task to the next task
    if job_result.result is not None:
        next_kwargs["_canvas_result"] = job_result.result

    # Propagate chain metadata
    next_kwargs["_canvas_chain_id"] = task_kwargs["_canvas_chain_id"]
    next_kwargs["_canvas_chain_next"] = remaining_chain

    # Defer the next task
    try:
        task = procrastinate_app.tasks[task_name]
        deferrer = task.configure(**next_options)
        job_id = await deferrer.defer_async(**next_kwargs)

        logger.info(
            f"Deferred next task in chain: {task_name} (job_id: {job_id})",
            extra={
                "chain_id": task_kwargs["_canvas_chain_id"],
                "next_task": task_name,
                "next_job_id": job_id,
            },
        )
    except Exception as e:
        logger.exception(
            f"Failed to defer next task in chain: {task_name}",
            extra={
                "chain_id": task_kwargs["_canvas_chain_id"],
                "error": str(e),
            },
        )
        raise


async def _handle_chord_completion(
    job: jobs.Job,
    job_result: job_context.JobResult,
    procrastinate_app: app.App,
) -> None:
    """Handle completion tracking for a chord workflow."""
    task_kwargs = job.task_kwargs
    chord_id = task_kwargs["_canvas_chord_id"]
    chord_size = task_kwargs["_canvas_chord_size"]
    callback_info = task_kwargs["_canvas_chord_callback"]

    connector = procrastinate_app.connector

    # Check if chord tracking record exists, create if not
    check_query = """
        SELECT completed_count FROM procrastinate_canvas_chords
        WHERE chord_id = %(chord_id)s
    """
    result = await connector.execute_query_one_async(
        check_query,
        chord_id=chord_id,
    )

    if result is None:
        # First task completing - initialize the chord tracking
        init_query = """
            INSERT INTO procrastinate_canvas_chords
            (chord_id, header_size, completed_count, results, callback_task_name,
             callback_kwargs, callback_options)
            VALUES (%(chord_id)s, %(header_size)s, 0, '[]'::jsonb,
                    %(callback_task_name)s, %(callback_kwargs)s::jsonb,
                    %(callback_options)s::jsonb)
            ON CONFLICT (chord_id) DO NOTHING
        """
        await connector.execute_query_async(
            init_query,
            chord_id=chord_id,
            header_size=chord_size,
            callback_task_name=callback_info["task_name"],
            callback_kwargs=json.dumps(callback_info["kwargs"]),
            callback_options=json.dumps(callback_info["options"]),
        )

    # Update the chord with this task's result
    update_query = """
        UPDATE procrastinate_canvas_chords
        SET completed_count = completed_count + 1,
            results = results || %(result)s::jsonb
        WHERE chord_id = %(chord_id)s
        RETURNING completed_count, header_size, callback_task_name,
                  callback_kwargs, callback_options, results
    """

    result_value = (
        job_result.result if job_result.result is not None else None
    )
    row = await connector.execute_query_one_async(
        update_query,
        chord_id=chord_id,
        result=json.dumps([result_value]),
    )

    if row is None:
        logger.error(
            f"Failed to update chord completion for {chord_id}",
            extra={"chord_id": chord_id},
        )
        return

    completed_count = row["completed_count"]
    header_size = row["header_size"]

    logger.debug(
        f"Chord {chord_id}: {completed_count}/{header_size} tasks completed",
        extra={
            "chord_id": chord_id,
            "completed": completed_count,
            "total": header_size,
        },
    )

    # Check if all header tasks are complete
    if completed_count >= header_size:
        # All tasks complete - defer the callback
        callback_task_name = row["callback_task_name"]
        callback_kwargs = row["callback_kwargs"]
        callback_options = row["callback_options"]
        all_results = row["results"]

        # Pass all results to the callback
        callback_kwargs["_canvas_result"] = all_results

        try:
            task = procrastinate_app.tasks[callback_task_name]
            deferrer = task.configure(**callback_options)
            callback_job_id = await deferrer.defer_async(**callback_kwargs)

            logger.info(
                f"Chord {chord_id} complete, deferred callback: {callback_task_name} (job_id: {callback_job_id})",
                extra={
                    "chord_id": chord_id,
                    "callback_task": callback_task_name,
                    "callback_job_id": callback_job_id,
                },
            )

            # Clean up the chord tracking record
            delete_query = """
                DELETE FROM procrastinate_canvas_chords
                WHERE chord_id = %(chord_id)s
            """
            await connector.execute_query_async(
                delete_query,
                chord_id=chord_id,
            )

        except Exception as e:
            logger.exception(
                f"Failed to defer chord callback: {callback_task_name}",
                extra={
                    "chord_id": chord_id,
                    "error": str(e),
                },
            )
            raise
