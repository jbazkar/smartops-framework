pipeline {
  agent any
  options { timestamps(); ansiColor('xterm'); }
  environment {
    PYTHON = 'python3'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python') {
      steps {
        sh '''
          python3 -V || python -V || true
          python3 -m venv .venv || python -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          # Use requirements.txt if present, else install minimal deps
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          else
            pip install pyyaml numpy pandas matplotlib scikit-learn reportlab
          fi
        '''
      }
    }

    stage('Run SmartOps Simulation') {
      steps {
        sh '''
          . .venv/bin/activate
          export PYTHONPATH=.
          python examples/simulate_pipeline.py --config configs/sample_config.yaml
        '''
      }
    }

    stage('Generate Deployment Summary (Markdown + JSON)') {
      steps {
        sh '''
          . .venv/bin/activate
          python - << "PY"
import os, csv, json, pathlib
root = pathlib.Path(".")
art = root / "artifacts"; art.mkdir(exist_ok=True)

# Read impact table if available
rows = []
csv_path = root / "results_banking" / "banking_impact_summary.csv"
if csv_path.exists():
    rows = list(csv.DictReader(open(csv_path, newline="", encoding="utf-8")))

# Compose markdown summary
md = []
md.append(f"## Deployment Summary (PR #{os.getenv('CHANGE_ID','N/A')})")
md.append("")
md.append(f"**Source Branch:** {os.getenv('CHANGE_BRANCH','')} → **Target:** {os.getenv('CHANGE_TARGET','')}")
md.append(f"**Commit:** {os.getenv('GIT_COMMIT','')[:7]}")
md.append("")
if rows:
    md.append("### Impact Metrics")
    md.append("")
    for r in rows:
        md.append(f"- **{r['Metric']}**: {r['Before AI Implementation']} → {r['After AI Implementation']} ({r['Improvement %']})")
else:
    md.append("_No impact summary CSV found (results_banking/banking_impact_summary.csv)._")

md_path = art / "deploy_summary.md"
md_path.write_text("\\n".join(md), encoding="utf-8")

# Prepare GitHub issue-comment payload for PR
body = {"body": md_path.read_text(encoding="utf-8")}
(art / "deploy_summary.json").write_text(json.dumps(body), encoding="utf-8")
print("Wrote", md_path, "and artifacts/deploy_summary.json")
PY
        '''
      }
    }
  }

  post {
    success {
      // Archive artifacts so you can browse them in Jenkins
      archiveArtifacts artifacts: 'artifacts/**,results_banking/*.png,results_banking/*.csv,docs/*.pdf', allowEmptyArchive: true

      // If this is a PR build, post a comment with the summary (requires a GitHub token credential)
      script {
        if (env.CHANGE_ID) {
          withCredentials([string(credentialsId: 'github_token', variable: 'GHTOKEN')]) {
            sh """
              curl -sS -H 'Authorization: Bearer ${GHTOKEN}' -H 'Accept: application/vnd.github+json' \
                -X POST \
                -d @artifacts/deploy_summary.json \
                https://api.github.com/repos/jbazkar/smartops-framework/issues/${CHANGE_ID}/comments
            """
          }
        }
      }
    }
    always {
      cleanWs()
    }
  }
}
