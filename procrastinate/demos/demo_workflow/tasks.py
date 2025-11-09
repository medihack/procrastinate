"""
Example demonstrating workflow-style job dependencies in Procrastinate.

This example shows how to create a data processing pipeline where jobs
must execute in a specific order:
  1. Download data
  2. Process data (depends on download) - checks if download succeeded
  3. Generate report (depends on process)
"""

from __future__ import annotations

import logging

from procrastinate import job_context

from .app import app

logger = logging.getLogger(__name__)


@app.task(queue="download")
async def download_data(source: str):
    """Simulate downloading data from a source."""
    logger.info(f"Downloading data from {source}")
    # Simulate work
    return f"data_from_{source}.csv"


@app.task(queue="process", pass_context=True)
async def process_data(context: job_context.JobContext, filename: str):
    """
    Simulate processing downloaded data.

    This task demonstrates how to check parent job statuses.
    """
    # Get the status of parent jobs
    parent_statuses = await context.get_parent_statuses_async()

    logger.info(f"Parent job statuses: {parent_statuses}")

    # Check if all parent jobs succeeded
    if all(status == "succeeded" for status in parent_statuses.values()):
        logger.info(f"All parent jobs succeeded. Processing {filename}")
        # Simulate work
        return f"processed_{filename}"
    else:
        # Handle case where parent jobs failed
        failed = [
            job_id
            for job_id, status in parent_statuses.items()
            if status != "succeeded"
        ]
        logger.error(
            f"Cannot process data: parent jobs {failed} did not succeed. Skipping processing."
        )
        raise Exception(f"Parent jobs {failed} failed")


@app.task(queue="report")
async def generate_report(processed_file: str):
    """Simulate generating a report from processed data."""
    logger.info(f"Generating report from {processed_file}")
    # Simulate work
    return f"report_for_{processed_file}.pdf"
