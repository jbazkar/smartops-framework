from __future__ import annotations
import argparse
from smartops.config import load_config
from smartops.collectors.log_collector import stream_logs
from smartops.collectors.metrics_collector import stream_metrics
from smartops.features.feature_engineer import make_features
from smartops.detectors.isolation_forest import IsolationForestDetector
from smartops.detectors.oneclass_svm import OneClassSVMDetector
from smartops.detectors.autoencoder import AutoencoderDetector
from smartops.rules.rules_engine import decide
from smartops.orchestrators.remediator import run as remediate
from smartops.evaluation.metrics import fuse_scores

def main(cfg_path: str):
    cfg = load_config(cfg_path)
    iforest = IsolationForestDetector(threshold=cfg.detectors.get("iforest_threshold", 0.7))
    ocsvm = OneClassSVMDetector(threshold=cfg.detectors.get("ocsvm_threshold", 0.75))
    ae = AutoencoderDetector(threshold=cfg.detectors.get("ae_threshold", 0.8))

    for log, metric in zip(stream_logs(25), stream_metrics(25)):
        x, ctx = make_features(log, metric)
        scores = {
            "iforest": iforest.score(x),
            "ocsvm": ocsvm.score(x),
            "ae": ae.score(x),
        }
        fused = fuse_scores(list(scores.values()))
        policy = {
            "min_votes": cfg.rules.get("min_votes", 2),
            "min_score": cfg.rules.get("min_score", 0.75),
            "blocked_services": cfg.rules.get("blocked_services", []),
            "service": ctx.get("service", "unknown"),
        }
        decision = decide(scores, policy)
        action = cfg.remediation.get("action_on_permit", "open_ticket")
        params = {"service": ctx.get("service"), "fused_score": fused}
        result = remediate(action if decision["permit"] else "notify_only", params, dry_run=True)
        print(f"ctx={ctx} scores={scores} fused={fused:.2f} decision={decision} result={result}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    main(args.config)
