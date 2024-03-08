import socket
import threading
from dataclasses import dataclass


@dataclass
class Client:
    id: int
    name: str
    socket: socket.socket
    address: str


def handle_client(client: Client, clients: list[Client], pool: set[int]):
    client.socket.send(f"Connected. You are {client.name}.".encode("utf-8"))
    while True:
        try:
            message = client.socket.recv(1024).decode("utf-8")
            if not message:
                print(f"Client {client.name} disconnected")
                client.socket.close()
                clients.remove(client)
                pool.add(client.id)
                break
            else:
                print(f"Received message from {client.name}: {message}")
                for other in clients:
                    if other is client:
                        continue
                    other.socket.send(f"({client.name}): {message}".encode("utf-8"))

        except Exception as e:
            print(f"Error handling client: {client.name}. {e}")
            client.socket.close()
            clients.remove(client)
            pool.add(client.id)
            break


def server(addr=("", 9999), max_pool=2):
    server_socket = socket.create_server(addr, family=socket.AF_INET)
    clients: list[Client] = []
    pool = set(range(max_pool))

    print("Chat server is running...")

    while True:
        try:
            client_socket, client_address = server_socket.accept()

            print(f"New connection from {client_address}")
            if len(pool) == 0:
                client_socket.send(f"Connection rejected. Pool is empty.".encode("utf-8"))
                client_socket.close()
                print(f"Connection rejected. Pool is empty.")

            else:
                client = Client(id := pool.pop(), f"USER-{id}", client_socket, client_address)
                clients.append(client)

                client_thread = threading.Thread(target=handle_client, args=(client, clients, pool))
                client_thread.daemon = True
                client_thread.start()

        except KeyboardInterrupt:
            print("Chat server is closing...")
            break

        except Exception as e:
            print(e)
            break

    server_socket.close()


if __name__ == "__main__":
    server()
