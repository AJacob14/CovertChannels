from __future__ import annotations

from Servers.Server import Server

class TestServer(Server):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)
    
    def accept(self) -> bytes:
        return self.server.recv(65535)