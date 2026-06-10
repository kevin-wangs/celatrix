"""Fault tolerance: retry logic and device failover."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Callable
import logging, time

logger = logging.getLogger("celatrix")

@dataclass
class RetryPolicy:
    max_retries: int = 3
    backoff_base: float = 1.0
    backoff_max: float = 30.0

    def get_delay(self, attempt):
        return min(self.backoff_base * (2 ** attempt), self.backoff_max)

class FaultManager:
    def __init__(self, policy=None):
        self.policy = policy or RetryPolicy()
        self._failures = {}

    def record_failure(self, task_id, error):
        self._failures.setdefault(task_id, []).append(error)
        count = len(self._failures[task_id])
        logger.warning("Task %s failed (attempt %d): %s", task_id, count, error)
        return count <= self.policy.max_retries

    def should_retry(self, task_id):
        return len(self._failures.get(task_id, [])) < self.policy.max_retries

    def get_backoff(self, task_id):
        attempt = len(self._failures.get(task_id, []))
        return self.policy.get_delay(attempt)
