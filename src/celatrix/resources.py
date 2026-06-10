"""Resource manager with ROCm SMI integration."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import logging, subprocess, json

logger = logging.getLogger("celatrix")

@dataclass
class DeviceResources:
    device_id: int
    name: str = ""
    total_vram_mb: int = 0
    used_vram_mb: int = 0
    compute_units: int = 0
    gpu_util_pct: float = 0.0
    temp_c: float = 0.0
    power_w: float = 0.0

    @property
    def free_vram_mb(self): return self.total_vram_mb - self.used_vram_mb
    @property
    def is_available(self): return self.gpu_util_pct < 90 and self.temp_c < 85

class ResourceManager:
    def __init__(self, device_ids):
        self.device_ids = device_ids
        self._pool: Dict[int, DeviceResources] = {}
        self._refresh()

    def _refresh(self):
        for did in self.device_ids:
            try: self._pool[did] = DeviceResources(device_id=did, **self._query_smi(did))
            except: self._pool[did] = DeviceResources(device_id=did, name=f"GPU {did}", total_vram_mb=16384, compute_units=96)

    def _query_smi(self, did):
        try:
            r = subprocess.run(["rocm-smi", "--json"], capture_output=True, text=True, timeout=5)
            d = json.loads(r.stdout).get(str(did), {})
            return {"name": d.get("Card series", ""), "gpu_util_pct": float(d.get("GPU use (%)", 0)), "temp_c": float(d.get("Temperature (Sensor edge) (C)", 0))}
        except: return {}

    def best_device(self, vram_needed=0):
        candidates = [d for d in self._pool.values() if d.free_vram_mb >= vram_needed and d.is_available]
        if not candidates: candidates = list(self._pool.values())
        return min(candidates, key=lambda d: d.gpu_util_pct).device_id

    def summary(self):
        lines = ["Device Pool:"]
        for d in self._pool.values():
            lines.append(f"  [{d.device_id}] {d.name}: GPU {d.gpu_util_pct:.0f}% | {d.used_vram_mb}/{d.total_vram_mb}MB | {d.temp_c:.0f}C")
        return "\n".join(lines)
