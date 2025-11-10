from __future__ import annotations
from typing import Dict

def run(action: str, params: Dict, dry_run: bool = True) -> Dict:
    if dry_run:
        return {"executed": False, "action": action, "params": params, "note": "dry-run only"}
    return {"executed": True, "action": action, "params": params, "note": "simulated execution"}
