"""
Example demonstrating workflow-style job dependencies in Procrastinate.

This example shows how to create a data processing pipeline where jobs
must execute in a specific order:
  1. Download data
  2. Process data (depends on download)
  3. Generate report (depends on process)
"""

from __future__ import annotations

import logging

from .app import app

logger = logging.getLogger(__name__)


@app.task(queue="download")
async def download_data(source: str):
    """Simulate downloading data from a source."""
    logger.info(f"Downloading data from {source}")
    # Simulate work
    return f"data_from_{source}.csv"


@app.task(queue="process")
async def process_data(filename: str):
    """Simulate processing downloaded data."""
    logger.info(f"Processing {filename}")
    # Simulate work
    return f"processed_{filename}"


@app.task(queue="report")
async def generate_report(processed_file: str):
    """Simulate generating a report from processed data."""
    logger.info(f"Generating report from {processed_file}")
    # Simulate work
    return f"report_for_{processed_file}.pdf"
