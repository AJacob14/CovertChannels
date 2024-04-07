"""
    This module is responsible for sending data covertly using the IP ID field. The data being sent is encoded as the
    ID field of the IP header.
"""

from __future__ import annotations

from enum import IntEnum

from scapy.all import *
from scapy.layers.inet import IP, TCP

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
        dummy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dummy.bind(("localhost", port))
        sock = StreamSocket(dummy)
        data_len = len(data)
        # Pad the data if it is not an even number of bytes
        if data_len % 2 != 0:
            data += b"\x00"
            data_len += 1
        for i in range(0, data_len, 2):
            val = self._get_short(data, i)
            ip = IP(dst=self.ip, id=val)
            tcp = TCP(sport=port, dport=self.port)
            packet = ip / tcp
            print(packet)
            sock.send(packet)
        sock.close()

    # Work in progress implementation for manually handling the TCP handshake
    def send2(self, data: bytes):
        port = self._get_free_port()
        dummy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dummy.bind(("0.0.0.0", port))
        data_len = len(data)
        state: ConnectionState = ConnectionState.START
        seq = random.randint(0, 2 ** 32 - 1)
        ack = 0
        if data_len % 2 != 0:
            data += b"\x00"
            data_len += 1
        for i in range(0, data_len, 2):
            match state:
                case ConnectionState.START:
                    flag = "S"
                    state = ConnectionState.SYN_SENT
                case ConnectionState.SYN_SENT:
                    flag = "A"
                    state = ConnectionState.ESTABLISHED
                case ConnectionState.ESTABLISHED:
                    flag = ""
                case ConnectionState.CLOSING:
                    flag = "F"

            upper = data[i] << 8
            lower = data[i + 1]
            if state == ConnectionState.SYN_SENT:
                ip = IP(dst=self.ip, id=(upper | lower))
                tcp = TCP(sport=port, dport=self.port, flags=flag)
            else:
                ip = IP(dst=self.ip)
                tcp = TCP(sport=port, dport=self.port, flags=flag, seq=seq, ack=ack)
            packet = ip / tcp
            print(packet)
            syn_ack = sr1(packet)
            print(syn_ack)
            if state == ConnectionState.SYN_SENT:
                seq = syn_ack.ack
                ack = syn_ack.seq + 1
            else:
                pass
            if state == ConnectionState.ESTABLISHED:
                self.wait()

        dummy.close()


if __name__ == "__main__":
    pass
