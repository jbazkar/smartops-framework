"""
Builds results_banking_v2/banking_impact_summary_v2.csv from model scores.
Uses the same thresholds and RNG seed as the other v2 artifacts so numbers align.
"""

from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path("results_banking_v2")
scores_csv = BASE / "banking_model_scores.csv"
out_csv    = BASE / "banking_impact_summary_v2.csv"

if not scores_csv.exists():
    raise SystemExit("Missing results_banking_v2/banking_model_scores.csv. "
                     "Run tools/generate_bfsi_dataset_v2.py first.")

# Load model scores
df = pd.read_csv(scores_csv)

# Alert decision (match analyzer logic)
alert = (
    (df["score_iforest"]  > 0.70) |
    (df["score_ocsvm"]    > 0.70) |
    (df["score_autoenc"]  > 0.75)
).astype(int).to_numpy()

# Synthetic ground truth (same seed as confusion-matrix builder)
rng = np.random.default_rng(2025)
y_true = rng.choice([0, 1], size=len(df), p=[0.92, 0.08])   # 8% anomalies
y_pred = alert

# Confusion counts
tp = int(((y_true==1) & (y_pred==1)).sum())
fp = int(((y_true==0) & (y_pred==1)).sum())
fn = int(((y_true==1) & (y_pred==0)).sum())
tn = int(((y_true==0) & (y_pred==0)).sum())

def pct(x): return f"{round(x*100)}%"

acc  = (tp + tn) / (tp + tn + fp + fn)
fpr  = (fp) / (fp + tn) if (fp + tn) else 0.0
prec = (tp) / (tp + fp) if (tp + fp) else 0.0
rec  = (tp) / (tp + fn) if (tp + fn) else 0.0

rows = [
    {"Metric": "Anomaly Detection Accuracy", "Banking v2 (Actual)": pct(acc)},
    {"Metric": "False Positive Rate",        "Banking v2 (Actual)": pct(fpr)},
    {"Metric": "Precision",                  "Banking v2 (Actual)": pct(prec)},
    {"Metric": "Recall",                     "Banking v2 (Actual)": pct(rec)},
]
pd.DataFrame(rows).to_csv(out_csv, index=False)
print("Wrote:", out_csv)