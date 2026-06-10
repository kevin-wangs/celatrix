"""DAG engine for dependency resolution."""
from __future__ import annotations
from collections import defaultdict, deque
from typing import Dict, List
import logging
from celatrix.task import Task, TaskState

logger = logging.getLogger("celatrix")

class DAGCycleError(Exception): pass

class DAG:
    def __init__(self, tasks):
        self.tasks = {t.task_id: t for t in tasks}
        self._adj = defaultdict(list)
        self._in_degree = defaultdict(int)
        self._build()

    def _build(self):
        for task in self.tasks.values():
            if task.task_id not in self._in_degree: self._in_degree[task.task_id] = 0
            for dep in task.deps:
                self._adj[dep.task_id].append(task.task_id)
                self._in_degree[task.task_id] += 1

    def topological_sort(self):
        in_deg = dict(self._in_degree)
        queue = deque(tid for tid, d in in_deg.items() if d == 0)
        order = []
        while queue:
            tid = queue.popleft()
            order.append(tid)
            for n in self._adj[tid]:
                in_deg[n] -= 1
                if in_deg[n] == 0: queue.append(n)
        if len(order) != len(self.tasks): raise DAGCycleError("Cycle detected")
        return order

    def get_ready_tasks(self):
        return [t for t in self.tasks.values() if t.state == TaskState.PENDING and all(d.state == TaskState.COMPLETED for d in t.deps)]

    def get_critical_path(self):
        order = self.topological_sort()
        dist = {t: 0 for t in order}
        prev = {t: None for t in order}
        for tid in order:
            for n in self._adj[tid]:
                if dist[tid] + 1 > dist[n]: dist[n] = dist[tid] + 1; prev[n] = tid
        end = max(dist, key=dist.get)
        path, cur = [], end
        while cur: path.append(cur); cur = prev[cur]
        return list(reversed(path))

    def all_completed(self): return all(t.state == TaskState.COMPLETED for t in self.tasks.values())
    def has_failures(self): return any(t.state == TaskState.FAILED for t in self.tasks.values())
