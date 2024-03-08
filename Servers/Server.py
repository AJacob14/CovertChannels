from __future__ import annotations

import socket
from queue import Queue
from typing import Iterator
from threading import Thread
from abc import ABC, abstractmethod

from scapy.packet import Packet

class Server(ABC):
    def __init__(self, ip: str, port: int, type: int):
        self.ip: str = ip
        self.port: int = port
        self.type: int = type
        self.server: socket.socket = None
        self.__server_started: bool = False
        self.__server_thread: Thread = None
        self._received_data: Queue[bytes] = Queue()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if not self.__server_started:
            self.stop()

    def start(self):
        self.__server_thread = Thread(target=self.server_start, daemon=True)
        self.__server_thread.start()
    
    def server_start(self):
        print("Starting server...")
        self.server = socket.socket(socket.AF_INET, self.type)
        self.server.bind((self.ip, self.port))
        self.server_config()
        self.__server_started = True
        print("Server started!")
        self.accept_loop()

    def server_config(self):
        self.server.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    def stop(self):
        self.__server_started = False
    
    @abstractmethod
    def accept(self) -> bytes:
        raise NotImplementedError

    def accept_loop(self):
        try:
            print("Waiting for data...")
            while self.__server_started:
                data = self.accept()
                #print("Data received!")
                self._received_data.put(data)
        except Exception as e:
            print(e)
            self.__server_started = False

    @staticmethod
    def expand(packet: Packet) -> Iterator[Packet]:
        yield packet
        while packet.payload:
            packet = packet.payload
            yield packet

if __name__ == "__name__":
    pass
