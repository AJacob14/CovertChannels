"""
    This module is responsible for receiving data covertly using the TCP source port number. The data being received is
    decoded from the source port number of the TCP header.
"""

from __future__ import annotations

from scapy.all import *
from scapy.layers.inet import IP, TCP

from covert_channels.Servers.SocketServer import SocketServer


class TcpPortServer(SocketServer):
    """
        A covert channel server that receives data through the TCP source port number.
    """
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port, socket.SOCK_RAW)

    def accept(self) -> bytes:
        return self.server.recv(65535)

    def receive(self) -> bytes:
        buffer = bytearray()
        while True:
            print("Waiting for packet...")
            packet_bytes = self._received_data.get()
            print("Packet received!")
            packet_base = IP(packet_bytes)
            layers: list[Packet] = list(self._expand(packet_base))
            tcp: TCP = layers[1]
            if tcp.dport != self.port:
                continue
            if tcp.sport == self.port:
                break
            payload = layers[1].sport.to_bytes(2, byteorder=sys.byteorder)
            buffer += payload

        return buffer


if __name__ == "__main__":
    pass
