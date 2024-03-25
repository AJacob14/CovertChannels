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

from UserInterface import ClientServer, ClientServerType
from Clients import Client, HttpClient, IpIdClient, TcpPortClient, UdpPortClient
from Servers import Server, HttpServer, IpIdServer, TcpPortServer, UdpPortServer

class CovertChannelGui(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # region Instance Variables

        self.title: str = "Covert Channels"
        self.version: str = "v1.0.0"
        self.client_server: ClientServer = None

        # endregion

        # region GUI Positioning

        self.setGeometry(0, 0, 768, 432)

        qt_rectangle = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # endregion

        # region GUI Construction



        form_layout = QFormLayout()
        self.setLayout(form_layout)
        self.setWindowTitle(f"{self.title} {self.version}")

        # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CovertChannelGui()

    win.show()
    sys.exit(app.exec())