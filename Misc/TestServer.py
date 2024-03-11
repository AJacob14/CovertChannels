from __future__ import annotations

import socket

from scapy.all import *

HOST = "127.0.0.1"
PORT = 42069

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
