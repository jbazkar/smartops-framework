from __future__ import annotations
from typing import List

def fuse_scores(scores: List[float]) -> float:
    if not scores:
        return 0.0
    return sum(scores) / float(len(scores))
