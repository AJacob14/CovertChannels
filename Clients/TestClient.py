from __future__ import annotations

from scapy.all import *
from scapy.layers.inet import IP, TCP

from Clients.Client import Client

class TestClient(Client):
    def __init__(self, target_ip: str, target_port: int):
        super().__init__(target_ip, target_port)

    def send_packet(self):
        packet = IP(dst=self.ip) / TCP(dport=self.port, sport=1)
        send(packet)