#!/usr/bin/env python3
"""
mock_netconf_server.py

Lightweight TCP-only mock that listens on a host/port and, upon connection,
sends a minimal NETCONF <hello> banner. It then logs incoming bytes and closes.

This is NOT a full SSH/NETCONF server. It exists to:
  - Prove that a TCP port is open and reachable
  - Allow simple tests with `nc -vz` / `telnet`
  - Provide a basic demo target for connection attempts

Limitations:
  - No SSH handshake, no NETCONF framing, no RPC handling
  - ncclient (which expects SSH) will fail against this mock

Usage:
  python3 scripts/mock_netconf_server.py --host 127.0.0.1 --port 1830
"""

import argparse
import socket
import socketserver
import threading


HELLO_BANNER = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    "<hello xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\">\n"
    "  <capabilities>\n"
    "    <capability>urn:ietf:params:netconf:base:1.0</capability>\n"
    "  </capabilities>\n"
    "</hello>\n"
)


class Handler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        peer = self.client_address
        print(f"🔌 [mock_netconf_server] Connection from {peer}")
        try:
            self.request.sendall(HELLO_BANNER.encode("utf-8"))
            self.request.settimeout(2.0)
            try:
                data = self.request.recv(4096)
                if data:
                    print(f"📥 [mock_netconf_server] Received {len(data)} bytes: {data[:80]!r} ...")
            except socket.timeout:
                pass
        except Exception as exc:
            print(f"❌ [mock_netconf_server] Error handling client: {exc}")
        finally:
            try:
                self.request.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            self.request.close()
            print(f"🔚 [mock_netconf_server] Closed connection to {peer}")


def main() -> int:
    parser = argparse.ArgumentParser(description="TCP-only NETCONF banner mock server")
    parser.add_argument("--host", default="127.0.0.1", help="Listen address (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=1830, help="Listen port (default 1830)")
    args = parser.parse_args()

    server = socketserver.TCPServer((args.host, args.port), Handler)
    server.allow_reuse_address = True

    print(f"🚀 [mock_netconf_server] Listening on {args.host}:{args.port}")
    print("ℹ️  This is TCP-only; ncclient expects SSH and may still fail.")

    try:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        thread.join()
    except KeyboardInterrupt:
        print("\n🛑 [mock_netconf_server] Shutting down...")
    finally:
        server.shutdown()
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


