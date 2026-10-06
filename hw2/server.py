#!/usr/bin/env python3
from itertools import count
import threading
import socket
import protocol as proto


HOST = "0.0.0.0"
PORT = 5555

tasks = {}
task_id_count = count(1)

task_lock = threading.Lock()


def handle_client(sock: socket.socket, addr) -> None:
    try:
        print(f"[i] {addr} подключился")
        proto.send_message(sock, "TEXT", "добро пожаловать".encode())

        while True:
            message = proto.recv_message(sock)

            if message is None:
                print(f"[i] {addr} отключился без QUIT")
                break

            command, payload = message

            if command == "ADD":
                text = payload.decode(errors="replace")

                with task_lock:
                    new_task_id = next(task_id_count)
                    tasks[new_task_id] = {"text": text, "is_done": False}

                proto.send_message(sock, "TEXT", f"вы добавили задачу №{new_task_id}: «{text}»".encode())
                print(f"[+] {addr} добавил задачу: «{text}»")

            elif command == "LIST":
                with task_lock:
                    tasks_snapshot = tasks.copy()

                task_list = ""

                for task_id, task in tasks_snapshot.items():
                    task_list += f"\n{task_id}. [{"x" if task["is_done"] else " "}] {task["text"]}"
                
                proto.send_message(sock, "LIST", task_list.encode())

            elif command == "DONE":
                text = payload.decode(errors="replace")

                try:
                    task_id = int(text)

                except ValueError:
                    proto.send_message(sock, "ERRO", "неверный формат. Формат: «/done <number>»".encode())
                    continue

                if tasks.get(task_id) is None:
                    proto.send_message(sock, "ERRO", f"задача №{task_id} не существует. Список задач: «/list»".encode())
                
                else:
                    with task_lock:
                        tasks[task_id]["is_done"] = True

                    proto.send_message(sock, "TEXT", f"вы выполнили задачу №{task_id}".encode())
                    print(f"[~] {addr} выполнил задачу №{task_id}")

            elif command == "DELT":
                text = payload.decode(errors="replace")

                try:
                    task_id = int(text)

                except ValueError:
                    proto.send_message(sock, "ERRO", "неверный формат. Формат: «/delete <number>»".encode())
                    continue

                if tasks.get(task_id) is None:
                    proto.send_message(sock, "ERRO", f"задача №{task_id} не существует. Список задач: «/list»".encode())

                else:
                    with task_lock:
                        del tasks[task_id]

                    proto.send_message(sock, "TEXT", f"вы удалили задачу №{task_id}".encode())
                    print(f"[-] {addr} удалил задачу №{task_id}")

            elif command == "QUIT":
                proto.send_message(sock, "TEXT", "до свидания".encode())
                print(f"[i] {addr} вышел через QUIT")
                break
    
    except ConnectionResetError:
        print(f"[!] {addr} - соединение сброшено (RST)")
    
    except BrokenPipeError:
        print(f"[!] {addr} - не удалось отправить, соединение разорвано")
    
    finally:
        sock.close()


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[*] сервер слушает {HOST}:{PORT}")

        while True:
            client_sock, addr = server.accept()
            threading.Thread(
                target=handle_client,
                args=(client_sock, addr),
                daemon=True,
            ).start()


if __name__ == "__main__":
    try:
        main()
    
    except KeyboardInterrupt:
        print("\n[*] сервер остановлен")