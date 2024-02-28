import socket

serverIP = "127.0.0.1"
serverPort = 9008
msg_bytes = bytes("Python", "cp1250")

print("PYTHON UDP CLIENT")
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(msg_bytes, (serverIP, serverPort))

buff, address = client.recvfrom(1024)
print(f"Received msg: {str(buff, 'cp1250')}")
