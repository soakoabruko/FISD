#!/usr/bin/env python3
import socket
import threading
import protocol as proto


HOST = "127.0.0.1"
PORT = 5555


def listen_loop(sock: socket.socket, stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        try:
            message = proto.recv_message(sock)
        
        except (ConnectionResetError, OSError):
            message = None

        if message is None:
            print("\n[!] соединение с сервером потеряно")
            stop_event.set()
            break

        command, payload = message
        text = payload.decode("utf-8", errors="replace")

        if command == "LIST":
            print(f"\n[задачи]{text}\n> ", end="")

        elif command == "ERRO":
            print(f"\n[ошибка] {text}\n> ", end="")

        else:
            print(f"\n* {text}\n> ", end="")


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    
    except (ConnectionRefusedError, OSError) as e:
        print(f"не удалось подключиться: {e}")
        return

    stop_event = threading.Event()
    threading.Thread(
        target=listen_loop,
        args=(sock, stop_event),
        daemon=True,
    ).start()

    try:
        while not stop_event.is_set():
            line = input()

            if line.startswith("/add "):
                c, text = line.split(maxsplit=1)
                proto.send_message(sock, "ADD", text.encode())

            elif line == "/list":
                proto.send_message(sock, "LIST")

            elif line.startswith("/done "):
                c, number = line.split(maxsplit=1)
                proto.send_message(sock, "DONE", number.encode())

            elif line.startswith("/delete"):
                c, number = line.split(maxsplit=1)
                proto.send_message(sock, "DELT", number.encode())

            elif line == "/quit":
                proto.send_message(sock, "QUIT")

            else:
                print(f"\n[ошибка] неизвестная команда: «{line}»\n> ", end="")
    
    except (EOFError, KeyboardInterrupt, BrokenPipeError, OSError):
        pass

    finally:
        stop_event.set()
        sock.close()


if __name__ == "__main__":
    main()