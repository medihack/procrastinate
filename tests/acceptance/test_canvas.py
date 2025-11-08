"""
Acceptance tests for canvas workflows (chain, group, chord).
"""

import asyncio

import pytest

from procrastinate import App, PsycopgConnector, chain, chord, group


@pytest.fixture
async def canvas_app(connection_params):
    """Create a test app with canvas tasks."""
    connector = PsycopgConnector(**connection_params)
    app = App(connector=connector)

    # Simple task that adds two numbers
    @app.task
    async def add(x, y):
        return x + y

    # Task that multiplies a number by 2
    @app.task
    async def double(x):
        return x * 2

    # Task that sums a list of numbers
    @app.task
    async def sum_all(numbers):
        return sum(numbers)

    # Task that receives the result from a previous task
    @app.task
    async def use_result(_canvas_result):
        return _canvas_result

    yield app

    await connector.close_async()


@pytest.mark.asyncio
async def test_signature_creation(canvas_app):
    """Test that signatures can be created from tasks."""
    add_task = canvas_app.tasks["add"]
    sig = add_task.s(x=1, y=2)

    assert sig.task == add_task
    assert sig.kwargs == {"x": 1, "y": 2}
    assert sig.options == {}


@pytest.mark.asyncio
async def test_signature_apply_async(canvas_app):
    """Test that signatures can be applied asynchronously."""
    add_task = canvas_app.tasks["add"]
    sig = add_task.s(x=5, y=3)

    job_id = await sig.apply_async()
    assert job_id > 0

    # Verify job was created
    job_row = await canvas_app.connector.execute_query_one_async(
        "SELECT * FROM procrastinate_jobs WHERE id = %(job_id)s",
        job_id=job_id,
    )
    assert job_row is not None
    assert job_row["task_name"] == "add"
    assert job_row["args"]["x"] == 5
    assert job_row["args"]["y"] == 3


@pytest.mark.asyncio
async def test_chain_creation(canvas_app):
    """Test that chains can be created using the pipe operator."""
    add_task = canvas_app.tasks["add"]
    double_task = canvas_app.tasks["double"]

    # Using pipe operator
    c = add_task.s(x=2, y=3) | double_task.s()

    assert len(c.signatures) == 2
    assert c.signatures[0].task == add_task
    assert c.signatures[1].task == double_task


@pytest.mark.asyncio
async def test_chain_using_function(canvas_app):
    """Test creating a chain using the chain() function."""
    add_task = canvas_app.tasks["add"]
    double_task = canvas_app.tasks["double"]

    c = chain(add_task.s(x=2, y=3), double_task.s())

    assert len(c.signatures) == 2


@pytest.mark.asyncio
async def test_chain_apply_async(canvas_app):
    """Test that chains can be applied."""
    add_task = canvas_app.tasks["add"]
    use_result_task = canvas_app.tasks["use_result"]

    c = chain(add_task.s(x=10, y=20), use_result_task.s())
    job_id = await c.apply_async()

    assert job_id > 0

    # Verify first job has chain metadata
    job_row = await canvas_app.connector.execute_query_one_async(
        "SELECT * FROM procrastinate_jobs WHERE id = %(job_id)s",
        job_id=job_id,
    )
    assert "_canvas_chain_id" in job_row["args"]
    assert "_canvas_chain_next" in job_row["args"]
    assert len(job_row["args"]["_canvas_chain_next"]) == 1


@pytest.mark.asyncio
async def test_group_creation(canvas_app):
    """Test that groups can be created."""
    add_task = canvas_app.tasks["add"]

    g = group(add_task.s(x=i, y=i) for i in range(5))

    assert len(g.signatures) == 5


@pytest.mark.asyncio
async def test_group_apply_async(canvas_app):
    """Test that groups can be applied."""
    add_task = canvas_app.tasks["add"]

    g = group(add_task.s(x=i, y=i) for i in range(3))
    job_ids = await g.apply_async()

    assert len(job_ids) == 3
    assert all(job_id > 0 for job_id in job_ids)


@pytest.mark.asyncio
async def test_chord_creation(canvas_app):
    """Test that chords can be created."""
    add_task = canvas_app.tasks["add"]
    sum_all_task = canvas_app.tasks["sum_all"]

    c = chord(group(add_task.s(x=i, y=i) for i in range(5)), sum_all_task.s())

    assert len(c.header.signatures) == 5
    assert c.body.task == sum_all_task


@pytest.mark.asyncio
async def test_chord_apply_async(canvas_app):
    """Test that chords can be applied."""
    add_task = canvas_app.tasks["add"]
    sum_all_task = canvas_app.tasks["sum_all"]

    c = chord(group(add_task.s(x=i, y=i) for i in range(3)), sum_all_task.s())
    job_id = await c.apply_async()

    assert job_id > 0

    # Verify first job has chord metadata
    job_row = await canvas_app.connector.execute_query_one_async(
        "SELECT * FROM procrastinate_jobs WHERE id = %(job_id)s",
        job_id=job_id,
    )
    assert "_canvas_chord_id" in job_row["args"]
    assert "_canvas_chord_size" in job_row["args"]
    assert "_canvas_chord_callback" in job_row["args"]


@pytest.mark.asyncio
async def test_chain_with_list_syntax(canvas_app):
    """Test creating chain with list."""
    add_task = canvas_app.tasks["add"]
    double_task = canvas_app.tasks["double"]

    sigs = [add_task.s(x=1, y=2), double_task.s()]
    c = chain(*sigs)

    assert len(c.signatures) == 2


@pytest.mark.asyncio
async def test_group_with_list_syntax(canvas_app):
    """Test creating group with list."""
    add_task = canvas_app.tasks["add"]

    sigs = [add_task.s(x=1, y=1), add_task.s(x=2, y=2), add_task.s(x=3, y=3)]
    g = group(*sigs)

    assert len(g.signatures) == 3
