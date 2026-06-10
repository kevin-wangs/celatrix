"""Task placement policies."""
from __future__ import annotations
from typing import List
from celatrix.task import Task
from celatrix.resources import ResourceManager

class PlacementPolicy:
    def select_device(self, task, resources): ...

class RoundRobin(PlacementPolicy):
    def __init__(self): self._idx = 0
    def select_device(self, task, resources):
        devices = resources.device_ids
        dev = devices[self._idx % len(devices)]
        self._idx += 1
        return dev

class LeastLoaded(PlacementPolicy):
    def select_device(self, task, resources):
        return resources.best_device(task.resources.min_vram_mb)

class AffinityPolicy(PlacementPolicy):
    def __init__(self, affinity_map): self.map = affinity_map
    def select_device(self, task, resources):
        return self.map.get(task.name, LeastLoaded().select_device(task, resources))
