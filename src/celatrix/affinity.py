"""Device affinity rules."""
from __future__ import annotations
from typing import Dict

class AffinityRule:
    HARD = "hard"
    SOFT = "soft"

class AffinityManager:
    def __init__(self):
        self._rules: Dict[str, dict] = {}

    def set(self, task_name, device_id, strength=AffinityRule.SOFT):
        self._rules[task_name] = {"device": device_id, "strength": strength}

    def get(self, task_name):
        return self._rules.get(task_name)

    def resolve(self, task_name, fallback_device):
        rule = self.get(task_name)
        if rule and rule["strength"] == AffinityRule.HARD:
            return rule["device"]
        return rule["device"] if rule else fallback_device
