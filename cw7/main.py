#!/usr/bin/env python3
from queue import Queue
import socket
import sys

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import netcom


class ReceiveThread(QThread):
    message_received = pyqtSignal(dict)
    connection_lost = pyqtSignal()

    def __init__(self, net):
        super().__init__()
        self.net = net

    def run(self):
        while True:
            try:
                message = self.net.recv()
            except (ConnectionResetError, OSError):
                message = None

            if message is None:
                self.connection_lost.emit()
                break

            self.message_received.emit(message)


class SendThread(QThread):
    def __init__(self, net):
        super().__init__()
        self.net = net
        self.queue = Queue()

    def send(self, message):
        self.queue.put(message)

    def run(self):
        while True:
            message = self.queue.get()

            if message is None:
                break

            try:
                self.net.send(message)
            except (BrokenPipeError, OSError):
                break

    def stop(self):
        self.queue.put(None)


class MainWindow(QMainWindow):
    def __init__(self, net):
        super().__init__()
        self.net = net

        self.setWindowTitle("PyQt6 network chat")
        self.resize(560, 420)

        self.status = QLabel("Connected to 127.0.0.1:50505")

        self.history = QTextEdit()
        self.history.setReadOnly(True)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.history.clear())

        self.username = QLineEdit()
        self.username.setPlaceholderText("Type a username…")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a message…")
        self.input.returnPressed.connect(self.on_send_clicked)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.on_send_clicked)

        input_row = QHBoxLayout()
        input_row.addWidget(self.input)
        input_row.addWidget(send_button)

        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.history)
        layout.addWidget(clear_button)
        layout.addWidget(self.username)
        layout.addLayout(input_row)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.receive_thread = ReceiveThread(self.net)
        self.receive_thread.message_received.connect(self.handle_message)
        self.receive_thread.connection_lost.connect(self.on_connection_lost)
        self.receive_thread.start()

        self.send_thread = SendThread(self.net)
        self.send_thread.start()

    def on_send_clicked(self):
        username = self.username.text().strip()

        if not username:
            return

        text = self.input.text().strip()

        if not text:
            return

        self.send_thread.send({
            "type": "chat",
            "username": username,
            "text": text,
        })

        self.input.clear()

    def handle_message(self, message):
        if message.get("type") == "chat":
            username = message.get("username", "Anonymous")
            text = message.get("text", "")
            self.history.append(f"{username}: {text}")
        elif message.get("type") == "system":
            text = message.get("text", "")
            self.history.append(f"[System] {text}")

    def on_connection_lost(self):
        self.status.setText("Disconnected to 127.0.0.1:50505")

        QMessageBox.critical(
            self,
            "Error",
            "Connection to the server has been lost",
            QMessageBox.StandardButton.Ok,
        )

    def closeEvent(self, event):
        self.send_thread.stop()
        self.send_thread.wait()

        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((netcom.HOST, netcom.PORT))
    except OSError as exc:
        print(f"Could not connect to server at {netcom.HOST}:{netcom.PORT}: {exc}")
        print("Run server.py first, then start main.py.")
        return

    net = netcom.NetCom(sock)
    window = MainWindow(net)
    window.show()

    exit_code = app.exec()

    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except OSError:
        pass

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()