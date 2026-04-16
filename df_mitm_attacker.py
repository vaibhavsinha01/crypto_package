import socket 
p = 23
g = 5
m1 = 3
m2 = 7

M1 = pow(g,m1,p)
M2 = pow(g,m2,p)

server = socket.socket()
server.connect(("127.0.0.1",5010))
attacker = socket.socket()
attacker.bind(("127.0.0.1"),5009)
attacker.listen(1)

client,addr = attacker.accept()
B = int(client.recv(1024).decode())
server.send(str(M1).encode())
A = int(server.recv(1024).decode())
client.send(str(M2).encode())

key1 = pow(B,m2,p)
key2 = pow(A,m1,p)

print(key1)
print(key2)

client.close()
server.close()
attacker.close()