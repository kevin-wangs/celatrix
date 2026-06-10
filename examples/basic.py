#!/usr/bin/env python3
"""Basic Celatrix usage."""
from celatrix import Scheduler, Task

def preprocess(data=None, device_id=0): return [1, 2, 3]
def train(data=None, device_id=0): return {"loss": 0.01}
def evaluate(data=None, device_id=0): return {"accuracy": 0.99}

scheduler = Scheduler(devices=[0])
t1 = Task("preprocess", fn=preprocess)
t2 = Task("train", fn=train, deps=[t1])
t3 = Task("evaluate", fn=evaluate, deps=[t2])

scheduler.submit([t1, t2, t3])
results = scheduler.run()
print("Results:", results)
