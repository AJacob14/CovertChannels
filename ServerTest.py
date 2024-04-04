import socket

from scapy.all import *

from covert_channels.Servers import TcpPortServer, UdpPortServer, HttpServer, IpIdServer


def main():
    server = IpIdServer("127.0.0.1", 42069)
    with server:
        print("Waiting for data...")
        data = server.receive()
        print(f"Data received: {data}")


if __name__ == "__main__":
    main()
