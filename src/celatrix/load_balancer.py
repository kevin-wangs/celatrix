"""Load balancer for distributing work across devices."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List
import logging

logger = logging.getLogger("celatrix")

@dataclass
class LoadMetrics:
    device_id: int
    active_tasks: int = 0
    queue_depth: int = 0
    avg_latency_ms: float = 0.0

class LoadBalancer:
    def __init__(self, device_ids):
        self.metrics = {did: LoadMetrics(did) for did in device_ids}

    def update(self, device_id, active, queue, latency):
        m = self.metrics[device_id]
        m.active_tasks = active
        m.queue_depth = queue
        m.avg_latency_ms = latency

    def select(self) -> int:
        return min(self.metrics, key=lambda d: self.metrics[d].active_tasks + self.metrics[d].queue_depth * 0.5)

    def summary(self):
        lines = ["Load Balancer:"]
        for m in self.metrics.values():
            lines.append(f"  [{m.device_id}] active={m.active_tasks} queue={m.queue_depth} latency={m.avg_latency_ms:.1f}ms")
        return "\n".join(lines)
