from __future__ import annotations
from typing import Dict, Tuple, List

def make_features(log: Dict, metric: Dict) -> Tuple[List[float], Dict]:
    latency = float(log.get("latency_ms", 0))
    severity = 1.0 if log.get("severity") == "ERROR" else (0.5 if log.get("severity") == "WARN" else 0.0)
    status_err = 1.0 if int(log.get("status_code", 200)) >= 500 else 0.0
    cpu = float(metric.get("cpu_pct", 0))
    mem = float(metric.get("mem_pct", 0))
    qps = float(metric.get("qps", 0))
    epm = float(metric.get("errors_per_min", 0))
    vec = [latency, severity, status_err, cpu, mem, qps, epm]
    context = {"service": log.get("service"), "ts": log.get("ts")}
    return vec, context
