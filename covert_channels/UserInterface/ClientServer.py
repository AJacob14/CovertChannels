from __future__ import annotations

from enum import IntEnum
from multiprocessing import Process, Queue

from covert_channels.Clients import Client, HttpClient, IpIdClient, TcpPortClient, UdpPortClient
from covert_channels.Servers import Server, HttpServer, IpIdServer, TcpPortServer, UdpPortServer

class ClientServer:
    def __init__(self, ip: str, port: int, type_: ClientServerType):
        self.client: Client = None
        self.client_process: Process = None
        self.client_queue: Queue = Queue()
        self.server: Server = None
        self.server_process: Process = None
        self.server_queue: Queue = Queue()
        self.type: ClientServerType = type_
        self.__active: bool = False
        self.__construct_client_server(ip, port, type_)

    @property
    def active(self) -> bool:
        return self.__active
    
    @active.setter
    def active(self, value: bool):
        self.__active = value

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

    def start(self):
        self.client_process = Process(target=ClientServer._start_client, args=(self.client_queue, self.client))
        self.server_process = Process(target=ClientServer._start_server, args=(self.server_queue, self.server))
        self.server_process.start()
        self.client_process.start()

    def stop(self):
        self.client_process.terminate()
        self.server_process.terminate()

    def send(self, data: bytes) -> bytes:
        self.client_queue.put(data)
        data = self.server_queue.get()
        return data

    @staticmethod
    def _start_client(queue: Queue, client: Client):
        while True:
            message = queue.get()
            if isinstance(message, str):
                message = message.encode()
            client.send(message)

    @staticmethod
    def _start_server(queue: Queue, server: Server):
        while True:
            data = server.receive()
            queue.put(data)


class ClientServerType(IntEnum):
    HTTP = 0,
    IP_ID = 1,
    TCP_PORT = 2,
    UDP_PORT = 3

    def __str__(self) -> str:
        match self:
            case ClientServerType.HTTP:
                return "HTTP"
            case ClientServerType.IP_ID:
                return "IP ID"
            case ClientServerType.TCP_PORT:
                return "TCP Port"
            case ClientServerType.UDP_PORT:
                return "UDP Port"

if __name__ == "__main__":
    pass
