import socket

serverPort = 9008
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(("", serverPort))
buff = []

print("PYTHON UDP SERVER")

while True:

    buff, address = serverSocket.recvfrom(1024)
    msg = str(buff, "cp1250")
    print("python udp server received msg: " + msg)

    if msg == "Java":
        msg_bytes = bytes("Pong Java", "cp1250")
    elif msg == "Python":
        msg_bytes = bytes("Pong Python", "cp1250")
    else:
        msg_bytes = bytes("Pong Unkown", "cp1250")

    serverSocket.sendto(msg_bytes, address)
