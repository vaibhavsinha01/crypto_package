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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y
    _, x, _ = extended_gcd(e, phi)
    return x % phi

def generate_keypair(bits=512):
    p, q = generate_prime(bits), generate_prime(bits)
    while p == q:
        q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e += 2
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(c), e, n) for c in message]

print("Generating RSA keypair (this may take a moment)...")
public_key, private_key = generate_keypair(bits=512)
e, n = public_key

print(f"Public key (e): {e}")
print(f"Modulus (n): {n}")

plaintext = input("Enter plaintext message: ")
cipher = encrypt(plaintext, public_key)
cipher_str = ','.join(str(x) for x in cipher)

print("Encrypted:", cipher_str[:80], "...")

client = socket.socket()
client.connect(("localhost", 4444))

payload = f"{e}|{n}|{cipher_str}"
client.send(payload.encode())
print("Sent to server")
client.close()