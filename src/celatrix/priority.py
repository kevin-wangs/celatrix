"""Priority queue for task scheduling."""
from __future__ import annotations
import heapq
from typing import List
from celatrix.task import Task

class PriorityQueue:
    def __init__(self):
        self._heap: List[tuple] = []
        self._counter = 0

    def push(self, task: Task):
        heapq.heappush(self._heap, (-task.resources.priority, self._counter, task))
        self._counter += 1

    def pop(self) -> Task:
        _, _, task = heapq.heappop(self._heap)
        return task

    def peek(self) -> Task:
        return self._heap[0][2]

    def __len__(self): return len(self._heap)
    def __bool__(self): return bool(self._heap)
