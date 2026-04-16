import socket

def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y
    _, x, _ = extended_gcd(e, phi)
    return x % phi

def decrypt(cipher, private_key):
    d, n = private_key
    return ''.join(chr(pow(c, d, n)) for c in cipher)

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 4444))
server.listen(1)

print("Server waiting...")
conn, addr = server.accept()

data = conn.recv(65536).decode()
parts = data.split('|')
e = int(parts[0])
n = int(parts[1])
cipher = [int(x) for x in parts[2].split(',')]

print(f"Received public key e: {e}")
print(f"Modulus n: {n}")

p = int(input("Enter prime p: "))
q = int(input("Enter prime q: "))

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)
private_key = (d, n)

print("Decrypted:", decrypt(cipher, private_key))

conn.close()
server.close()