import socket 
import random 
p = 23
q = 11
g = 2
x = 5 
y = pow(g,x,p)

def hash_fn(m):
    h = 0
    for c in m:
        h = (h*31 + ord(c))%100000
    return h

def inv(a,m):
    for i in range(1,m):
        if(a*i % m == 1):
            return i   

s = socket.socket()
s.bind(("127.0.0.1",5004))
s.listen(1)

c,a = s.accept()
msg = c.recv(1024).decode()
H = hash_fn(msg)
k = random.randint(1,q-1)
r = (pow(g,k,p))%q
s1 = (inv(k,q)*(H+x*r))%q

c.send(f"{r},{s1}".encode())

c.close()
s.close()