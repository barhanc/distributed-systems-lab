import socket
import threading

ASCII_ART = """
,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
| ~ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | [ | ] | <-    |
|---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----|
| ->| | " | , | . | P | Y | F | G | C | R | L | / | = |  \  |
|-----',--',--',--',--',--',--',--',--',--',--',--',--'-----|
| Caps | A | O | E | U | I | D | H | T | N | S | - |  Enter |
|------'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'--------|
|        | ; | Q | J | K | X | B | M | W | V | Z |          |
|------,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|
| ctrl |  | alt |                          | alt  |  | ctrl |
'------'--'-----'--------------------------'------'--'------'
"""
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
            closed = True
            print(e)
            break


def receive_udp(udp_socket: socket.socket):
    while True:
        try:
            buff, _ = udp_socket.recvfrom(1024)
            print(f"\n<<<\n{buff.decode('utf-8')}")
        except Exception as e:
            print(e)
            break


def client():
    addr_server = ("127.0.0.1", 9009)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(addr_server)

    receive_thread = threading.Thread(target=receive, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()
    #
    #
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(client_socket.getsockname())

    udp_thread = threading.Thread(target=receive_udp, args=(udp_socket,))
    udp_thread.daemon = True
    udp_thread.start()

    global closed
    while True:
        try:
            message = input(">>> ")
            if closed:
                break
            if message == "U":
                udp_socket.sendto(ASCII_ART.encode("utf-8"), addr_server)
            else:
                client_socket.send(message.encode("utf-8"))

        except KeyboardInterrupt:
            print("\nClient stopped")
            break

        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    client()
