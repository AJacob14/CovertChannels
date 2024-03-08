import socket

from scapy.all import *

from Servers.TestServer import TestServer
from Servers.Layer3PortServer import Layer3PortServer

def main():
    server = Layer3PortServer("127.0.0.1", 42069)
    queue = bytearray()
    with server:
        print("Waiting for data...")
        data = server.receive()
        print(f"Data received: {data}")

if __name__ == "__main__":
    main()
