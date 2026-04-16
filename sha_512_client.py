import socket

client = socket.socket()
client.connect(("localhost", 12347))
msg = input("Enter message: ")
client.send(msg.encode())
print("sha-512:", client.recv(1024).decode())
client.close()