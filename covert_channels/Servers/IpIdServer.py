"""
    This module is responsible for receiving data covertly using the IP ID field. The data being sent is encoded as the
    ID field of the IP header.
"""

from __future__ import annotations

from scapy.all import *
from scapy.layers.inet import IP, UDP

from covert_channels.Servers.SocketServer import SocketServer


class IpIdServer(SocketServer):
    """
        A covert channel server that receives data through the IP ID field.
    """

    def __init__(self, ip: str, port: int):
        super().__init__(ip, port, socket.SOCK_RAW)
        self.connection: socket.socket = None
        self.address: tuple[str, int] = ("", 0)

    def accept(self) -> bytes:
        return self.server.recv(65535)

    def receive(self) -> bytes:
        dummy = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to the port to prevent the OS from sending an ICMP port unreachable packet
        dummy.bind((self.ip, self.port))
        buffer = bytearray()
        while True:
            packet_bytes = self._received_data.get()
            packet_base = IP(packet_bytes)
            layers: list[Packet] = list(self._expand(packet_base))
            udp: UDP = layers[1]
            if udp.dport != self.port:
                continue
            if udp.sport == self.port:
                break
            sent_bytes = layers[0].id.to_bytes(2, byteorder='big')
            buffer += sent_bytes
        dummy.close()
        return bytes(buffer)


if __name__ == "__main__":
    pass
