#!/usr/bin/env python3
import threading
import socket
import protocol


class Server:
    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._client_threads: list[threading.Thread] = []

        self._online_usernames: dict[socket.socket, str] = {}

    def _broadcast(
            self,
            message: str,
            exclude: socket.socket | None = None,
        ) -> None:
            encoded_message = message.encode()

            with self._lock:
                recipients = list(self._online_usernames.keys())

            for recipient in recipients:
                if recipient is exclude:
                    continue

                try:
                    protocol.send_message(
                        recipient,
                        "INFO",
                        encoded_message,
                    )

                except BrokenPipeError:
                    print("Client socket closed.")

                except ConnectionResetError:
                    print("Client socket closed unexpectedly.")

                except OSError:
                    print("Client socket error.")   

    def _on_join(self, conn: socket.socket, username: str) -> None:
        with self._lock:
            self._online_usernames[conn] = username

        protocol.send_message(
            conn,
            "INFO",
            f"[SERVER] Welcome, {username}!".encode(),
        )

        self._broadcast(f"[SERVER] {username} logged in.", conn)

    def _on_text(self, conn: socket.socket, message: str) -> None:
        with self._lock:
            username = self._online_usernames.get(conn, None)

        if username is None:
            protocol.send_message(
                conn,
                "INFO",
                b"[SERVER] Send JOIN <username>.",
            )
        else:
            self._broadcast(f"[{username}] {message}")

    def _on_list(self, conn: socket.socket) -> None:
        with self._lock:
            online_usernames = "\n".join(list(self._online_usernames.values()))

        protocol.send_message(
            conn,
            "INFO",
            f"[SERVER] Online users:\n{online_usernames}".encode(),
        )

    def _handle_client(self, conn: socket.socket, addr) -> None:
        try:
            while True:
                message = protocol.recv_message(conn)

                if message is None:
                    break

                command, payload = message
                text = payload.decode().strip()

                match command:
                    case "JOIN":
                        self._on_join(conn, text)
                    
                    case "TEXT":
                        self._on_text(conn, text)
                    
                    case "LIST":
                        self._on_list(conn)
                    
                    case "QUIT":
                        break

                    case _:
                        protocol.send_message(
                            conn,
                            "INFO",
                            b"[SERVER] Unknown command."
                        )

        except BrokenPipeError:
            print("Client socket closed.")

        except ConnectionResetError:
            print("Client socket closed unexpectedly.")

        except OSError:
            print("Client socket error.")

        finally:
            try:
                conn.close()

            except OSError:
                print("Client socket error.")

            with self._lock:
                username = self._online_usernames.pop(conn, None)

            if username is not None:
                self._broadcast(f"[SERVER] {username} logged out.")

            with self._lock:
                try:
                    self._client_threads.remove(threading.current_thread())
                
                except ValueError:
                    print("The current thread has already finished executing.")

    def start(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 10000))
        sock.listen()
        sock.settimeout(1.0)

        try:
            while True:
                try:
                    conn, addr = sock.accept()

                except socket.timeout:
                    continue

                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                )

                with self._lock:
                    self._client_threads.append(client_thread)

                client_thread.start()

        except KeyboardInterrupt:
            pass

        finally:
            sock.close()

            with self._lock:
                last_client_threads = self._client_threads.copy()

            for client_thread in last_client_threads:
                client_thread.join()


def main() -> None:
    server = Server()
    server.start()


if __name__ == "__main__":
    main()