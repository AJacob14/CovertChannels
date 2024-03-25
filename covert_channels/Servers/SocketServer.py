from __future__ import annotations

import socket
from abc import ABC
from threading import Thread
from typing import Iterator

from scapy.packet import Packet
from pydivert import WinDivert

from covert_channels.Servers.Server import Server


class SocketServer(Server, ABC):
    def __init__(self, ip: str, port: int, type_: int):
        super().__init__(ip, port)
        self.type: int = type_
        self.server: socket.socket = None

    def _server_start(self):
        """
            Start and bind server socket. Also apply server configurations and start
            the accept loop.
        """
        print("Starting server...")
        self.server = socket.socket(socket.AF_INET, self.type)
        self.server.bind((self.ip, self.port))
        self._server_config()
        self._server_started = True
        print("Server started!")
        self.__accept_loop()

    def stop(self):
        self._server_started = False

    def _server_config(self):
        """
            Apply server configurations necessary to for the specific covert channel
        """
        self.server.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def __accept_loop(self):
        """
            Loop to accept incoming packets and put them in the received data queue
        """
        try:
            print("Waiting for data...")
            while self._server_started:
                data = self.accept()
                # print("Data received!")
                self._received_data.put(data)
            self.server.close()
        except Exception as e:
            print(e)
            self.server.close()
            self._server_started = False

    @staticmethod
    def _expand(packet: Packet) -> Iterator[Packet]:
        """
            Expand packet into its payload components
        :param packet: base packet to expand
        :return: iterator of packets
        """
        yield packet
        while packet.payload:
            packet = packet.payload
            yield packet

    def _drop_outbound_rst(self):
        with WinDivert("outbound and tcp.Rst") as w:
            for _ in w:
                if not self._server_started:
                    break   # This only works after the server is bound
                pass
                #print("Dropped a packet with RST flag")
                # The packet is dropped by not re-injecting it.

if __name__ == "__main__":
    pass
