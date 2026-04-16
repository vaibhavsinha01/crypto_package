import socket 

s = socket.socket()
s.connect(("127.0.0.1",5006))
m = int(input())
s.send(str(m).encode())
data = s.recv(1024).decode()
ciph,d,n = map(int,data.split(","))
msg = pow(ciph,d,n)
print(msg)
s.close()

