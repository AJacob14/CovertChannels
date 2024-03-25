from __future__ import annotations

import socket

from scapy.all import *
from scapy.layers.inet import IP, UDP

from covert_channels.Servers.SocketServer import SocketServer


class UdpPortServer(SocketServer):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port, socket.SOCK_RAW)

    def accept(self) -> bytes:
        return self.server.recv(65535)

    def receive(self) -> bytes:
        dummy = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to the port to prevent the OS from sending an ICMP port unreachable packet
        dummy.bind((self.ip, self.port))
        buffer = bytearray()
        while True:
            print("Waiting for packet...")
            packet_bytes = self._received_data.get()
            print("Packet received!")
            packet_base = IP(packet_bytes)
            layers: list[Packet] = list(self._expand(packet_base))
            udp: UDP = layers[1]
            if udp.dport != self.port:
                continue
            if udp.sport == self.port:
                break
            payload = layers[1].sport.to_bytes(2, byteorder=sys.byteorder)
            buffer += payload

        dummy.close()  # Close the dummy socket
        return buffer


if __name__ == "__main__":
    pass
