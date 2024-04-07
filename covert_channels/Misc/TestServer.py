"""
    This is the server counterpart to the TestClient for testing manual TCP handshake completion through scapy. This
    script is for research purposes and is not used in the covert channel implementation.
"""

from __future__ import annotations

import socket

from scapy.all import *

HOST = "127.0.0.1"
PORT = 31337


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    conn, addr = server.accept()
    print(f"Connection from {addr}")
    while True:
        data = conn.recv(4096)
        if not data:
            break
        print(f"Received data: {data}")


if __name__ == "__main__":
    main()
