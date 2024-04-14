from __future__ import annotations

import collections
import concurrent.futures
import pickle
from typing import Any, Callable, Generic, Iterable, Iterator

import dill  # type: ignore

from . import collectible
from .common import T, U


class ParallelMap(collectible.Collectible[U]):
    def __init__(self, f: Callable[[T], U], items: Iterable[T], max_tasks: int = 10):
        self.f = SerializableCallable(f)
        self.items = items
        self.max_tasks = max_tasks
        self.pool = concurrent.futures.ProcessPoolExecutor(max_workers=max_tasks)
        self.tasks: collections.deque = collections.deque()
        super().__init__(self._get_iterator())

    def _get_iterator(self) -> Iterator[U]:
        for i, item in enumerate(self.items):
            self.tasks.append(self.pool.submit(self.f, item))
            # until the queue fills up - submit 2 jobs and fetch 1
            if i % 2 == 1 or len(self.tasks) >= self.max_tasks and i % 2 == 0:
                task = self.tasks.popleft()
                yield task.result()

        for task in self.tasks:
            yield task.result()

        self.pool.shutdown()


#
# Serialization functions:
#
class SerializableCallable(Generic[T]):
    def __init__(self, f: Callable[[Any], T]):
        self.f = self._dumps_if_needed(f)

    def __call__(self, *args: Any) -> T:
        return self._loads_if_needed(self.f)(*args)

    @staticmethod
    def _dumps_if_needed(obj: Callable) -> Callable | bytes:
        try:
            pickle.dumps(obj)
            return obj
        except (AttributeError, pickle.PicklingError):
            return dill.dumps(obj)

    @staticmethod
    def _loads_if_needed(obj: Callable | bytes) -> Callable:
        if isinstance(obj, bytes):
            return dill.loads(obj)
        return obj
