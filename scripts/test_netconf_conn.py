#!/usr/bin/env python3
"""
test_netconf_conn.py

Small ncclient-based connection test that prints server capabilities on success,
otherwise prints the exact exception and suggests starting the mock server or
using env var overrides.

Environment variables (with defaults):
  NETCONF_HOST (default "192.168.1.10")
  NETCONF_PORT (default 830)
  NETCONF_USER (default "admin")
  NETCONF_PASS (default "admin")
  TIMEOUT      (default 10 seconds)

Example:
  .venv/bin/python scripts/test_netconf_conn.py
  NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 .venv/bin/python scripts/test_netconf_conn.py

Safety note
  True NETCONF requires an SSH-capable NETCONF server. The provided mock server
  is TCP-only and will not perform an SSH handshake.
"""

import os
import sys


def main() -> int:
    try:
        from ncclient import manager
    except Exception as exc:
        print(f"❌ [test_netconf_conn] ncclient not available: {exc}")
        print("   Activate venv and install dependencies:")
        print("   source .venv/bin/activate && pip install ncclient")
        return 2

    host = os.environ.get("NETCONF_HOST", "192.168.1.10")
    port = int(os.environ.get("NETCONF_PORT", "830"))
    username = os.environ.get("NETCONF_USER", "admin")
    password = os.environ.get("NETCONF_PASS", "admin")
    timeout = int(os.environ.get("TIMEOUT", "10"))

    print(f"🔌 [test_netconf_conn] Connecting to {host}:{port} (timeout {timeout}s) ...")
    try:
        with manager.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False,
            timeout=timeout,
        ) as m:
            print("✅ [test_netconf_conn] Connected. Server capabilities:")
            for cap in m.server_capabilities:
                print(f"   - {cap}")
            return 0
    except Exception as exc:
        print(f"❌ [test_netconf_conn] Connection failed: {exc}")
        print("   Tips:")
        print("   - Start mock server (TCP-only): python3 scripts/mock_netconf_server.py --host 127.0.0.1 --port 1830")
        print("   - Override env vars: NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 .venv/bin/python scripts/test_netconf_conn.py")
        print("   - For real devices, ensure SSH/NETCONF is enabled and port is open.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


