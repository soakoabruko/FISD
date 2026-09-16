#!/usr/bin/env python3
import socket
import protocol
import threading
                    

def handle_client(conn: socket.socket, addr: tuple) -> None:
    try:
        while True:
            message = protocol.recv_message(conn)

            if message is None:
                break

            command, payload = message

            match command:
                case "JOIN":
                    active_conn[conn] = payload.decode("utf-8").strip()

                case "TEXT":
                    for other_conn in active_conn:
                        if other_conn == conn:
                            continue

                        other_conn.sendall(f"{active_conn[conn]}: ".encode("utf-8") + payload)

                case "LIST":
                    conn.sendall(f"{list(active_conn.values())}".encode("utf-8"))

                case "QUIT":
                    break

                case _:
                    conn.sendall("ERROR: unknown command".encode("utf-8"))
    finally:
        removed_username = active_conn.pop(conn)
        conn.sendall(f"{removed_username} was deleted")
        conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 10000))

active_conn: dict[socket.socket, str] = {}

s.listen()

try:
    while True:
        conn, addr = s.accept()
        t = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True,
        )
        t.start()
finally:
    s.close()