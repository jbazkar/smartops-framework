# tools/build_endpoint_and_cm_v2.py
"""
Creates the two missing dashboard artifacts for v2:
  - results_banking_v2/banking_endpoint_alerts_v2.csv
  - results_banking_v2/banking_confusion_matrix_v2.png
Requires: pandas, numpy, matplotlib
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

base = Path("results_banking_v2")
scores_path = base / "banking_model_scores.csv"
if not scores_path.exists():
    raise SystemExit("Missing results_banking_v2/banking_model_scores.csv. "
                     "Run tools/generate_bfsi_dataset_v2.py first.")

# ---- Load model scores
scores = pd.read_csv(scores_path)

# Adjusted alert flag (matches analyzer logic)
scores["alert_adj"] = (
    (scores["score_iforest"] > 0.70) |
    (scores["score_ocsvm"] > 0.70) |
    (scores["score_autoenc"] > 0.75)
).astype(int)

# ---- Fake endpoint assignment (stable & readable)
endpoint_map = {
    "credit-card-auth": ["/auth","/authorize","/capture"],
    "payments-gateway": ["/charge","/refund","/settle"],
    "fraud-detection": ["/score","/report","/block"],
    "loan-eligibility": ["/check","/approve","/reject"],
    "account-summary": ["/fetch","/update","/notify"],
}
scores["__rowid"] = np.arange(len(scores))
def pick_ep(row):
    eps = endpoint_map.get(row.get("service",""), ["/op"])
    return eps[int(row["__rowid"]) % len(eps)]
scores["endpoint"] = scores.apply(pick_ep, axis=1)

# ---- Aggregate endpoint alerts and save CSV
ep = scores.groupby(["service","endpoint"])["alert_adj"].sum().reset_index()
out_csv = base / "banking_endpoint_alerts_v2.csv"
ep.to_csv(out_csv, index=False)
print("Wrote:", out_csv)

# ---- Build a simple confusion matrix plot (synthetic ground truth)
rng = np.random.default_rng(2025)
y_true = rng.choice([0,1], size=len(scores), p=[0.92, 0.08])
y_pred = scores["alert_adj"].to_numpy()

tp = int(((y_true==1)&(y_pred==1)).sum())
fp = int(((y_true==0)&(y_pred==1)).sum())
fn = int(((y_true==1)&(y_pred==0)).sum())
tn = int(((y_true==0)&(y_pred==0)).sum())

cm = np.array([[tn, fp], [fn, tp]])

plt.figure(figsize=(4.2,4))
plt.imshow(cm, cmap="Greys")
for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i,j], ha="center", va="center", fontsize=12)
plt.xticks([0,1], ["Pred 0","Pred 1"])
plt.yticks([0,1], ["True 0","True 1"])
plt.title("Banking v2: Confusion Matrix (synthetic truth)")
plt.tight_layout()

out_png = base / "banking_confusion_matrix_v2.png"
plt.savefig(out_png, dpi=200, bbox_inches="tight")
plt.close()
print("Wrote:", out_png)
