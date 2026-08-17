#!/usr/bin/env bash
set -euo pipefail

REPO="refaey11/AI-Trading-Assistant-Workspace"
RUNNER_DIR="$HOME/actions-runner"
mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR"

URL="$(gh api "repos/$REPO/actions/runners/downloads" --jq '.[] | select(.os == "linux" and .architecture == "x64") | .download_url' | head -n1)"
if [[ -z "$URL" ]]; then
  echo "ERROR: GitHub did not return a Linux x64 runner download URL."
  exit 1
fi

curl -fsSL "$URL" -o actions-runner.tar.gz
tar -xzf actions-runner.tar.gz
TOKEN="$(gh api -X POST "repos/$REPO/actions/runners/registration-token" --jq '.token')"
./config.sh --url "https://github.com/$REPO" --token "$TOKEN" --name "codespace-0042-0045" --labels "self-hosted,codespace,0042-0045" --unattended --replace
exec ./run.sh
