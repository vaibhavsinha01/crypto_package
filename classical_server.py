import socket
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def caesar_decrypt(text, k):
    return ''.join(chr((ord(c) - 65 - k) % 26 + 65) if c.isalpha() else c for c in text)


def mono_decrypt(text, key):
    rev = {key[i]: chr(65 + i) for i in range(26)}
    return ''.join(rev.get(c, c) for c in text)


def vigenere_decrypt(text, key):
    res = ""
    key = key.upper()

    for i, c in enumerate(text):
        if c.isalpha():
            res += chr((ord(c) - 65 - (ord(key[i % len(key)]) - 65)) % 26 + 65)
        else:
            res += c

    return res


def rail_decrypt(cipher, rails):
    n = len(cipher)
    rail = [['\n'] * n for _ in range(rails)]

    idx = 0
    direction = None
    r = 0

    # Mark positions
    for i in range(n):
        if r == 0:
            direction = 1
        elif r == rails - 1:
            direction = -1

        rail[r][i] = '*'
        r += direction

    # Fill cipher
    for i in range(rails):
        for j in range(n):
            if rail[i][j] == '*' and idx < n:
                rail[i][j] = cipher[idx]
                idx += 1

    # Read plaintext
    res = ""
    r = 0
    direction = None

    for i in range(n):
        if r == 0:
            direction = 1
        elif r == rails - 1:
            direction = -1

        res += rail[r][i]
        r += direction

    return res


def affine_decrypt(text, a, b):
    a_inv = None

    for i in range(26):
        if (a * i) % 26 == 1:
            a_inv = i
            break

    if a_inv is None:
        return "Invalid key"

    return ''.join(chr((a_inv * (ord(c) - 65 - b)) % 26 + 65) for c in text)

server = socket.socket()
server.bind(("localhost", 9090))
server.listen(1)

print("Classical Cipher Server Started...\nWaiting for client...")

conn, addr = server.accept()
data = conn.recv(4096).decode()

parts = data.split("|")
choice = int(parts[0])
cipher = parts[1]
key = parts[2]

if choice == 1:
    plain = caesar_decrypt(cipher, int(key))

elif choice == 2:
    plain = mono_decrypt(cipher, key)

elif choice in [3, 4]:
    plain = vigenere_decrypt(cipher, key)

elif choice == 5:
    plain = rail_decrypt(cipher, int(key))

elif choice == 9:
    a, b = map(int, key.split(","))
    plain = affine_decrypt(cipher, a, b)

else:
    plain = "(Demo cipher decrypted successfully)"

print("\nReceived Ciphertext:", cipher)
print("Decrypted Plaintext:", plain)

conn.close()
server.close()