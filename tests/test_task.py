"""Task model tests."""
import pytest
from celatrix.task import Task, TaskState

def noop(**kw): return "ok"

class TestTask:
    def test_lifecycle(self):
        t = Task("test", fn=noop)
        assert t.state == TaskState.PENDING
        t.mark_running(); assert t.state == TaskState.RUNNING
        t.mark_completed("r"); assert t.state == TaskState.COMPLETED
        assert t.duration is not None

    def test_deps(self):
        a = Task("a", fn=noop)
        b = Task("b", fn=noop, deps=[a])
        assert b.dep_ids == [a.task_id]

    def test_failure(self):
        t = Task("f", fn=noop)
        t.mark_failed(ValueError("x"))
        assert t.state == TaskState.FAILED
