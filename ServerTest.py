"""
    Test the various covert channels servers.
"""

from covert_channels.Servers import IpIdServer


def main():
    server = IpIdServer("127.0.0.1", 31337)
    with server:
        print("Waiting for data...")
        data = server.receive()
        print(f"Data received: {data}")


if __name__ == "__main__":
    main()
