#!/usr/bin/env python3
import protocol
import socket
import threading


COMMAND_LIST = '''List of commands:
JOIN <username> - registration
TEXT <message> - broadcast
LIST - list of online users
QUIT - exit'''


class Client:
    def _listen(self, sock: socket.socket) -> None:
        while True:
            message = protocol.recv_message(sock)

            if message is None:
                break

            command, payload = message
            text = payload.decode(errors="replace").strip()

            print(text)

    def start(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 10000))

        try:
            listener_thread = threading.Thread(
                target=self._listen,
                args=(sock,)
            )
            listener_thread.start()

            print(COMMAND_LIST)
            print()

            while True:
                message = input().strip()

                if not message:
                    continue

                parts = message.split(maxsplit=1)
                command = parts[0].upper()
                payload = parts[1].encode() if len(parts) == 2 else b""

                protocol.send_message(sock, command, payload)

        except BrokenPipeError:
            print("Server socket closed.")

        except ConnectionResetError:
            print("Server socket closed unexpectedly.")

        except OSError:
            print("Server socket error.")

        except KeyboardInterrupt:
            pass

        finally:
            sock.close()

            listener_thread.join()


def main() -> None:
    client = Client()
    client.start()


if __name__ == "__main__":
    main()