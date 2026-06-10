"""Health check for scheduler and devices."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List
import time

@dataclass
class HealthStatus:
    component: str
    healthy: bool
    message: str
    checked_at: float = 0.0

class HealthChecker:
    def __init__(self, scheduler=None):
        self.scheduler = scheduler
        self._checks = []

    def check_devices(self):
        if not self.scheduler: return []
        results = []
        for did in self.scheduler.devices:
            res = self.scheduler.resources._pool.get(did)
            if res:
                healthy = res.temp_c < 90 and res.gpu_util_pct < 95
                results.append(HealthStatus(f"device_{did}", healthy, f"temp={res.temp_c:.0f}C util={res.gpu_util_pct:.0f}%", time.time()))
        return results

    def check_all(self):
        results = self.check_devices()
        self._checks = results
        return results

    def is_healthy(self):
        return all(r.healthy for r in self.check_all())
