from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Iterable

import attr

from procrastinate import types

if TYPE_CHECKING:
    from procrastinate import tasks


@attr.dataclass(frozen=True)
class Signature:
    """
    A signature wraps the arguments and execution options of a single task call.

    Signatures can be used to pass tasks around as first-class objects and to
    compose complex workflows using chains, groups, and chords.

    Attributes
    ----------
    task : Task
        The task to execute
    kwargs : dict
        Keyword arguments to pass to the task
    options : dict
        Configuration options (queue, priority, lock, etc.)
    """

    task: tasks.Task
    kwargs: types.JSONDict = attr.ib(factory=dict)
    options: types.JSONDict = attr.ib(factory=dict)

    def __or__(self, other: Signature | Chain) -> Chain:
        """
        Create a chain by piping signatures together using the | operator.

        Examples
        --------
        >>> task1.s(x=1) | task2.s() | task3.s()
        """
        if isinstance(other, Chain):
            return Chain([self] + list(other.signatures))
        return Chain([self, other])

    async def apply_async(
        self, args: tuple[Any, ...] | None = None, kwargs: dict[str, Any] | None = None
    ) -> int:
        """
        Execute the signature asynchronously.

        Parameters
        ----------
        args : tuple, optional
            Positional arguments to add (these will be passed to the task)
        kwargs : dict, optional
            Keyword arguments to add or override

        Returns
        -------
        int
            The job ID
        """
        final_kwargs = self.kwargs.copy()
        if kwargs:
            final_kwargs.update(kwargs)

        # Handle args from previous task in chain
        if args:
            # If the task receives a single result from previous task,
            # store it in a special key
            if len(args) == 1:
                final_kwargs["_canvas_result"] = args[0]
            else:
                final_kwargs["_canvas_result"] = args

        deferrer = self.task.configure(**self.options)
        return await deferrer.defer_async(**final_kwargs)

    def apply(
        self, args: tuple[Any, ...] | None = None, kwargs: dict[str, Any] | None = None
    ) -> int:
        """
        Execute the signature synchronously.

        Parameters
        ----------
        args : tuple, optional
            Positional arguments to add
        kwargs : dict, optional
            Keyword arguments to add or override

        Returns
        -------
        int
            The job ID
        """
        final_kwargs = self.kwargs.copy()
        if kwargs:
            final_kwargs.update(kwargs)

        # Handle args from previous task in chain
        if args:
            if len(args) == 1:
                final_kwargs["_canvas_result"] = args[0]
            else:
                final_kwargs["_canvas_result"] = args

        deferrer = self.task.configure(**self.options)
        return deferrer.defer(**final_kwargs)


@attr.dataclass(frozen=True)
class Chain:
    """
    A chain executes tasks sequentially, passing the result of each task
    to the next one.

    Examples
    --------
    >>> from procrastinate import chain
    >>> result = await chain(add.s(2, 2), add.s(4), mul.s(2)).apply_async()
    # Executes: mul(add(add(2, 2), 4), 2) = mul(add(4, 4), 2) = mul(8, 2) = 16

    Attributes
    ----------
    signatures : list
        List of signatures to execute in order
    """

    signatures: list[Signature]

    def __or__(self, other: Signature | Chain) -> Chain:
        """Chain another signature or chain to this chain."""
        if isinstance(other, Chain):
            return Chain(list(self.signatures) + list(other.signatures))
        return Chain(list(self.signatures) + [other])

    async def apply_async(self, **kwargs: Any) -> int:
        """
        Execute the chain asynchronously.

        The first task is deferred immediately. Each task in the chain will
        defer the next task upon completion, passing its result forward.

        Returns
        -------
        int
            The job ID of the first task in the chain
        """
        if not self.signatures:
            raise ValueError("Cannot apply empty chain")

        # Prepare chain metadata for the first task
        first_sig = self.signatures[0]
        chain_id = str(uuid.uuid4())

        # Store the chain continuation in the first task's kwargs
        first_kwargs = first_sig.kwargs.copy()
        first_kwargs["_canvas_chain_id"] = chain_id
        first_kwargs["_canvas_chain_next"] = [
            {
                "task_name": sig.task.name,
                "kwargs": sig.kwargs,
                "options": sig.options,
            }
            for sig in self.signatures[1:]
        ]
        first_kwargs.update(kwargs)

        # Defer the first task
        deferrer = first_sig.task.configure(**first_sig.options)
        return await deferrer.defer_async(**first_kwargs)

    def apply(self, **kwargs: Any) -> int:
        """
        Execute the chain synchronously.

        Returns
        -------
        int
            The job ID of the first task in the chain
        """
        if not self.signatures:
            raise ValueError("Cannot apply empty chain")

        first_sig = self.signatures[0]
        chain_id = str(uuid.uuid4())

        first_kwargs = first_sig.kwargs.copy()
        first_kwargs["_canvas_chain_id"] = chain_id
        first_kwargs["_canvas_chain_next"] = [
            {
                "task_name": sig.task.name,
                "kwargs": sig.kwargs,
                "options": sig.options,
            }
            for sig in self.signatures[1:]
        ]
        first_kwargs.update(kwargs)

        deferrer = first_sig.task.configure(**first_sig.options)
        return deferrer.defer(**first_kwargs)


@attr.dataclass(frozen=True)
class Group:
    """
    A group executes tasks in parallel.

    Examples
    --------
    >>> from procrastinate import group
    >>> result = await group(add.s(i, i) for i in range(10)).apply_async()
    # Executes all tasks in parallel

    Attributes
    ----------
    signatures : list
        List of signatures to execute in parallel
    """

    signatures: list[Signature]

    async def apply_async(self, **kwargs: Any) -> list[int]:
        """
        Execute all tasks in the group in parallel.

        Returns
        -------
        list[int]
            List of job IDs for all tasks in the group
        """
        job_ids = []
        for sig in self.signatures:
            final_kwargs = sig.kwargs.copy()
            final_kwargs.update(kwargs)
            deferrer = sig.task.configure(**sig.options)
            job_id = await deferrer.defer_async(**final_kwargs)
            job_ids.append(job_id)
        return job_ids

    def apply(self, **kwargs: Any) -> list[int]:
        """
        Execute all tasks in the group in parallel (sync version).

        Returns
        -------
        list[int]
            List of job IDs for all tasks in the group
        """
        job_ids = []
        for sig in self.signatures:
            final_kwargs = sig.kwargs.copy()
            final_kwargs.update(kwargs)
            deferrer = sig.task.configure(**sig.options)
            job_id = deferrer.defer(**final_kwargs)
            job_ids.append(job_id)
        return job_ids


@attr.dataclass(frozen=True)
class Chord:
    """
    A chord executes a group of tasks in parallel, then executes a callback
    with all the results.

    Examples
    --------
    >>> from procrastinate import chord
    >>> result = await chord(
    ...     group(add.s(i, i) for i in range(10)),
    ...     tsum.s()
    ... ).apply_async()
    # Executes all add tasks in parallel, then calls tsum with all results

    Attributes
    ----------
    header : Group
        The group of tasks to execute in parallel
    body : Signature
        The callback task to execute with all results
    """

    header: Group
    body: Signature

    async def apply_async(self, **kwargs: Any) -> int:
        """
        Execute the chord asynchronously.

        All header tasks are deferred immediately with chord coordination metadata.
        When all header tasks complete, the body task will be automatically deferred
        with all the results.

        Returns
        -------
        int
            The job ID of the chord coordinator task
        """
        from procrastinate import builtin_tasks

        chord_id = str(uuid.uuid4())
        header_count = len(self.header.signatures)

        # Defer all header tasks with chord metadata
        header_job_ids = []
        for sig in self.header.signatures:
            final_kwargs = sig.kwargs.copy()
            final_kwargs["_canvas_chord_id"] = chord_id
            final_kwargs["_canvas_chord_size"] = header_count
            final_kwargs["_canvas_chord_callback"] = {
                "task_name": self.body.task.name,
                "kwargs": self.body.kwargs,
                "options": self.body.options,
            }
            final_kwargs.update(kwargs)

            deferrer = sig.task.configure(**sig.options)
            job_id = await deferrer.defer_async(**final_kwargs)
            header_job_ids.append(job_id)

        # The chord coordination is handled by a hook in the task execution
        # We return the first header job ID as a reference
        return header_job_ids[0] if header_job_ids else 0

    def apply(self, **kwargs: Any) -> int:
        """
        Execute the chord synchronously.

        Returns
        -------
        int
            The job ID of the first header task
        """
        chord_id = str(uuid.uuid4())
        header_count = len(self.header.signatures)

        header_job_ids = []
        for sig in self.header.signatures:
            final_kwargs = sig.kwargs.copy()
            final_kwargs["_canvas_chord_id"] = chord_id
            final_kwargs["_canvas_chord_size"] = header_count
            final_kwargs["_canvas_chord_callback"] = {
                "task_name": self.body.task.name,
                "kwargs": self.body.kwargs,
                "options": self.body.options,
            }
            final_kwargs.update(kwargs)

            deferrer = sig.task.configure(**sig.options)
            job_id = deferrer.defer(**final_kwargs)
            header_job_ids.append(job_id)

        return header_job_ids[0] if header_job_ids else 0


def chain(*signatures: Signature | Chain) -> Chain:
    """
    Create a chain of tasks that execute sequentially.

    Each task receives the result of the previous task as input.

    Parameters
    ----------
    *signatures : Signature or Chain
        Tasks to execute in sequence

    Returns
    -------
    Chain
        A chain object that can be executed with apply() or apply_async()

    Examples
    --------
    >>> from procrastinate import chain
    >>> c = chain(add.s(2, 2), add.s(4), mul.s(2))
    >>> await c.apply_async()
    """
    all_sigs: list[Signature] = []
    for sig in signatures:
        if isinstance(sig, Chain):
            all_sigs.extend(sig.signatures)
        else:
            all_sigs.append(sig)
    return Chain(all_sigs)


def group(*signatures: Signature | Iterable[Signature]) -> Group:
    """
    Create a group of tasks that execute in parallel.

    Parameters
    ----------
    *signatures : Signature or iterable of Signature
        Tasks to execute in parallel

    Returns
    -------
    Group
        A group object that can be executed with apply() or apply_async()

    Examples
    --------
    >>> from procrastinate import group
    >>> g = group(add.s(i, i) for i in range(10))
    >>> await g.apply_async()

    >>> # Or with multiple arguments
    >>> g = group(add.s(1, 1), add.s(2, 2), add.s(3, 3))
    >>> await g.apply_async()
    """
    all_sigs: list[Signature] = []
    for sig in signatures:
        if isinstance(sig, Signature):
            all_sigs.append(sig)
        else:
            # It's an iterable
            all_sigs.extend(sig)
    return Group(all_sigs)


def chord(header: Group | Iterable[Signature], body: Signature) -> Chord:
    """
    Create a chord that executes a group of tasks in parallel, then executes
    a callback with all the results.

    Parameters
    ----------
    header : Group or iterable of Signature
        Tasks to execute in parallel
    body : Signature
        Callback task that receives all results

    Returns
    -------
    Chord
        A chord object that can be executed with apply() or apply_async()

    Examples
    --------
    >>> from procrastinate import chord, group
    >>> c = chord(group(add.s(i, i) for i in range(10)), tsum.s())
    >>> await c.apply_async()

    >>> # Or with a list
    >>> c = chord([add.s(1, 1), add.s(2, 2)], tsum.s())
    >>> await c.apply_async()
    """
    if isinstance(header, Group):
        return Chord(header=header, body=body)
    else:
        return Chord(header=group(header), body=body)
