import socket

def decrypt(cipher, p, x):
    result = []
    for c1, c2 in cipher:
        s = pow(c1, x, p)
        s_inv = pow(s, p - 2, p)
        m = (c2 * s_inv) % p
        result.append(chr(m))
    return ''.join(result)

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 4444))
server.listen(1)

print("Server waiting...")
conn, addr = server.accept()

data = conn.recv(65536).decode()
parts = data.split('|')
p = int(parts[0])
g = int(parts[1])
h = int(parts[2])
x = int(parts[3])
cipher_str = parts[4]

cipher = [(int(pair.split(',')[0]), int(pair.split(',')[1])) for pair in cipher_str.split(';')]

print(f"p: {p}")
print(f"g: {g}")
print(f"h: {h}")
print(f"Private key x: {x}")

print("Decrypted:", decrypt(cipher, p, x))

conn.close()
server.close()