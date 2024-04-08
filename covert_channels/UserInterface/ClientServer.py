"""
    This module handles managing the client and server processes.
"""

from __future__ import annotations

from enum import IntEnum
from multiprocessing import Process, Queue

from covert_channels.Clients import Client, HttpClient, IpIdClient, TcpPortClient, UdpPortClient
from covert_channels.Servers import Server, HttpServer, IpIdServer, TcpPortServer, UdpPortServer


class ClientServer:
    """
        This class manages the client and server processes.
    """
    def __init__(self, ip: str, port: int, type_: ClientServerType):
        """
            Constructor for the ClientServer class.
        :param ip: IP address of the server.
        :param port: Port number of the server.
        :param type_: Type of covert channel to use.
        """
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
        """
            Construct the client and server objects based on the type of covert channel.
        :param ip: IP address of the server.
        :param port: Port number of the server.
        :param type_: Type of covert channel to use.
        """
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
        """
            Start the client and server processes.
        """
        self.client_process = Process(target=ClientServer._client_process, args=(self.client_queue, self.client))
        self.server_process = Process(target=ClientServer._server_process, args=(self.server_queue, self.server))
        self.server_process.start()
        self.client_process.start()

    def stop(self):
        """
            Stop the client and server processes through forceful termination.
        """
        self.client_process.terminate()
        self.server_process.terminate()

    def send(self, data: bytes) -> bytes:
        """
            Send data to be transmitted to the client which will covertly send that data to the server. The server will
            then covertly receive that data and return it.
        :param data: Data to be transmitted covertly.
        :return: The data received covertly.
        """
        self.client_queue.put(data)     # Send data to client
        # Covert communication between client and server
        data = self.server_queue.get()  # Receive data from server
        return data

    @staticmethod
    def _client_process(queue: Queue, client: Client):
        """
            Process that handles the client's covert communication with the server.
        :param queue: IPC queue for communication between the main process and the client process.
        :param client: The client object that will be used to communicate covertly with the server.
        """
        while True:
            message = queue.get()           # Receive message from main process
            if isinstance(message, str):
                message = message.encode()  # Convert message to bytes
            client.send(message)            # Send message to server

    @staticmethod
    def _server_process(queue: Queue, server: Server):
        """
            Process that handles the server's covert communication with the client.
        :param queue: IPC queue for communication between the main process and the server process.
        :param server: The server object that will be used to communicate covertly with the client.
        """
        with server:
            while True:
                data = server.receive()    # Receive data from client
                queue.put(data)            # Send data to main process


class ClientServerType(IntEnum):
    """
        Enum class that represents the different types of covert channels that can be used.
    """
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
