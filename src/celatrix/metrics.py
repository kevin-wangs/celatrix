"""Metrics collection for scheduler performance."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
from collections import defaultdict
import time, threading

@dataclass
class SchedulerMetrics:
    tasks_submitted: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_runtime_s: float = 0.0
    avg_task_latency_ms: float = 0.0

class MetricsCollector:
    def __init__(self):
        self._latencies: List[float] = []
        self._counters = defaultdict(int)
        self._lock = threading.Lock()

    def record_task(self, latency_ms):
        with self._lock:
            self._latencies.append(latency_ms)
            self._counters["tasks_completed"] += 1

    def increment(self, key):
        with self._lock: self._counters[key] += 1

    def summary(self):
        with self._lock:
            avg = sum(self._latencies) / len(self._latencies) if self._latencies else 0
            return SchedulerMetrics(
                tasks_submitted=self._counters.get("tasks_submitted", 0),
                tasks_completed=self._counters.get("tasks_completed", 0),
                tasks_failed=self._counters.get("tasks_failed", 0),
                avg_task_latency_ms=avg,
            )
