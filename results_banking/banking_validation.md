# Banking Per-Endpoint & Validation Summary

### 1. Endpoint Breakdown
Each BFSI service is subdivided into representative API endpoints (e.g., /auth, /charge, /score).
SmartOps records alert counts at endpoint granularity.

- Data: [`banking_endpoint_alerts.csv`](results_banking/banking_endpoint_alerts.csv)
- **Visualization:**
  <img src="banking_endpoint_alerts.png" width="80%" alt="Endpoint Alerts">

### 2. Validation (Illustrative)
Randomized synthetic "ground truth" anomalies were assigned to estimate detection quality.

| Metric | Value |
|--------|--------|
| True Positives | 0 |
| False Positives | 0 |
| False Negatives | 71 |
| True Negatives | 1129 |
| Precision | 0.00 |
| Recall | 0.00 |
| F1 Score | 0.00 |

- **Visualization:**
  <img src="banking_confusion_matrix.png" width="45%" alt="Confusion Matrix">


> These are illustrative only—showing how your SmartOps anomaly detectors can be validated on BFSI workloads.
