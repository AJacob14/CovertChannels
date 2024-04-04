import os
import json

from covert_channels.UserInterface import ClientServer, ClientServerType

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Config:
    CONFIG_PATH: str = "config.json"

    def __init__(self, metaclass=Singleton):
        self.ip: str = ""
        self.port: int = 0
        self.type: ClientServerType = 0

        self.__initalize()
    
    def __initalize(self):
        if os.path.exists(self.CONFIG_PATH):
            self.__load_config()
        else:
            self.__create_default_config()

    def __load_config(self):
        with open(self.CONFIG_PATH, "r") as file:
            config = json.load(file)
            self.ip = config["ip"]
            self.port = config["port"]
            self.type = ClientServerType(config["type"])

    def __create_default_config(self):
        self.ip = "127.0.0.1"
        self.port = 42069
        self.type = ClientServerType.HTTP
    
    def save_config(self):
        with open(self.CONFIG_PATH, "w") as file:
            json.dump({
                "ip": self.ip,
                "port": self.port,
                "type": self.type.value
            }, file)

if __name__ == "__main__":
    pass