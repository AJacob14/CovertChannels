from Clients.TestClient import TestClient
from Clients.TcpPortClient import TcpPortClient

def main():
    client = TcpPortClient("127.0.0.1", 42069)
    client.send(b"Hello World!")

if __name__ == "__main__":
    main()
