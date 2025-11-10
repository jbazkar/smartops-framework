from __future__ import annotations
from typing import List
import random

class AutoencoderDetector:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def score(self, x: List[float]) -> float:
        recon_err = min(1.0, (x[6] / 20.0) + (0.3 if x[2] else 0.0))
        noise = random.uniform(-0.05, 0.05)
        return max(0.0, min(1.0, recon_err + noise))

    def is_anomaly(self, x: List[float]) -> bool:
        return self.score(x) >= self.threshold
