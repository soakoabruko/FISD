import json
import socketserver
import threading

import netcom


class ChatHandler(socketserver.BaseRequestHandler):
    clients = set()
    clients_lock = threading.Lock()

    def handle(self):
        sock = self.request
        net = netcom.NetCom(sock)

        with self.clients_lock:
            self.clients.add(net)
        
        print(f"Client connected: {self.client_address}")

        try:
            while True:
                message = net.recv()

                if message is None:
                    break

                print("Received:", message)
                self.broadcast(message)
        except (ConnectionError, OSError, json.JSONDecodeError) as exc:
            print(f"Client error: {exc}")
        finally:
            with self.clients_lock:
                self.clients.discard(net)
            
            try:
                sock.close()
            except OSError:
                pass

            print(f"Client disconnected: {self.client_address}")

    @classmethod
    def broadcast(cls, message):
        with cls.clients_lock:
            clients = list(cls.clients)

        dead_clients = []

        for client in clients:
            try:
                client.send(message)
            except OSError:
                dead_clients.append(client)

        if dead_clients:
            with cls.clients_lock:
                for client in dead_clients:
                    cls.clients.discard(client)


class ThreadedChatServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with ThreadedChatServer((netcom.HOST, netcom.PORT), ChatHandler) as server:
        print(f"Chat server is running on {netcom.HOST}:{netcom.PORT}")
        print("Start main.py in one or more windows. Stop with Ctrl+C.")
        server.serve_forever()