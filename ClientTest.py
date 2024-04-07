"""
    Test the various covert channels clients.
"""


from covert_channels.Clients import IpIdClient


def main():
    client = IpIdClient("127.0.0.1", 31337)
    client.send(b"Hello World!")


if __name__ == "__main__":
    main()
