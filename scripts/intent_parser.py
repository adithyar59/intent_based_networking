#!/usr/bin/env python3
"""
intent_parser.py

Reads a high-level intent from intents/campus_policy.json and translates it
into a YANG-based XML configuration aligned with models/campus_lan.yang.

Outputs the XML configuration to generated_config.xml in the project root
(intent_based_networking/generated_config.xml).

This script is intentionally verbose with logs and comments for academic clarity.
"""

import json
import os
import sys
from xml.etree.ElementTree import Element, SubElement, tostring


def resolve_project_root() -> str:
    """Resolve the project root directory (intent_based_networking)."""
    # scripts/ is one level below the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return project_root


def load_intent(intent_path: str) -> dict:
    """Load the JSON intent file and return it as a dictionary."""
    with open(intent_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def build_xml_from_intent(intent_data: dict) -> str:
    """Generate XML string matching the YANG model (campus-lan)."""
    # Root element corresponds to container campus-network with the correct namespace
    ns = "urn:example:campus-lan"
    campus_network = Element("campus-network", {"xmlns": ns})

    # Expecting structure: vlans: { name: id }, policies: { name: policy }
    vlans = intent_data.get("vlans", {})
    policies = intent_data.get("policies", {})

    for vlan_name, vlan_id in vlans.items():
        vlan_elem = SubElement(campus_network, "vlan")
        id_elem = SubElement(vlan_elem, "id")
        id_elem.text = str(vlan_id)

        name_elem = SubElement(vlan_elem, "name")
        name_elem.text = str(vlan_name)

        policy_value = policies.get(vlan_name, "restricted")
        policy_elem = SubElement(vlan_elem, "policy")
        policy_elem.text = str(policy_value)

    # tostring returns bytes; decode to str
    xml_bytes = tostring(campus_network, encoding="utf-8")
    xml_str = xml_bytes.decode("utf-8")
    return xml_str


def save_xml(xml_str: str, output_path: str) -> None:
    """Persist the XML to the given output path."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)


def main() -> int:
    print("[intent_parser] Starting intent parsing and translation...")
    project_root = resolve_project_root()
    intent_path = os.path.join(project_root, "intents", "campus_policy.json")

    if not os.path.exists(intent_path):
        print(f"[intent_parser] ERROR: Intent file not found: {intent_path}")
        return 1

    try:
        intent_data = load_intent(intent_path)
        print("[intent_parser] Intent loaded successfully.")
    except Exception as exc:
        print(f"[intent_parser] ERROR loading intent: {exc}")
        return 1

    try:
        xml_str = build_xml_from_intent(intent_data)
        print("[intent_parser] YANG-based XML configuration generated.")
    except Exception as exc:
        print(f"[intent_parser] ERROR generating XML: {exc}")
        return 1

    output_path = os.path.join(project_root, "generated_config.xml")
    try:
        save_xml(xml_str, output_path)
        print(f"[intent_parser] XML saved to: {output_path}")
        print("Intent successfully translated to YANG config.")
    except Exception as exc:
        print(f"[intent_parser] ERROR saving XML: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
