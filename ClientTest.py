from Clients.TcpPortClient import TcpPortClient
from Clients.UdpPortClient import UdpPortClient
from Clients.HttpClient import HttpClient


def main():
    client = HttpClient("127.0.0.1", 42069)
    client.send(b"Hello World!")


if __name__ == "__main__":
    main()
