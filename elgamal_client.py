import socket
import random

def is_prime(n, k=10):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_prime(n):
            return n

def find_generator(p):
    for g in range(2, p):
        if pow(g, (p-1)//2, p) != 1:
            return g

def generate_keys(bits=256):
    p = generate_prime(bits)
    g = find_generator(p)
    x = random.randint(2, p - 2)
    h = pow(g, x, p)
    return (p, g, h), x

def encrypt(message, public_key):
    p, g, h = public_key
    cipher = []
    for c in message:
        m = ord(c)
        k = random.randint(2, p - 2)
        c1 = pow(g, k, p)
        c2 = (m * pow(h, k, p)) % p
        cipher.append((c1, c2))
    return cipher

print("Generating ElGamal keypair...")
public_key, private_key = generate_keys(bits=256)
p, g, h = public_key

print(f"p: {p}")
print(f"g: {g}")
print(f"h (public key): {h}")

plaintext = input("Enter plaintext message: ")
cipher = encrypt(plaintext, public_key)
cipher_str = ';'.join(f"{c1},{c2}" for c1, c2 in cipher)

print("Encrypted (truncated):", cipher_str[:80], "...")

client = socket.socket()
client.connect(("localhost", 4444))

payload = f"{p}|{g}|{h}|{private_key}|{cipher_str}"
client.send(payload.encode())
print("Sent to server")
client.close()