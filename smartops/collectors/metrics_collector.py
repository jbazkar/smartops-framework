from __future__ import annotations
from typing import Dict, Iterable
import random, time

def stream_metrics(n: int = 50) -> Iterable[Dict]:
    for _ in range(n):
        yield {
            "ts": time.time(),
            "cpu_pct": max(0.0, min(100.0, random.gauss(45, 15))),
            "mem_pct": max(0.0, min(100.0, random.gauss(55, 10))),
            "qps": max(0.0, random.gauss(1200, 300)),
            "errors_per_min": max(0.0, random.gauss(5, 2)),
        }
