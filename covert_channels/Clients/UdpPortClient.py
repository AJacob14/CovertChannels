"""
    This module is responsible for sending data covertly using the UDP source port number. The data being sent is
    encoded as the source port number of the UDP header.
"""

from __future__ import annotations

from scapy.all import *
from scapy.layers.inet import IP, UDP

from covert_channels.Clients.Client import Client


class UdpPortClient(Client):
    """
        A covert channel client that sends data through the UDP source port number.
    """
    def __init__(self, target_ip: str, target_port: int):
        super().__init__(target_ip, target_port)

    def send(self, data: bytes):
        ip = IP(dst=self.ip)
        if len(data) % 2 != 0:
            data += b'\x00'  # Padding
        for i in range(0, len(data), 2):
            val = int.from_bytes(data[i:i + 2], byteorder=sys.byteorder)
            # This can be avoided by using a more sophisticated encoding scheme
            if val < 1024:
                print("Potential risk of using a low port!")
            udp = UDP(dport=self.port, sport=val)
            packet = ip / udp / Raw(load=self.generate_random_string(10))
            print(packet)
            send(packet)
            self.wait()
        udp = UDP(dport=self.port, sport=self.port)
        packet = ip / udp / Raw(load=self.generate_random_string(10))
        print(packet)
        send(packet)


if __name__ == "__main__":
    pass
