import json
import os

from covert_channels.UserInterface import ClientServerType


class Singleton(type):
    """
        Singleton metaclass for the Config class to ensure only one instance is created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    CONFIG_PATH: str = "config.json"

    def __init__(self):
        """
            Constructor for the Config class.
        """
        self.ip: str = ""
        self.port: int = 0
        self.type: ClientServerType = ClientServerType.HTTP

        self.__initialize()

    def __initialize(self):
        """
            Initialize the configuration object with saved values or default values.
        """
        if os.path.exists(self.CONFIG_PATH):
            self.__load_config()
        else:
            self.__create_default_config()

    def __load_config(self):
        """
            Load the configuration from the config file.
        """
        with open(self.CONFIG_PATH, "r") as file:
            config = json.load(file)
            self.ip = config["ip"]
            self.port = config["port"]
            self.type = ClientServerType(config["type"])

    def __create_default_config(self):
        """
            Create a default configuration file by setting the default values.
        """
        self.ip = "127.0.0.1"
        self.port = 31337
        self.type = ClientServerType.HTTP

    def save_config(self):
        """
            Save the configuration to the config file.
        """
        with open(self.CONFIG_PATH, "w") as file:
            json.dump({
                "ip": self.ip,
                "port": self.port,
                "type": self.type.value
            }, file)


if __name__ == "__main__":
    pass
