import socket 
p = 23
g = 5
b = 15
B = pow(g,b,p)
s = socket.socket()
s.connect(("127.0.0.1",5009))
s.send(str(B).encode())
A = int(s.recv(1024).decode())
key = pow(A,b,p)
print("Client key:",key)
s.close()