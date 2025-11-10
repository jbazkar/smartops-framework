# Banking/Financial Results (Illustrative)

This set mirrors common BFSI workloads (credit auth, payments, fraud detection, loan eligibility, account summary). 
It shows how SmartOps can surface anomalies and trigger guarded remediation.

## Files
- `results_banking/banking_telemetry.csv` — Synthetic BFSI telemetry (latency, CPU/MEM, QPS, failure/decline/fraud rates).
- `results_banking/banking_model_scores.csv` — Detector and ensemble scores plus alert/action labels.
- `results_banking/banking_latency_cpu_alerts.png` — Latency/CPU averages with alert markers.
- `results_banking/banking_ensemble_trend.png` — Ensemble anomaly score (avg).
- `results_banking/banking_alerts_by_service.png` — Alert counts per BFSI service.
- `results_banking/banking_actions.png` — Actions triggered (policy blocks payments-gateway by design).

> Data is randomized and sanitized; use for demos, GitHub evidence, and EB1A exhibits.
