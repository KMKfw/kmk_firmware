'''
Here we're abusing _asyncios TaskQueue to implement a very simple priority
queue task scheduler.
Despite documentation, Circuitpython doesn't usually ship with a min-heap
module; it does however implement a pairing-heap for `TaskQueue` in native code.
'''

try:
    from typing import Callable
except ImportError:
    pass

from supervisor import ticks_ms

from _asyncio import Task, TaskQueue

from kmk.kmktime import ticks_add, ticks_diff

_task_queue = TaskQueue()


class PeriodicTaskMeta:
    def __init__(self, func: Callable[[None], None], period: int) -> None:
        self._task = Task(self.call)
        self._coro = func
        self.period = period

    def call(self) -> None:
        after_ms = ticks_add(self._task.ph_key, self.period)
        _task_queue.push_sorted(self._task, after_ms)
        self._coro()

    def restart(self) -> None:
        _task_queue.push_sorted(self._task)


def create_task(
    func: [Callable[[None], None], Task, PeriodicTaskMeta],
    *,
    after_ms: int = 0,
    period_ms: int = 0,
) -> [Task, PeriodicTaskMeta]:
    if isinstance(func, Task):
        t = r = func
    elif isinstance(func, PeriodicTaskMeta):
        r = func
        t = r._task
    elif period_ms:
        r = PeriodicTaskMeta(func, period_ms)
        t = r._task
    else:
        t = r = Task(func)

    if after_ms > 0:
        _task_queue.push_sorted(t, ticks_add(ticks_ms(), after_ms))
    elif after_ms == 0:
        _task_queue.push_head(t)

    return r


def get_due_task() -> [Callable, None]:
    now = ticks_ms()
    while True:
        t = _task_queue.peek()
        if not t or ticks_diff(t.ph_key, now) > 0:
            break
        _task_queue.pop_head()
        yield t.coro


def cancel_task(t: [Task, PeriodicTaskMeta]) -> None:
    if isinstance(t, PeriodicTaskMeta):
        t = t._task
    _task_queue.remove(t)
