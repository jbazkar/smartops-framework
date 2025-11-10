from __future__ import annotations
from typing import Dict

def decide(scores: Dict[str, float], policy: Dict) -> Dict:
    min_votes = int(policy.get("min_votes", 2))
    min_score = float(policy.get("min_score", 0.75))
    blocked = set(policy.get("blocked_services", []))
    service = policy.get("service", "unknown")

    votes = sum(1 for _, s in scores.items() if s >= min_score)
    if service in blocked:
        return {"permit": False, "reason": f"Service '{service}' is blocked by policy"}
    if votes >= min_votes:
        return {"permit": True, "reason": f"{votes} detectors >= {min_score}"}
    return {"permit": False, "reason": f"Only {votes} detectors cleared threshold"}
