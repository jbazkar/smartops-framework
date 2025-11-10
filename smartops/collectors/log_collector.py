from __future__ import annotations
from typing import Dict, Iterable
import random, time

def stream_logs(n: int = 50) -> Iterable[Dict]:
    severities = ["INFO", "WARN", "ERROR"]
    services = ["checkout", "payments", "auth", "catalog"]
    for _ in range(n):
        yield {
            "ts": time.time(),
            "severity": random.choices(severities, weights=[0.7,0.2,0.1])[0],
            "service": random.choice(services),
            "latency_ms": max(1, int(random.gauss(120, 50))),
            "status_code": random.choice([200,200,200,500,502,503]),
        }
