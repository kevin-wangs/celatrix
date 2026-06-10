"""Configuration management."""
import os, json, logging

logger = logging.getLogger("celatrix")

_DEFAULTS = {"default_devices": [0], "max_retries": 3, "log_level": "WARNING", "checkpoint_dir": ".celatrix/checkpoints"}

class Config:
    _instance = None
    def __init__(self):
        self._data = dict(_DEFAULTS)
        path = os.environ.get("CELATRIX_CONFIG")
        if path and os.path.exists(path):
            with open(path) as f: self._data.update(json.load(f))

    @classmethod
    def instance(cls):
        if cls._instance is None: cls._instance = cls()
        return cls._instance

    def get(self, key, default=None): return self._data.get(key, default)
    def set(self, key, value): self._data[key] = value
