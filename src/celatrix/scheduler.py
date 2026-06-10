"""Main scheduler: parallel execution with retry."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any
import logging, time
from celatrix.task import Task, TaskState
from celatrix.dag import DAG
from celatrix.resources import ResourceManager

logger = logging.getLogger("celatrix")

class Scheduler:
    def __init__(self, devices, max_workers=None):
        self.devices = devices
        self.max_workers = max_workers or len(devices)
        self.resources = ResourceManager(devices)
        self._tasks: List[Task] = []
        self._results: Dict[str, Any] = {}

    def submit(self, tasks): self._tasks.extend(tasks)

    def run(self):
        dag = DAG(self._tasks)
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {}
            while not dag.all_completed() and not dag.has_failures():
                for task in dag.get_ready_tasks():
                    if task.task_id in futures: continue
                    device = task.device_pref if task.device_pref is not None else self.resources.best_device()
                    task.mark_running()
                    futures[task.task_id] = pool.submit(self._exec, task, device)
                for tid, f in list(futures.items()):
                    if f.done():
                        task = self._tasks_by_id()[tid]
                        try: task.mark_completed(f.result()); self._results[task.name] = task.result
                        except Exception as e:
                            if task.retry_count < task.max_retries: task.retry_count += 1; task.state = TaskState.PENDING; del futures[tid]
                            else: task.mark_failed(e)
                time.sleep(0.01)
        return self._results

    def _exec(self, task, device_id):
        return task.fn(**{d.name: d.result for d in task.deps}, device_id=device_id)

    def _tasks_by_id(self): return {t.task_id: t for t in self._tasks}
