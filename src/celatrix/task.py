"""Task model with dependency tracking."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, List, Optional, Any
import time, uuid

class TaskState(Enum):
    PENDING = auto()
    QUEUED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

@dataclass
class ResourceRequest:
    min_vram_mb: int = 0
    min_compute_units: int = 1
    max_threads: int = 256
    priority: int = 0

@dataclass
class Task:
    name: str
    fn: Callable
    deps: List[Task] = field(default_factory=list)
    device_pref: Optional[int] = None
    resources: ResourceRequest = field(default_factory=ResourceRequest)
    state: TaskState = TaskState.PENDING
    result: Any = None
    error: Optional[Exception] = None
    task_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 2

    @property
    def duration(self):
        if self.started_at and self.finished_at: return self.finished_at - self.started_at
        return None

    @property
    def dep_ids(self): return [d.task_id for d in self.deps]

    def mark_running(self):
        self.state = TaskState.RUNNING
        self.started_at = time.time()

    def mark_completed(self, result):
        self.state = TaskState.COMPLETED
        self.result = result
        self.finished_at = time.time()

    def mark_failed(self, error):
        self.state = TaskState.FAILED
        self.error = error
        self.finished_at = time.time()

    def __repr__(self):
        return f"Task({self.name}, state={self.state.name}, deps={len(self.deps)})"
