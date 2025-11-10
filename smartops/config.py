from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
import yaml

@dataclass
class AppConfig:
    project: str
    env: str
    detectors: Dict[str, Any]
    rules: Dict[str, Any]
    remediation: Dict[str, Any]

def load_config(path: str) -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return AppConfig(
        project=raw.get("project", "smartops-demo"),
        env=raw.get("env", "dev"),
        detectors=raw.get("detectors", {}),
        rules=raw.get("rules", {}),
        remediation=raw.get("remediation", {}),
    )
