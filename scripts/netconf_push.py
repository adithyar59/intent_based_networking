#!/usr/bin/env python3
"""
netconf_push.py

Purpose
  - Attempt a real NETCONF push using ncclient.
  - If connection/edit-config fails for any reason (socket/SSH/timeout),
    automatically fall back to a deterministic simulation so demos always run.

Environment variables (with defaults):
  NETCONF_HOST (default "192.168.1.10")
  NETCONF_PORT (default 830)
  NETCONF_USER (default "admin")
  NETCONF_PASS (default "admin")
  TIMEOUT      (default 10 seconds)

Usage example (override host/port, run inside venv):
  NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 NETCONF_USER=admin NETCONF_PASS=admin \
  .venv/bin/python scripts/netconf_push.py

Safety note
  The mock/simulation is for demo reproducibility and does not configure a real device.
  When presenting results, indicate whether the push was REAL or SIMULATED.
"""

import os
import sys
import time
from typing import Optional
from xml.etree import ElementTree as ET


def resolve_project_root() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return project_root


def read_generated_xml(project_root: str) -> Optional[str]:
    xml_path = os.path.join(project_root, "generated_config.xml")
    if not os.path.exists(xml_path):
        print("❌ [netconf_push] ERROR: generated_config.xml not found at", xml_path)
        print("   Run: .venv/bin/python scripts/intent_parser.py")
        return None
    with open(xml_path, "r", encoding="utf-8") as f:
        return f.read()


def simulate_netconf_push(xml_config: str) -> bool:
    """Simulate NETCONF push deterministically using the generated XML."""
    print("⚠️  [netconf_push] Falling back to SIMULATION mode.")
    print("   Simulating NETCONF push...")
    time.sleep(0.3)

    try:
        root = ET.fromstring(xml_config)
        for vlan in root.findall(".//vlan"):
            vlan_id_el = vlan.find("id")
            name_el = vlan.find("name")
            vlan_id = vlan_id_el.text.strip() if vlan_id_el is not None and vlan_id_el.text else "?"
            name = name_el.text.strip() if name_el is not None and name_el.text else "?"
            print(f"   Applying VLAN config: VLAN {vlan_id} -> {name}")
            time.sleep(0.1)
    except Exception:
        print("   Applying configuration (generic items)...")
        time.sleep(0.2)

    print("   Commit simulated.")
    print("✅ [netconf_push] Configuration push completed successfully (SIMULATED).")
    return True


def push_via_netconf(host: str, port: int, username: str, password: str, timeout: int, xml_config: str) -> bool:
    try:
        from ncclient import manager
    except Exception as exc:
        print(f"⚠️  [netconf_push] ncclient not available: {exc}")
        return False

    print(f"🔌 [netconf_push] Connecting to NETCONF device {host}:{port} (timeout {timeout}s) ...")
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
            print("📨 [netconf_push] Connected. Pushing configuration via edit-config ...")
            config_payload = f"""
<config>
{xml_config}
</config>
""".strip()
            response = m.edit_config(target="running", config=config_payload)
            print("✅ [netconf_push] edit-config RPC reply:")
            print(response)
            print("✅ [netconf_push] Configuration pushed successfully (REAL device).")
            return True
    except Exception as exc:
        print(f"❌ [netconf_push] Real push failed: {exc}")
        return False


def main() -> int:
    print("[netconf_push] Starting NETCONF push...")
    project_root = resolve_project_root()
    xml_config = read_generated_xml(project_root)
    if xml_config is None:
        return 2

    host = os.environ.get("NETCONF_HOST", "192.168.1.10")
    port = int(os.environ.get("NETCONF_PORT", "830"))
    username = os.environ.get("NETCONF_USER", "admin")
    password = os.environ.get("NETCONF_PASS", "admin")
    timeout = int(os.environ.get("TIMEOUT", "10"))

    if push_via_netconf(host, port, username, password, timeout, xml_config):
        return 0

    simulate_netconf_push(xml_config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
