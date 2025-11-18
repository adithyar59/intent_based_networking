#!/usr/bin/env bash

set -euo pipefail

echo "[setup] Starting environment setup for Intent-Based Networking project..."

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
echo "[setup] Project root: $PROJECT_ROOT"

# Ensure basic system tools are present (non-interactive)
echo "[setup] Updating apt package lists (non-interactive)..."
DEBIAN_FRONTEND=noninteractive sudo -n true 2>/dev/null || true
sudo apt-get update -y || true

# Optionally install Prometheus and node exporter (best-effort)
echo "[setup] (Optional) Installing Prometheus and node exporter (best-effort)..."
sudo apt-get install -y prometheus prometheus-node-exporter || true

# Python & venv
if ! command -v python3 >/dev/null 2>&1; then
  echo "[setup] Installing python3..."
  sudo apt-get install -y python3 || true
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
  echo "[setup] Installing python3-venv to enable virtual environments..."
  sudo apt-get install -y python3-venv || true
fi

VENV_DIR="$PROJECT_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "[setup] Creating Python virtual environment at $VENV_DIR ..."
  python3 -m venv "$VENV_DIR" || {
    echo "[setup] venv creation failed; falling back to user virtualenv..."
    python3 -m pip install --user --break-system-packages virtualenv || true
    ~/.local/bin/virtualenv "$VENV_DIR"
  }
fi

# Activate venv
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo "[setup] Installing Python dependencies into venv (ncclient, prometheus-api-client)..."
pip install ncclient prometheus-api-client lxml

# Make scripts executable
chmod +x "$PROJECT_ROOT/scripts/intent_parser.py" || true
chmod +x "$PROJECT_ROOT/scripts/netconf_push.py" || true
chmod +x "$PROJECT_ROOT/scripts/verify_prometheus.py" || true
chmod +x "$PROJECT_ROOT/scripts/test_netconf_conn.py" || true
chmod +x "$PROJECT_ROOT/scripts/mock_netconf_server.py" || true
chmod +x "$PROJECT_ROOT/setup_environment.sh" || true

cat <<'EON'
[setup] Done.

Next steps:
  1) Activate venv:
       source .venv/bin/activate
  2) Generate config from intent:
       python3 scripts/intent_parser.py
  3) (Optional) Start mock NETCONF TCP server (for connectivity demo):
       python3 scripts/mock_netconf_server.py --host 127.0.0.1 --port 1830
  4) Test NETCONF connectivity (will fail against TCP-only mock, succeeds with real SSH/NETCONF):
       NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 python3 scripts/test_netconf_conn.py
  5) Attempt push (auto-fallback to simulation on error):
       NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 NETCONF_USER=admin NETCONF_PASS=admin \
       python3 scripts/netconf_push.py

Notes:
  - Prometheus install is optional; you can also use Docker for Prometheus:
      docker run --rm -p 9090:9090 -v "$PWD/prometheus:/etc/prometheus" prom/prometheus
  - The mock server is TCP-only and not a full SSH/NETCONF implementation.
EON


