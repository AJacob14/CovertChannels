from __future__ import annotations

import sys

from scapy.all import *
from scapy.layers.inet import IP, TCP

from covert_channels.Clients.Client import Client

class TcpPortClient(Client):
    """
        A covert channel client that sends data through the TCP source port number.

        This client is not very stealthy, as after it sends the SYN packet and the 
        server responds with a SYN-ACK packet, the OS will send an RST packet to
        close the connection before the client can send an ACK packet. This is because 
        the OS is not expecting a response from the server, so it closes the connection. 
        This leads to RST packets being sent to the server, which is very obvious and 
        unusual in packet captures (shows as red in Wireshark).
    """
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
            tcp = TCP(dport=self.port, sport=val)
            packet = ip / tcp
            print(packet)
            send(packet)
            self.wait()
        tcp = TCP(dport=self.port, sport=self.port)
        packet = ip / tcp
        print(packet)
        send(packet)

if __name__ == "__main__":
    pass
