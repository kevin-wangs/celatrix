"""Live task migration between devices."""
from __future__ import annotations
import logging
from celatrix.task import Task

logger = logging.getLogger("celatrix")

class MigrationManager:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def migrate(self, task, target_device):
        old_device = task.device_pref
        task.device_pref = target_device
        logger.info("Migrated %s: device %d -> %d", task.task_id, old_device, target_device)

    def auto_migrate(self):
        migrated = 0
        for task in self.scheduler._tasks:
            if task.state == TaskState.RUNNING:
                best = self.scheduler.resources.best_device()
                if best != task.device_pref:
                    self.migrate(task, best)
                    migrated += 1
        return migrated
