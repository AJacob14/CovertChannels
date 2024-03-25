from __future__ import annotations

import sys
import socket

from scapy.all import *
from scapy.layers.inet import IP, TCP

from covert_channels.Servers.SocketServer import SocketServer

class IpIdServer(SocketServer):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port, socket.SOCK_STREAM)
        self.connection: socket.socket = None
        self.address: tuple[str, int] = ("", 0)
    
    def _server_config(self):
        self.server.listen()

    def accept(self) -> bytes:
        if self.connection is None:
            self.connection, self.address = self.server.accept()
        return self.server.recv(4096)

    def receive(self) -> bytes:
        buffer = bytearray()
        while True:
            packet_bytes = self._received_data.get()
            packet_base = IP(packet_bytes)
            layers: list[Packet] = list(self._expand(packet_base))
            tcp: TCP = layers[1]
            if tcp.dport != self.port:
                continue
            if tcp.sport == self.port:
                break
            sent_bytes = layers[0].id.to_bytes(2, byteorder=sys.byteorder)
            buffer += sent_bytes
        return bytes(buffer)
    
if __name__ == "__main__":
    pass
