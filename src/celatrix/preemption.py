"""Task preemption for high-priority work."""
from __future__ import annotations
import logging
from celatrix.task import Task, TaskState

logger = logging.getLogger("celatrix")

class PreemptionManager:
    def __init__(self):
        self._preempted = {}

    def preempt(self, task):
        if task.state == TaskState.RUNNING:
            task.state = TaskState.QUEUED
            self._preempted[task.task_id] = task
            logger.info("Preempted task %s", task.task_id)
            return True
        return False

    def restore(self, task_id):
        task = self._preempted.pop(task_id, None)
        if task:
            task.state = TaskState.PENDING
            return task
        return None
