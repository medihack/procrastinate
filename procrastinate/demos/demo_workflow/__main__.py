"""
Demo script showing how to use job dependencies to create workflows.

This example demonstrates:
1. Creating parent jobs
2. Creating child jobs that depend on parent jobs
3. How jobs wait for their dependencies to complete before running
"""

from __future__ import annotations

import asyncio
import logging

from . import app as app_module
from . import tasks

logger = logging.getLogger(__name__)


async def main():
    logging.info("Running workflow demo with job dependencies")

    async with app_module.app.open_async():
        # Create a data processing workflow
        # Step 1: Download data (no dependencies)
        download_job_id = await tasks.download_data.defer_async(
            source="api.example.com"
        )
        logger.info(f"Deferred download job: {download_job_id}")

        # Step 2: Process data (depends on download completing)
        # This job won't run until download_job completes successfully
        process_job_id = await tasks.process_data.configure(
            depends_on=[download_job_id]
        ).defer_async(filename="data.csv")
        logger.info(
            f"Deferred process job: {process_job_id} (depends on {download_job_id})"
        )

        # Step 3: Generate report (depends on processing completing)
        report_job_id = await tasks.generate_report.configure(
            depends_on=[process_job_id]
        ).defer_async(processed_file="processed_data.csv")
        logger.info(
            f"Deferred report job: {report_job_id} (depends on {process_job_id})"
        )

        print("\nWorkflow created!")
        print(f"Job execution order:")
        print(f"  1. Download data (job {download_job_id})")
        print(f"  2. Process data (job {process_job_id}) - waits for job {download_job_id}")
        print(f"  3. Generate report (job {report_job_id}) - waits for job {process_job_id}")
        print("\nStart a worker to see the jobs execute in order:")
        print("  python -m procrastinate worker")


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    asyncio.run(main())
