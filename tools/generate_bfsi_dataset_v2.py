# tools/generate_bfsi_dataset_v2.py
"""
Generate a new BFSI dataset side-by-side (results_banking_v2/),
without touching the original results_banking/ files.

- Writes:
    results_banking_v2/banking_telemetry.csv
    results_banking_v2/banking_model_scores.csv
- Schema matches v1 so all existing charts/scripts can be reused by changing the folder.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

out = Path("results_banking_v2")
out.mkdir(parents=True, exist_ok=True)

telemetry_path = out / "banking_telemetry.csv"
scores_path = out / "banking_model_scores.csv"

# Try to reuse service names from v1 if present; else use defaults
services = ["credit-card-auth", "payments-gateway", "fraud-detection", "loan-eligibility", "account-summary"]
try:
    v1 = Path("results_banking/banking_telemetry.csv")
    if v1.exists():
        sv = pd.read_csv(v1, usecols=["service"]).service.unique().tolist()
        if sv:
            services = sv
except Exception:
    pass

# Config: 6 hours of data, 1-min granularity
start = datetime.utcnow().replace(second=0, microsecond=0)
periods = 6 * 60  # 6 hours
idx = [start + timedelta(minutes=i) for i in range(periods)]
rng = np.random.default_rng(2025)

tele_rows, score_rows = [], []

for ts in idx:
    for svc in services:
        # baseline per-service so curves differ
        seed = abs(hash(svc)) % 1000
        rng_local = np.random.default_rng(seed + int(ts.timestamp()) % 10_000)

        # Telemetry with slight drift + noise
        base_lat = 250 + (services.index(svc) * 20)            # ms
        base_cpu = 45 + (services.index(svc) * 3)              # %
        latency = float(np.clip(rng_local.normal(base_lat, 35), 30, 800))
        cpu     = float(np.clip(rng_local.normal(base_cpu, 12), 5, 99))
        mem     = float(np.clip(rng_local.normal(max(cpu*0.9, 15), 10), 5, 99))
        qps     = float(max(0, rng_local.normal(900, 180)))
        api_fail= float(np.clip(rng_local.normal(0.006, 0.003), 0, 0.25))
        decline = float(np.clip(rng_local.normal(0.03, 0.01), 0, 0.35))
        fraudpm = int(max(0, rng_local.normal(2 + services.index(svc)*0.3, 1)))

        tele_rows.append({
            "ts": ts.isoformat(),
            "service": svc,
            "txn_latency_ms": latency,
            "cpu_pct": cpu,
            "mem_pct": mem,
            "qps": qps,
            "api_fail_rate": api_fail,
            "decline_rate": decline,
            "fraud_alerts_per_min": fraudpm
        })

        # Detector scores (keep schema compatible with v1)
        s_if = float(np.clip((latency / 650.0) + api_fail*1.6 + rng_local.normal(0, 0.02), 0, 1))
        s_sv = float(np.clip((cpu + mem) / 200.0 + rng_local.normal(0, 0.02), 0, 1))
        s_ae = float(np.clip(api_fail*1.8 + rng_local.normal(0, 0.03), 0, 1))
        ens  = float(np.mean([s_if, s_sv, s_ae]))

        # Alert logic (can be tuned later)
        # Use slightly permissive thresholds so charts aren't empty
        alert = int((s_if > 0.75) + (s_sv > 0.75) + (s_ae > 0.80) >= 1)
        if svc == "payments-gateway" and alert:
            action = "open_incident_ticket"  # guardrail: no auto-scale on payments
        else:
            action = "scale_out" if (alert and cpu > 75) else ("open_incident_ticket" if alert else "notify_only")

        score_rows.append({
            "ts": ts.isoformat(),
            "service": svc,
            "score_iforest": s_if,
            "score_ocsvm": s_sv,
            "score_autoenc": s_ae,
            "score_ensemble": ens,
            "alert": alert,
            "action": action
        })

# Write fresh CSVs (overwrite if present)
pd.DataFrame(tele_rows).to_csv(telemetry_path, index=False)
pd.DataFrame(score_rows).to_csv(scores_path, index=False)

print(f"Wrote {telemetry_path} and {scores_path}")
print(f"Services: {services}")
print(f"Rows: telemetry={len(tele_rows)}, scores={len(score_rows)}")
