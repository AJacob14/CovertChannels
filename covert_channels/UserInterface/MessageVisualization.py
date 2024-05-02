HTTP_ENDPOINTS: list[str] = ["info", "stats", "home", "story", "privileges", "profile", "details", "department", 
                             "schedule", "vacation", "group", "information", "status", "data", "reports", "messages"]

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
        Creates a string representations of the IP header.
    :param id_: Id of the IP header
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

def visualize_tcp(msg: bytes) -> list[str]:
    """
        Visualizes the TCP message in a list of strings.
    :param msg: Message to visualize
    :return: List of strings representing the message
    """
    headers = []
    for i in range(0, len(msg), 2):
        port = int.from_bytes(msg[i:i + 2], "big")
        header = print_tcp_header(port)
        headers.append(header)
    return headers

def print_tcp_header(port: int) -> str:
    """
        Creates a string representations of the TCP header.
    :param port: Source port of the TCP header
    :return: String representation of the TCP header
    """
    header =   "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header += f"|{port:>17}              |             31337             |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|                             Seq #                             |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|                             Ack #                             |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|   5   |   0   |      SYN      |              8192             |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|            xxxxxxx            |               0               |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    return header

def visualize_udp(msg: bytes):
    """
        Visualizes the UDP message in a list of strings.
    :param msg: Source port of the UDP header
    :return: List of strings representing the message
    """
    headers = []
    for i in range(0, len(msg), 2):
        port = int.from_bytes(msg[i:i + 2], "big")
        header = print_udp_header(port)
        headers.append(header)
    return headers

def print_udp_header(port: int) -> str:
    """
        Creates a string representations of the UDP header.
    :param port: Port to visualize
    :return: String representation of the UDP header
    """
    header =   "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header += f"|{port:>17}              |             31337             |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    header +=  "|               8               |            xxxxxxx            |\n"
    header +=  "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
    return header

def visualize_http(msg: bytes):
    """
        Visualizes the HTTP message in a list of strings.
    :param msg: Message to visualize
    :return: List of strings representing the message
    """
    requests = []
    requests.append("POST /login HTTP/1.1")
    for b in msg:
        for i in range(2):
            nibble = (b >> (4 * i)) & 0x0F
            request = HTTP_ENDPOINTS[nibble]
            requests.append(f"GET /{request} HTTP/1.1")
    requests.append("POST /logout HTTP/1.1")
    return requests

if __name__ == "__main__":
    # message = b"Hello, World!"
    # headers = visualize_tcp(message)
    # for header in headers:
    #     print(header)
    print("This file is not meant to be run directly.")