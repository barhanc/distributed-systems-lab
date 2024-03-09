import socket
import threading
from dataclasses import dataclass


@dataclass
class Client:
    id: int
    name: str
    socket: socket.socket
    address: str


lock = threading.Lock()


def handle_client(client: Client, clients: list[Client], pool: set[int]):
    client.socket.send(f"Connected. You are {client.name}.".encode("utf-8"))
    while True:
        try:
            message = client.socket.recv(1024).decode("utf-8")
            if not message:
                print(f"Client {client.name} disconnected")
                with lock:
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
            with lock:
                clients.remove(client)
                pool.add(client.id)
            break


def handle_udp(udp_socket: socket.socket, clients: list[Client]):
    while True:
        try:
            buff, addr = udp_socket.recvfrom(1024)
            print(f"Received message\n{buff.decode('utf-8')}")
            for client in clients:
                if client.address != addr:
                    udp_socket.sendto(buff, client.address)

        except Exception as e:
            print(e)
            break


def server(max_pool=2):
    addr = ("127.0.0.1", 9009)
    server_socket = socket.create_server(addr, family=socket.AF_INET)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(addr)

    clients: list[Client] = []
    pool = set(range(max_pool))

    print("Chat server is running...")

    udp_thread = threading.Thread(target=handle_udp, args=(udp_socket, clients))
    udp_thread.daemon = True
    udp_thread.start()

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")

            if len(pool) == 0:
                client_socket.send("Connection rejected. Pool is empty.".encode("utf-8"))
                client_socket.close()
                print(f"Connection rejected. Pool is empty.")
            else:
                with lock:
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
