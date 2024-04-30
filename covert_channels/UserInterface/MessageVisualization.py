#from scapy.all import IP
from scapy.layers.inet import IP

def visualize_ip(msg: bytes) -> list[str]:
    """
        Visualizes the IP message in a list of strings.
    :param msg: Message to visualize
    :return: List of strings representing the message
    """
    if len(msg) % 2 != 0:
        msg += b"\x00"
    headers = []
    for i in range(0, len(msg), 2):
        id_ = int.from_bytes(msg[i:i + 2], "big")
        header = print_ip_header(id_)
        headers.append(header)
    return headers

def print_ip_header(id_: int) -> str:
    """
        Prints the IP header.
    :param port: Port to visualize
    :return: String representation of the IP header
    """
    header =   "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|   4   |   5   |       0       |              38               |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header += f"|{id_:>20}           | 000 |         0               |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|      64       |      17       |             xxxxxxx           |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|                           127.0.0.1                           |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|                           127.0.0.1                           |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"

    return header

if __name__ == "__main__":
    print("This file is not meant to be run directly.")