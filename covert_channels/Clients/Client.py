from __future__ import annotations

import sys
import time
import errno
import socket
import random
import string
from typing import Iterator
from abc import ABC, abstractmethod

from scapy.packet import Packet


class Client(ABC):
    def __init__(self, target_ip: str, target_port: int):
        self.ip: str = target_ip
        self.port: int = target_port
        self.base_wait: float = 0.1
        self.jitter: float = 0.1

    @abstractmethod
    def send(self, data: bytes):
        raise NotImplementedError

    def wait(self):
        time.sleep(self.base_wait + (self.jitter * random.random()))

    def _get_free_port(self) -> int:
        """
            Get a free port to use for sending data. This avoid other processes receiving the 
            response to the sent packet. This implementation would not be used in a real world 
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
    def generate_random_string(length: int):
        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choices(characters, k=length))
        return random_string
    
    @staticmethod
    def _get_short(data: bytes, offset: int) -> int:
        higher = data[offset] << 8
        lower = data[offset + 1]
        return higher | lower
        #return int.from_bytes(data[offset:offset + 2], byteorder=sys.byteorder)

if __name__ == "__main__":
    pass
