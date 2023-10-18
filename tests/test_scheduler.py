import time
import unittest

from kmk import scheduler


class TestScheduler(unittest.TestCase):
    def _task(self):
        self._t_count += 1

    def _task_loop(self, duration):
        until = time.time_ns() + 1_000_000 * duration
        while time.time_ns() < until:
            for t in scheduler.get_due_task():
                t()

    def setUp(self):
        self._t_count = 0
        scheduler._task_queue = scheduler.TaskQueue()

    def test_cancel_task(self):
        t = scheduler.create_task(self._task, after_ms=1)
        scheduler.cancel_task(t)
        self._task_loop(2)
        self.assertEqual(self._t_count, 0)

    def test_create_task(self):
        scheduler.create_task(self._task)
        self._task_loop(1)
        self.assertEqual(self._t_count, 1)

    def test_create_task_after_ms_after(self):
        scheduler.create_task(self._task, after_ms=2)
        self._task_loop(1)
        self.assertEqual(self._t_count, 0)

    def test_create_task_after_ms_within(self):
        scheduler.create_task(self._task, after_ms=1)
        self._task_loop(2)
        self.assertEqual(self._t_count, 1)

    def test_create_task_from_PeriodicTaskMeta(self):
        t = scheduler.create_task(self._task, period_ms=1)
        scheduler.cancel_task(t)
        self.assertEqual(self._t_count, 0)

        t = scheduler.create_task(t)
        self.assertIsInstance(t, scheduler.PeriodicTaskMeta)
        self._task_loop(2)
        self.assertEqual(self._t_count, 3)

    def test_create_task_from_Task(self):
        t = scheduler.create_task(self._task)
        scheduler.cancel_task(t)
        self.assertEqual(self._t_count, 0)

        t = scheduler.create_task(t)
        self.assertIsInstance(t, scheduler.Task)
        self._task_loop(1)
        self.assertEqual(self._t_count, 1)

    def test_create_task_period_ms(self):
        scheduler.create_task(self._task, period_ms=2)
        self._task_loop(1)
        self.assertEqual(self._t_count, 1)
        for i in range(2, 4):
            self._task_loop(1)
            self.assertEqual(self._t_count, i)
            self._task_loop(1)
            self.assertEqual(self._t_count, i)

    def test_restart_PeriodicTaskMeta(self):
        t = scheduler.create_task(self._task, period_ms=1)
        scheduler.cancel_task(t)
        self.assertEqual(self._t_count, 0)

        t.restart()
        self._task_loop(2)
        self.assertEqual(self._t_count, 3)

    def test_create_task_PeriodicTaskMeta(self):
        t = scheduler.create_task(self._task, period_ms=1)
        self.assertIsInstance(t, scheduler.PeriodicTaskMeta)

    def test_create_task_Task(self):
        t = scheduler.create_task(self._task)
        self.assertIsInstance(t, scheduler.Task)


if __name__ == '__main__':
    unittest.main()
