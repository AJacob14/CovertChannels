from Clients.TestClient import TestClient
from Clients.TcpPortClient import TcpPortClient
from Clients.UdpPortClient import UdpPortClient


def main():
    client = UdpPortClient("127.0.0.1", 42069)
    client.send(b"Hello World!")


if __name__ == "__main__":
    main()
