from __future__ import annotations

import sys

from scapy.all import *
from scapy.layers.inet import IP, TCP

from Servers.Server import Server

class TcpPortServer(Server):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port, socket.SOCK_STREAM)
    
    def server_config(self):
        self.server.listen()

    def accept(self) -> bytes:
        addr: str
        conn, addr = self.server.accept()
        conn.close()
        return addr.encode()
        #return self.server.recv(65535)
    
    def receive(self) -> bytes:
        buffer = bytearray()
        while True:
            print("Waiting for packet...")
            packet = self._received_data.get()
            print("Packet received!")
            print(packet)
            # packet_base = IP(packet)
            # layers: list[Packet] = list(self.expand(packet_base))
            # tcp: TCP = layers[1]
            # if tcp.dport != self.port:
            #     continue
            # if tcp.sport == self.port:
            #     break
            # payload = layers[1].sport.to_bytes(2, byteorder=sys.byteorder)
            # buffer += payload
        
        return buffer

if __name__ == "__main__":
    pass
