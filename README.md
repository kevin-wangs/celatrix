# Celatrix

<div align="center">

**Task orchestration engine for multi-device compute environments**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)]()
[![ROCm](https://img.shields.io/badge/AMD%20ROCm-ready-orange.svg)]()

</div>

## Why Celatrix?

Modern GPU clusters need intelligent scheduling. Celatrix provides **DAG-based task orchestration**, **resource-aware placement**, and **fault tolerance** for heterogeneous AMD GPU environments.

| Feature | Celatrix | Ray | Dask |
|---------|----------|-----|------|
| DAG scheduling | Built-in | Plugin | Partial |
| GPU-aware placement | Yes | Limited | No |
| ROCm SMI integration | Native | No | No |
| Fault tolerance | Auto-retry | Yes | Yes |
| Critical path optimization | Yes | No | No |

## Architecture

```
+-----------------------------------------------+
|            Celatrix Scheduler                  |
+--------+--------+--------+--------------------+
|  DAG   |Resource| Policy |   Fault Tolerance  |
| Engine |Manager | Engine |   retry/failover   |
+--------+--------+--------+--------------------+
|         Device Pool (AMD GPUs)                |
|  Dev 0  |  Dev 1  |  Dev 2  |  ...           |
+---------+---------+---------+-----------------+
```

## Quick Start

```python
from celatrix import Scheduler, Task

scheduler = Scheduler(devices=[0, 1])

task_a = Task("preprocess", fn=preprocess, device_pref=0)
task_b = Task("train", fn=train, deps=[task_a], device_pref=1)
task_c = Task("evaluate", fn=evaluate, deps=[task_b])

scheduler.submit([task_a, task_b, task_c])
results = scheduler.run()
```

## Requirements
- Python 3.9+
- Optrix 0.1+
- AMD ROCm 6.0+ (optional)

## Installation
```bash
pip install celatrix
```

## License
MIT License
