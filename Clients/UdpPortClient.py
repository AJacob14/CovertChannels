from __future__ import annotations

from scapy.all import *
from scapy.layers.inet import IP, UDP

from Clients.Client import Client

class UdpPortClient(Client):
    def __init__(self, target_ip: str, target_port: int):
        super().__init__(target_ip, target_port)

    def send(self, data: bytes):
        ip = IP(dst=self.ip)
        if len(data) % 2 != 0:
            data += b'\x00' # Padding
        for i in range(0, len(data), 2):
            val = int.from_bytes(data[i:i+2], byteorder=sys.byteorder)
            if val < 1024:
                print("Potential risk of using a low port!")
            udp = UDP(dport=self.port, sport=val)
            packet = ip / udp / Raw(load="----")
            print(packet)
            send(packet)
            self.wait()
        udp = UDP(dport=self.port, sport=self.port)
        packet = ip / udp / Raw(load="----")
        print(packet)
        send(packet)

if __name__ == "__main__":
    pass
