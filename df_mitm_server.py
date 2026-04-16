import socket 
p = 23
g = 5 
a = 6 
A = pow(g,a,p)

s = socket.socket()
s.bind(("127.0.0.1",5010))
s.listen(1)
c,addr = s.accept()
B = int(c.recv(1024).decode())
c.send(str(A).encode())
key = pow(B,a,p)
print(f"server key",key)
c.close()
s.close()