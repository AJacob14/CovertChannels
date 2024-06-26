"""
    This is a test client for manually handling the TCP handshake through scapy. This script is for testing various
    methods for completing the TCP handshake without the OS sending a RST ACK response. This script is used for research
    purposes and is not used in the covert channel implementation.
"""

from __future__ import annotations

from pydivert import WinDivert
from scapy.all import *
from scapy.layers.inet import IP, TCP

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 31337
HOST = "0.0.0.0"
PORT = 31337


def main():
    random.seed(PORT)
    dummy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #dummy.connect((SERVER_HOST, SERVER_PORT))
    dummy.bind((HOST, PORT))
    dummy.listen()
    thread = Thread(target=drop_out_rst, daemon=True)
    thread.start()
    ip = IP(dst=SERVER_HOST, id=0)
    tcp = TCP(sport=PORT, dport=SERVER_PORT, flags="S", seq=random.randint(0, 2 ** 32 - 1), ack=0)
    packet = ip / tcp
    print(packet)
    resp = sr1(packet)
    print(resp)
    seq = resp[TCP].ack
    ack = resp[TCP].seq + 1
    ip = IP(dst=SERVER_HOST, id=1)
    tcp = TCP(sport=PORT, dport=SERVER_PORT, flags="A", seq=seq, ack=ack)
    packet = ip / tcp
    print(packet)
    resp = sr1(packet)
    print(resp)


def drop_out_rst():
    with WinDivert("outbound and tcp.Rst") as w:
        for _ in w:
            print("Dropped a packet with RST flag")
            # The packet is dropped by not re-injecting it.


if __name__ == "__main__":
    main()
