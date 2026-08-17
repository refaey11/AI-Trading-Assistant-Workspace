#!/usr/bin/env bash
set -euo pipefail

REPO="refaey11/AI-Trading-Assistant-Workspace"
RUNNER_DIR="$HOME/actions-runner"
mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR"

URL="$(gh api repos/actions/runner/releases/latest --jq '.assets[] | select(.name | endswith("linux-x64.tar.gz")) | .browser_download_url')"
curl -fsSL "$URL" -o actions-runner.tar.gz
tar -xzf actions-runner.tar.gz
TOKEN="$(gh api -X POST "repos/$REPO/actions/runners/registration-token" --jq '.token')"
./config.sh --url "https://github.com/$REPO" --token "$TOKEN" --name "codespace-0042-0045" --labels "self-hosted,codespace,0042-0045" --unattended
exec ./run.sh
