"""Task serialization for distributed scheduling."""
from __future__ import annotations
import pickle, json
from celatrix.task import Task

def serialize_task(task):
    return {"task_id": task.task_id, "name": task.name, "state": task.state.name, "dep_ids": task.dep_ids}

def serialize_dag(tasks):
    return [serialize_task(t) for t in tasks]

def to_json(tasks):
    return json.dumps(serialize_dag(tasks), indent=2)
