import socket 
p = 17
g = 10
x = 5 
y = pow(g,x,p)
k = 3
s = socket.socket()
s.bind(("127.0.0.1",6561))
s.listen(1) 
c,a = s.accept()
m = int(c.recv(1024).decode())
c1 = pow(g,k,p)
c2 = (m*pow(y,k,p))%p
c.send(f"{c1},{c2},{x},{p}".encode())
c.close()
s.close()