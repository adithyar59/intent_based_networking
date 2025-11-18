#!/usr/bin/env python3
"""
verify_prometheus.py

Connects to a local Prometheus server and runs basic health queries
to verify that targets are up and network interfaces are healthy.
"""

import sys


def query_metrics() -> int:
    try:
        from prometheus_api_client import PrometheusConnect
    except Exception as exc:
        print(f"[verify_prometheus] prometheus-api-client not available: {exc}")
        print("[verify_prometheus] Install it via: pip install prometheus-api-client")
        return 1

    prom_url = "http://localhost:9090"
    print(f"[verify_prometheus] Connecting to Prometheus at {prom_url} ...")
    try:
        prom = PrometheusConnect(url=prom_url, disable_ssl=True)
        if not prom.check_prometheus_connection():
            print("[verify_prometheus] ERROR: Unable to connect to Prometheus.")
            return 2
        print("[verify_prometheus] Connected to Prometheus.")
    except Exception as exc:
        print(f"[verify_prometheus] ERROR connecting to Prometheus: {exc}")
        return 2

    queries = [
        ("up", "General scrape target up/down status"),
        ("node_network_up", "Network interface up/down status"),
    ]

    for expr, description in queries:
        try:
            print(f"[verify_prometheus] Querying: {expr}  (# {description})")
            # Using a simple instant query
            result = prom.custom_query(query=expr)
            print(f"[verify_prometheus] Result for {expr}:")
            print(result if result else "[]")
        except Exception as exc:
            print(f"[verify_prometheus] ERROR executing query {expr}: {exc}")

    print("[verify_prometheus] Verification complete.")
    return 0


if __name__ == "__main__":
    sys.exit(query_metrics())
