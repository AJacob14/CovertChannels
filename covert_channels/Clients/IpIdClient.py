"""
    This module is responsible for sending data covertly using the IP ID field. The data being sent is encoded as the
    ID field of the IP header.
"""

from __future__ import annotations

from enum import IntEnum

from scapy.all import *
from scapy.layers.inet import IP, UDP

from covert_channels.Clients.Client import Client


class ConnectionState(IntEnum):
    """
        Enum for the connection state.
    """
    START = 0
    SYN_SENT = 1
    ESTABLISHED = 2
    CLOSING = 3


class IpIdClient(Client):
    """
        A covert channel client that sends data through the IP ID field.
    """
    def __init__(self, target_ip: str, target_port: int):
        super().__init__(target_ip, target_port)

    def send(self, data: bytes):
        port = self._get_free_port()
        data_len = len(data)
        if data_len % 2 != 0:
            data += b"\x00"
            data_len += 1
        udp = UDP(sport=port, dport=self.port)
        for i in range(0, data_len, 2):
            upper = data[i] << 8
            lower = data[i + 1]
            ip = IP(dst=self.ip, id=(upper | lower))
            raw = Raw(self.generate_random_string(10).encode())
            packet = ip / udp / raw
            print(packet)
            send(packet)
        udp = UDP(dport=self.port, sport=self.port)
        packet = ip / udp / Raw(load=self.generate_random_string(10))
        print(packet)
        send(packet)


if __name__ == "__main__":
    pass
