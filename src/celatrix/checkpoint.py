"""Checkpoint: save and restore scheduler state."""
from __future__ import annotations
import pickle, logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("celatrix")

class CheckpointManager:
    def __init__(self, path=".celatrix/checkpoints"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def save(self, name, state):
        file = self.path / f"{name}.pkl"
        with open(file, "wb") as f:
            pickle.dump(state, f)
        logger.info("Checkpoint saved: %s", file)

    def load(self, name):
        file = self.path / f"{name}.pkl"
        with open(file, "rb") as f:
            return pickle.load(f)

    def list(self):
        return [f.stem for f in self.path.glob("*.pkl")]

    def delete(self, name):
        file = self.path / f"{name}.pkl"
        file.unlink(missing_ok=True)
