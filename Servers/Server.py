from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue


class Server(ABC):
    """
        Base class for all covert channel servers
    """

    def __init__(self, ip: str, port: int):
        self.ip: str = ip
        self.port: int = port
        self._server_started: bool = False
        self._received_data: Queue[bytes] = Queue()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._server_started:
            self.stop()

    @abstractmethod
    def start(self):
        """
            Start server thread which listens for incoming packets
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """
            Signal to stop server
        """
        raise NotImplementedError

    @abstractmethod
    def accept(self) -> bytes:
        """
            Accept incoming packet data
        :return: bytes data of interest extracted from the received packet
        """
        raise NotImplementedError

    @abstractmethod
    def receive(self) -> bytes:
        """
            Receive incoming data by extracting and reconstructing the data from the received packets
        :return: covertly transmitted data
        """
        raise NotImplementedError


if __name__ == "__name__":
    pass
