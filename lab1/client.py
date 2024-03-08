import socket
import threading

closed = False


def receive(client_socket: socket.socket):
    global closed
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                closed = True
                print("Server closed connection")
                break
            print(f"\n<<< {message}")
        except Exception as e:
            print(e)
            break


def client():
    host = "127.0.0.1"
    port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    global closed
    while True:
        try:
            message = input(">>> ")
            if closed:
                break
            client_socket.send(message.encode("utf-8"))

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(e)
            break

    client_socket.close()


if __name__ == "__main__":
    client()
