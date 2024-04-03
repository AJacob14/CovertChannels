from __future__ import annotations

import argparse
import json
import os
import sys
import threading
from datetime import datetime
from queue import Queue
from threading import Timer
from typing import Callable

import requests
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QFont, QTextCursor, QColor, QScreen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout, QPushButton, QHBoxLayout, QTabWidget, \
    QTextEdit, QTableWidget, QTableWidgetItem, QLabel, QCheckBox, QFileDialog, QComboBox, QMessageBox, \
    QTextBrowser
from qt_material import apply_stylesheet

from covert_channels.UserInterface import ClientServer, ClientServerType, Config
from covert_channels.Clients import Client, HttpClient, IpIdClient, TcpPortClient, UdpPortClient
from covert_channels.Servers import Server, HttpServer, IpIdServer, TcpPortServer, UdpPortServer

def create_button(label: str, width: int = 150, height: int = 25) -> QPushButton:
    btn = QPushButton(label)
    btn.setFont(QFont("Arial", 12))
    btn.setFixedWidth(width)
    btn.setFixedHeight(height)
    return btn

class CovertChannelGui(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # region Instance Variables

        self.title: str = "Covert Channels"
        self.version: str = "v1.0.0"
        self.ip: str = ""
        self.port: int = 0
        self.client_server: ClientServer = None
        self.config: Config = Config()

        # endregion

        # region GUI Positioning

        self.setGeometry(0, 0, 768, 432)

        qt_rectangle = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # endregion

        # region GUI Construction

        hbox = QHBoxLayout()
        self.message_box = QLineEdit()
        self.message_box.setPlaceholderText("Enter message to send")
        self.message_box.setFont(QFont("Arial", 12))
        self.message_box.setFixedWidth(250)
        self.message_box.setFixedHeight(25)
        message_btn = create_button("Send Message")
        self.channel_control_btn = create_button("Start")
        self.channel_control_btn.clicked.connect(self.toggle_channel_active)
        hbox.addWidget(self.message_box)
        hbox.addWidget(message_btn)
        hbox.addWidget(self.channel_control_btn)

        form_layout = QFormLayout()
        form_layout.addRow(hbox)
        self.setLayout(form_layout)
        self.setWindowTitle(f"{self.title} {self.version}")

        # endregion

        self.initialize()

    @property
    def active(self) -> bool:
        return self.client_server is not None and self.client_server.active

    @active.setter
    def active(self, value: bool):
        if self.client_server is not None:
            self.client_server.active = value

    def closeEvent(self, a0: QtGui.QCloseEvent | None):
        if self.active:
            self.stop_channel()
        
        self.config.save_config()
        
        return super().closeEvent(a0)

    def initialize(self):
        self.ip = self.config.ip
        self.port = self.config.port
        self.client_server = ClientServer(self.ip, self.port, self.config.type)
    
    @staticmethod
    def get_default_config() -> dict:
        return {
            "ip": "127.0.0.1",
            "port": 42069,
            "type": ClientServerType.HTTP
        }

    def toggle_channel_active(self):
        if self.active:
            self.stop_channel()
            self.channel_control_btn.setText("Start")
            self.active = False
            print("Channel stopped")
        else:
            self.start_channel()
            self.channel_control_btn.setText("Stop")
            self.active = True
            print("Channel started")
    
    def start_channel(self):
        if self.active:
            return
        
        # TODO: Implement logic to start channel

    def stop_channel(self):
        if not self.active:
            return
        
        # TODO: Implement logic to stop channel

def run_gui():
    app = QApplication(sys.argv)
    window = CovertChannelGui()

    apply_stylesheet(app, theme="light_cyan.xml")

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()