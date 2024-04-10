from __future__ import annotations

import errno
import random
import socket
import string
import threading
import time
from abc import ABC, abstractmethod
from typing import Iterator

from pydivert import WinDivert
from scapy.packet import Packet


class Client(ABC):
    """
        Abstract class for a covert channel client that sends data to a server.
    """

    def __init__(self, target_ip: str, target_port: int):
        """
            Initialize the client with the target IP and port.
        :param target_ip: Ip address of the covert channel server
        :param target_port: Port of the covert channel server
        """
        self.ip: str = target_ip
        self.port: int = target_port
        self.base_wait: float = 0.1
        self.jitter: float = 0.1
        self.__droppping_rst_packets: bool = False

    @abstractmethod
    def send(self, data: bytes):
        """
            Send data to the server
        :param data: Bytes to covertly send
        """
        raise NotImplementedError

    def wait(self):
        """
            Wait for a random amount of time
        """
        time.sleep(self.base_wait + (self.jitter * random.random()))

    @staticmethod
    def _get_free_port() -> int:
        """
            Get a free port to use for sending data. This avoids other processes receiving the
            response to the transmitted packet. This implementation would not be used in a real world
            scenario as it generates noise by potentially binding to multiple ports and used ports.
        :return: A currently unused port number
        """
        port = random.randint(1024, 65535)
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("localhost", port))
                    break
                except socket.error as e:
                    if e.errno == errno.EADDRINUSE:
                        port = random.randint(1024, 65535)
                    else:
                        # something else raised the socket.error exception
                        raise
        return port

    @staticmethod
    def _expand(packet: Packet) -> Iterator[Packet]:
        """
            Expand packet into its payload components
        :param packet: base packet to expand
        :return: iterator of packets
        """
        yield packet
        while packet.payload:
            packet = packet.payload
            yield packet

    @staticmethod
    def generate_random_string(length: int) -> str:
        """
            Generate a random string of the given length
        :param length: Length of the string to generate
        :return: The randomly generated string
        """
        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choices(characters, k=length))
        return random_string

    @staticmethod
    def _get_short(data: bytes, offset: int) -> int:
        """
            Get a short from the data at the given offset
        :param data: Sequence of bytes to extract the short from
        :param offset: Offset to start extracting the short from
        :return: The short extracted from the data
        """
        higher = data[offset] << 8
        lower = data[offset + 1]
        return higher | lower

    def _drop_rst_packets(self):
        """
            Drop outgoing RST packets
        """
        with WinDivert("outbound and tcp.Rst") as w:
            for _ in w:
                # Drop the packet by not re-injecting it
                if not self.__droppping_rst_packets:
                    break
    
    def _start_dropping_rst_packets(self):
        """
            Start dropping outgoing RST packets
        """
        if self.__droppping_rst_packets:
            return
        self.__droppping_rst_packets = True
        thread = threading.Thread(target=self._drop_rst_packets)
        thread.start()
    
    def _stop_dropping_rst_packets(self):
        """
            Stop dropping outgoing RST packets
        """
        self.__droppping_rst_packets = False

if __name__ == "__main__":
    pass
