"""Scheduler integration tests."""
from celatrix import Scheduler, Task

def noop(**kw): return "ok"

class TestScheduler:
    def test_basic_schedule(self):
        s = Scheduler(devices=[0])
        a = Task("a", fn=noop)
        b = Task("b", fn=noop, deps=[a])
        s.submit([a, b])
        results = s.run()
        assert "a" in results and "b" in results
