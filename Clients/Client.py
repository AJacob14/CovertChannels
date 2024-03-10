from __future__ import annotations

import time
import random
from abc import ABC, abstractmethod


class Client(ABC):
    def __init__(self, target_ip: str, target_port: int):
        self.ip: str = target_ip
        self.port: int = target_port
        self.base_wait: float = 0.1
        self.jitter: float = 0.1

    @abstractmethod
    def send(self, data: bytes):
        raise NotImplementedError

    def wait(self):
        time.sleep(self.base_wait + (self.jitter * random.random()))


if __name__ == "__main__":
    pass
