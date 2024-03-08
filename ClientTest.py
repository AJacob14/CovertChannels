from Clients.TestClient import TestClient
from Clients.Layer3PortClient import Layer3PortClient

def main():
    client = Layer3PortClient("127.0.0.1", 42069)
    client.send(b"Hello World!")

if __name__ == "__main__":
    main()
