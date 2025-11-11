<p align="center">
  <img src="docs/banner_image_for_AI-driven_predictive_monitoring.png" alt="AI-Driven Predictive Monitoring and Anomaly Detection Framework" width="100%">
</p>

<div align="center">

# 🧠 SmartOps — AI-Driven Predictive Monitoring & Anomaly Detection in DevOps

[![Stars](https://img.shields.io/github/stars/jbazkar/smartops-framework?style=social)](https://github.com/jbazkar/smartops-framework/stargazers)
[![Issues](https://img.shields.io/github/issues/jbazkar/smartops-framework)](https://github.com/jbazkar/smartops-framework/issues)
[![CI](https://img.shields.io/github/actions/workflow/status/jbazkar/smartops-framework/ci.yml?label=build)](https://github.com/jbazkar/smartops-framework/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**Illustrative framework for AI-driven predictive monitoring and anomaly detection**  
in DevOps, BFSI, and cloud observability environments.

</div>

---

## 📘 Overview
SmartOps combines classic anomaly detection algorithms (Isolation Forest, One-Class SVM, Autoencoder)  
with policy-driven orchestration to predict issues, prevent failures, and trigger auto-remediation.

- Learns operational baselines from telemetry (CPU, latency, APIs, logs)
- Detects deviations indicating potential incidents
- Validates anomalies via guardrails
- Performs safe auto-remediation actions
- Generates human-readable evidence for research and EB1A documentation

---

## 🧩 Architecture Diagram

```mermaid
flowchart LR
  A[Sources: Logs & Metrics] --> B[Collectors]
  B --> C[Feature Engineering]
  C --> D1[Detector: Isolation Forest]
  C --> D2[Detector: One-Class SVM]
  C --> D3[Detector: Autoencoder]
  D1 --> E[Ensemble & Scoring]
  D2 --> E
  D3 --> E
  E --> F[Rules Engine: Policies & Guardrails]
  F --> G{Action?}
  G -- yes --> H[Remediator: Playbooks, Tickets, Runbooks]
  G -- no --> I[Observe & Notify]
  H --> J[Feedback Loop: Outcomes → Model Tuning]
  I --> J
```

> Predictive Monitoring learns “normal” system behavior using multiple anomaly detectors, fuses results, and triggers automated or guided remediation.

---

## ⚙️ Example Run

```bash
# Clone the repository
git clone https://github.com/jbazkar/smartops-framework.git
cd smartops-framework

# Run the illustrative SmartOps pipeline
python examples/simulate_pipeline.py --config configs/sample_config.yaml
```

This executes a sanitized simulation where SmartOps analyzes synthetic telemetry, applies rules, and performs a dry-run auto-remediation.

---

## 🗂 Repository Structure

```
smartops-framework/
├─ smartops/                  # Core modules
│  ├─ collectors/             # Data collectors
│  ├─ features/               # Feature engineering
│  ├─ detectors/              # ML models (IForest, OCSVM, Autoencoder)
│  ├─ fusion/                 # Ensemble fusion logic
│  ├─ rules/                  # Guardrails and thresholds
│  ├─ orchestrators/          # Pipeline orchestrators
│  └─ remediation/            # Remediation actions
├─ configs/                   # YAML configurations
├─ examples/                  # Example pipelines
├─ results_banking/           # BFSI synthetic datasets
├─ docs/                      # Architecture & Evidence
├─ assets/                    # Images and supporting visuals
├─ tests/                     # Unit/smoke tests
├─ LICENSE, CITATION.cff, README.md
└─ .github/workflows/         # CI automation
```

---

## 📊 Evidence Highlights

### Section 5 – Predictive Monitoring Results & Evidence  
Demonstrates early-stage anomaly detection and quantified improvement after AI SmartOps integration.  
📄 [`docs/evidence.md`](docs/evidence.md)

- AI Predictive Monitoring Curve  
  <img src="ai_predictive_monitoring_curve.png" width="80%" alt="AI Predictive Monitoring Concept">

- Quantitative Results (Before vs After)  
  <img src="ai_results_comparison.png" width="75%" alt="Before vs After Results">

### Section 6 – Before vs After AI Validation  
Shows measurable impact of AI on detection accuracy and false-positive reduction.

| Metric | Before | After | Improvement |
|--------|--------|--------|-------------|
| Anomaly Detection Accuracy | 70 % | 92 % | +22 % |
| False Positives | 30 % | 5 % | −25 % |

<img src="banking_before_after_comparison.png" width="70%" alt="Before vs After AI Performance Chart">

---

## 🧾 Licensing & Citation

© 2025 **Baskaran Jeyarajan (Baskar)**  
Licensed under the **Apache 2.0 License**.  

For academic references, please cite:

```bibtex
@software{Jeyarajan_SmartOps_2025,
  author       = {Baskaran Jeyarajan},
  title        = {SmartOps: AI-Driven Predictive Monitoring and Anomaly Detection in DevOps},
  year         = {2025},
  publisher    = {GitHub},
  url          = {https://github.com/jbazkar/smartops-framework},
  license      = {Apache-2.0}
}
```

---

## 🌐 Connect & Contributions

💬 **Author:** [Baskaran Jeyarajan (Baskar)](https://awsbaskar.net)  
🤝 Pull requests and issue reports are welcome — please see [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

<p align="center">
  <sub>© 2025 Baskaran Jeyarajan. All Rights Reserved. | AI SmartOps Framework</sub>
</p>
