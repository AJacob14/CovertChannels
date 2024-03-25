from __future__ import annotations

from enum import IntEnum

from Clients.Client import Client
from Clients.HttpClient import HttpClient
from Clients.IpIdClient import IpIdClient
from Clients.TcpPortClient import TcpPortClient
from Clients.UdpPortClient import UdpPortClient
from Servers.Server import Server
from Servers.HttpServer import HttpServer
from Servers.IpIdServer import IpIdServer
from Servers.TcpPortServer import TcpPortServer
from Servers.UdpPortServer import UdpPortServer

class ClientServer:
    def __init__(self, ip: str, port: int, type_: ClientServerType):
        self.client: Client = None
        self.server: Server = None
        self.__construct_client_server(ip, port, type_)

    def __construct_client_server(self, ip: str, port: int, type_: ClientServerType):
        match type_:
            case ClientServerType.HTTP:
                self.client = HttpClient(ip, port)
                self.server = HttpServer(ip, port)
            case ClientServerType.IP_ID:
                self.client = IpIdClient(ip, port)
                self.server = IpIdServer(ip, port)
            case ClientServerType.TCP_PORT:
                self.client = TcpPortClient(ip, port)
                self.server = TcpPortServer(ip, port)
            case ClientServerType.UDP_PORT:
                self.client = UdpPortClient(ip, port)
                self.server = UdpPortServer(ip, port)

class ClientServerType(IntEnum):
    HTTP = 0,
    IP_ID = 1,
    TCP_PORT = 2,
    UDP_PORT = 3

if __name__ == "__main__":
    pass
