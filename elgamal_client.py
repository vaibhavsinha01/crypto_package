import socket 

s = socket.socket()
s.connect(("127.0.0.1"),5007)
m = int(input())
s.send(str(m).encode())
data = s.recv(1024).decode()
c1,c2,x,p = map(int,data.split(","))
s_val = pow(c1,x,p)
inv = pow(s_val,p-2,p)
msg = (c2*inv)%p
print(msg)
s.close()