from __future__ import annotations
from typing import List
import random

class OneClassSVMDetector:
    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold

    def score(self, x: List[float]) -> float:
        base = min(1.0, (x[3] + x[4]) / 200.0)
        noise = random.uniform(-0.05, 0.05)
        return max(0.0, min(1.0, base + noise))

    def is_anomaly(self, x: List[float]) -> bool:
        return self.score(x) >= self.threshold
