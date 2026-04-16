import socket 

def hash_fn(m):
    h = 0
    for c in m:
        h = (h*31+ord(c))%100000
    
    return h 

def inv(a,m):
    for i in range(1,m):
        if(a*i)%m == 1:
            return i 

p = 23
q = 11
g = 2
y = pow(g,5,p)

s = socket.socket()
s.connect(("127.0.0.1",5004))

msg = input()
s.send(msg.encode())
data = s.recv(1024).decode()
r,s1 = map(int,data.split(','))
H = hash_fn(msg)

w = inv(s1,q)
u1 = (H*w)%q
u2 = (r*w)%q 

v = ((pow(g,u1,p)*pow(y,u2,p))%p)%q 

print("Valid" if v==r else "Invalid")
s.close()