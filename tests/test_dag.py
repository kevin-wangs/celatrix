"""DAG tests."""
import pytest
from celatrix.dag import DAG, DAGCycleError
from celatrix.task import Task

def noop(**kw): return "ok"

class TestDAG:
    def test_topological_order(self):
        a = Task("a", fn=noop); b = Task("b", fn=noop, deps=[a]); c = Task("c", fn=noop, deps=[b])
        dag = DAG([a, b, c])
        order = dag.topological_sort()
        assert order.index(a.task_id) < order.index(b.task_id)

    def test_ready(self):
        a = Task("a", fn=noop); b = Task("b", fn=noop, deps=[a])
        dag = DAG([a, b])
        assert len(dag.get_ready_tasks()) == 1

    def test_cycle(self):
        a = Task("a", fn=noop); b = Task("b", fn=noop, deps=[a]); a.deps = [b]
        with pytest.raises(DAGCycleError): DAG([a, b]).topological_sort()
