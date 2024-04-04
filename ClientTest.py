from covert_channels.Clients import Client, HttpClient, IpIdClient, TcpPortClient, UdpPortClient

def main():
    client = IpIdClient("127.0.0.1", 42069)
    client.send(b"Hello World!")


if __name__ == "__main__":
    main()
