#!/usr/bin/env python3
import json
import struct


HOST = "127.0.0.1"
PORT = 50505


class NetCom:
    def __init__(self, sock):
        self.sock = sock

    @staticmethod
    def _recv_exact(sock, size):
        chunks = []
        received = 0

        while received < size:
            chunk = sock.recv(size - received)

            if not chunk:
                return None
            
            chunks.append(chunk)
            received += len(chunk)
        
        return b"".join(chunks)

    def recv(self):
        header = self._recv_exact(self.sock, 4)

        if header is None:
            return None

        payload_size = struct.unpack("!I", header)[0]
        payload = self._recv_exact(self.sock, payload_size)

        if payload is None:
            return None

        return json.loads(payload.decode("utf-8"))

    def send(self, message):
        payload = json.dumps(message, ensure_ascii=False).encode("utf-8")
        header = struct.pack("!I", len(payload))
        self.sock.sendall(header + payload)