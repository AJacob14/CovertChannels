from __future__ import annotations

import os
import signal
import time
from queue import Queue

import requests
from flask import Flask, request, jsonify

from Servers.Server import Server

app = Flask(__name__)

INTERNAL_QUEUE: Queue[bytes] = Queue()
RECEIVING: bool = False
DATA_READY: bool = False


class HttpServer(Server):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)
        global INTERNAL_QUEUE
        INTERNAL_QUEUE = self._received_data

    def _server_start(self):
        self._server_started = True
        app.run(debug=True, use_reloader=False, host=self.ip, port=self.port)

    def stop(self):
        requests.get(f"http://{self.ip}:{self.port}/shutdown")
        self._server_started = False

    def accept(self) -> bytes:
        pass

    def receive(self) -> bytes:
        buffer = bytearray()
        byte = 0
        lower = True
        global DATA_READY
        while not DATA_READY:
            time.sleep(0.1)
        while not INTERNAL_QUEUE.empty():
            data = INTERNAL_QUEUE.get()
            if lower:
                byte = data[0] & 0x0F
                lower = False
            else:
                byte |= (data[0] & 0x0F) << 4
                lower = True
                buffer.append(byte)
                #print(f"Received byte: {byte}")
        DATA_READY = False
        return bytes(buffer)


# region Flask Routes

@app.route("/shutdown", methods=["POST"])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"message": "Server shutting down..."}), 200


@app.route("/users/login", methods=["POST"])
def login():
    request_data = request.get_json()
    username = request_data.get("username")
    password = request_data.get("password")
    if username == "exfiltrate" and password == "data":
        global RECEIVING
        RECEIVING = True
        return jsonify({"message": "User logged in"}), 200

    return jsonify({"message": "User not found"}), 401


@app.route("/users/<action>", methods=["GET"])
def users(action: str):
    if not RECEIVING:
        return jsonify({"message": "User not logged in"}), 401
    match action:
        case "info":
            INTERNAL_QUEUE.put(b"\x00")
        case "stats":
            INTERNAL_QUEUE.put(b"\x01")
        case "home":
            INTERNAL_QUEUE.put(b"\x02")
        case "story":
            INTERNAL_QUEUE.put(b"\x03")
        case "privileges":
            INTERNAL_QUEUE.put(b"\x04")
        case "profile":
            INTERNAL_QUEUE.put(b"\x05")
        case "details":
            INTERNAL_QUEUE.put(b"\x06")
        case "department":
            INTERNAL_QUEUE.put(b"\x07")
        case "schedule":
            INTERNAL_QUEUE.put(b"\x08")
        case "vacation":
            INTERNAL_QUEUE.put(b"\x09")
        case "group":
            INTERNAL_QUEUE.put(b"\x0A")
        case "information":
            INTERNAL_QUEUE.put(b"\x0B")
        case "status":
            INTERNAL_QUEUE.put(b"\x0C")
        case "data":
            INTERNAL_QUEUE.put(b"\x0D")
        case "reports":
            INTERNAL_QUEUE.put(b"\x0E")
        case "messages":
            INTERNAL_QUEUE.put(b"\x0F")
        case _:
            return jsonify({"message": "Invalid action"}), 400
    return jsonify({"message": f"User {action}"}), 200


@app.route("/users/logout", methods=["POST"])
def user_logout():
    global RECEIVING, DATA_READY
    RECEIVING = False
    DATA_READY = True
    return jsonify({"message": "User logged out"}), 200


# endregion

if __name__ == "__main__":
    pass
