'''A cute little task runner.

Examples:
    >>> from tsk_monster import run, tsk
    >>> run(
    ...     tsk(
    ...         'wget -O img1.jpg https://picsum.photos/200/300',
    ...         prods=['img1.jpg']),
    ...
    ...     tsk(
    ...         'convert -resize 100x img1.jpg img1.small.jpg',
    ...         needs=['img1.jpg'],
    ...         prods=['img1.small.jpg']))
'''

import logging
import os
import queue
import threading
from collections import defaultdict
from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass
from functools import partial
from inspect import getmembers, isgeneratorfunction
from pathlib import Path
from typing import Any, Callable, Generator, List, Tuple, cast

import typer
from typing_extensions import Annotated

lg = logging.getLogger(__name__)


@dataclass
class need:
    val: Any


@dataclass
class prod:
    val: Any


@dataclass
class Cmd:
    description: str
    action: Callable[[], Any]

    @classmethod
    def from_str(cls, cmd: str):
        return cls(cmd, partial(os.system, cmd))

    def __repr__(self) -> str:
        return self.description


Job = Generator[need | prod | Cmd, None, None]


def run_jobs(*jobs: Job):
    '''Run jobs in parallel, respecting dependencies.

    Args:
        *jobs: A list of jobs to run.


    Examples:
        >>> from tsk_monster import run, tsk
        >>> run(
        ...     tsk(
        ...         'wget -O img1.jpg https://picsum.photos/200/300',
        ...         prods=['img1.jpg']),
        ...
        ...     tsk(
        ...         'convert -resize 100x img1.jpg img1.small.jpg',
        ...         needs=['img1.jpg'],
        ...         prods=['img1.small.jpg']))
    '''
    q = queue.Queue[Job]()
    needs = defaultdict(list)
    prods = set()

    def worker():
        def add2q(job: Job):
            def _(future: Future):
                future.result()
                q.put(job)
                q.task_done()

            return _

        with ProcessPoolExecutor() as executor:
            while True:
                job = q.get()

                try:
                    item = next(job)
                    lg.info(f'Running: {type(item)} {item}')

                    if isinstance(item, Cmd):
                        lg.info(f'Submitting: {item.description}')
                        future = executor.submit(item.action)
                        future.add_done_callback(add2q(job))

                    if isinstance(item, need):
                        lg.debug(f'{job} needs {item.val}')

                        if item.val in prods:
                            q.put(job)
                            q.task_done()
                        else:
                            needs[item.val].append(job)

                    if isinstance(item, prod):
                        lg.debug(f'{job} produced {item.val}')

                        prods.add(item.val)
                        q.put(job)
                        q.task_done()

                        jobs = needs.pop(item.val, [])

                        for job in jobs:
                            q.put(job)
                            q.task_done()

                except StopIteration:
                    lg.info(f'Done {job}')
                    q.task_done()

    threading.Thread(
        target=worker,
        daemon=True).start()

    for job in jobs:
        q.put(job)

    q.join()

    lg.info('All work completed')


Paths = List[Path | str] | List[Path]


def tsk(
        *cmds: Cmd | str,
        needs: Paths = [],
        prods: Paths = []) -> Job:
    '''Create a file based task.

    Examples:
        >>> tsk(
        ...     'wget -O img1.jpg https://picsum.photos/200/300',
        ...     prods=['img1.jpg'])

    Args:
        cmd: A command to run.
        needs: A list of files that are needed.
        prods: A list of files that will be produced.

    Returns:
        A job.
    '''

    def changed(path: Path):
        try:
            tsk = path.with_suffix('.tsk')
            if not tsk.exists():
                return True

            return tsk.stat().st_mtime < path.stat().st_mtime
        finally:
            tsk.touch()

    def to_paths(paths: Paths) -> List[Path]:
        return [Path(p) if isinstance(p, str) else p for p in paths]

    needs = to_paths(needs)
    prods = to_paths(prods)

    cmds = tuple([
        Cmd.from_str(cmd)
        if isinstance(cmd, str)
        else cmd
        for cmd in cmds])

    cmds = cast(Tuple[Cmd], cmds)

    always_run = len(needs) + len(prods) == 0

    def gen():
        for n in needs:
            yield need(n)

        if always_run or any(map(changed, needs)) or not all(map(Path.exists, prods)):
            yield from cmds

        else:
            for cmd in cmds:
                lg.info(f'SKIPPING: {cmd.description}')

        for m in prods:
            if m.exists():
                yield prod(m)
            else:
                raise Exception(f'{cmd} failed to produce {m}.')

    return gen()


def load_tasks():
    module = __import__('tskfile')
    return getmembers(module, isgeneratorfunction)


def task_names(prefix: str):
    return [name for name, _ in load_tasks() if name.startswith(prefix)]


app = typer.Typer()


@app.command()
def tsk_monster(target: Annotated[str, typer.Argument(autocompletion=task_names)]):
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%H:%M:%S',
        format='%(asctime)s - %(levelname)s - %(message)s')

    module = __import__('tskfile')
    members = getmembers(module, isgeneratorfunction)
    for name, value in members:
        if target == name:
            run_jobs(*value())


def main():
    app()
