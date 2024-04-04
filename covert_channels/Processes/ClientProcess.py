from __future__ import annotations

from multiprocessing import Process, Queue
from multiprocessing.connection import Client

from covert_channels.Clients import Client as CovertClient

class ClientProcess(Process):
    def __init__(self):
        self.client: CovertClient = None
        

if __name__ == "__main__":
    pass
