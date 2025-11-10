# Architecture (Illustrative)

SmartOps analyzes telemetry (CPU, latency, API performance) using an ensemble of Isolation Forest, One-Class SVM, and Autoencoder. Scores are fused, validated by a Rules Engine, and—if permitted—trigger safe, dry-run remediation.

```mermaid
flowchart TB
  subgraph Ingest
  A[Log Collector] --> C[Feature Engineering]
  B[Metrics Collector] --> C
  end
  C --> D1[Isolation Forest]
  C --> D2[One-Class SVM]
  C --> D3[Autoencoder]
  D1 --> E[Score Fusion]
  D2 --> E
  D3 --> E
  E --> F[Rules Engine]
  F --> G{Permit?}
  G -- Yes --> H[Remediator]
  G -- No --> I[Notify / Ticket]
  H --> J[Feedback Store]
  I --> J


