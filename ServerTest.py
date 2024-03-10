import socket

from scapy.all import *

from Servers.TcpPortServer import TcpPortServer
from Servers.UdpPortServer import UdpPortServer
from Servers.HttpServer import HttpServer


def main():
    server = HttpServer("127.0.0.1", 42069)
    with server:
        print("Waiting for data...")
        data = server.receive()
        print(f"Data received: {data}")


if __name__ == "__main__":
    main()
