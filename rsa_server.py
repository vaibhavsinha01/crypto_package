import socket 

p = 61
q = 53
n = p*q 
e = 17 
d = 2753 

s = socket.socket()
s.bind(("127.0.0.1",5006))
s.listen(1)

c,a = s.accept()
m = int(c.recv(1024).decode())

cipher = pow(m,e,n)
c.send(f"{cipher},{d},{n}".encode())
c.close()
s.close()