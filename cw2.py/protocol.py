#!/usr/bin/env python3
import socket
import struct


MAX_MESSAGE_SIZE = 10 * 1024 * 1024


def rect_exact(sock: socket.socket, size: int) -> bytes:
    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection closed before all data was received")

        data.extend(chunk)

    return bytes(data)


def send_message(sock: socket.socket, command: str, payload: bytes) -> None:
    command_bytes = command.encode("utf-8")
    length = len(payload)
    header = struct.pack("!4sI", command_bytes, length)
    sock.sendall(header + payload)


def recv_message(sock: socket.socket) -> tuple[str, bytes] | None:
    try:
        header = rect_exact(sock, 8)

        command_bytes, length = struct.unpack("!4sI", header)
        command = command_bytes.decode("utf-8").strip()

        if length > MAX_MESSAGE_SIZE:
            payload = rect_exact(sock, MAX_MESSAGE_SIZE)
        else:
            payload = rect_exact(sock, length)

        return command, payload
    except ConnectionError:
        return None