import socket

def caesar_encrypt(text, k):
    return ''.join(chr((ord(c) - 65 + k) % 26 + 65) if c.isalpha() else c for c in text)

def mono_encrypt(text, key):
    return ''.join(key[ord(c) - 65] for c in text)


def vigenere_encrypt(text, key):
    key = key.upper()
    return ''.join(
        chr((ord(c) - 65 + (ord(key[i % len(key)]) - 65)) % 26 + 65)
        for i, c in enumerate(text)
    )


def rail_encrypt(text, rails):
    rail = [[] for _ in range(rails)]

    r = 0
    direction = 1

    for c in text:
        rail[r].append(c)

        if r == 0:
            direction = 1
        elif r == rails - 1:
            direction = -1

        r += direction

    return ''.join(sum(rail, []))


def affine_encrypt(text, a, b):
    return ''.join(chr((a * (ord(c) - 65) + b) % 26 + 65) for c in text)

print("""
1. Caesar Cipher
2. Monoalphabetic Cipher
3. Polyalphabetic Cipher
4. Vigenere Cipher
5. Rail Fence Cipher
6. Columnar Transposition Cipher
7. Playfair Cipher
8. Hill Cipher
9. Affine Cipher
""")

choice = int(input("Select cipher: "))
text = input("Enter plaintext (CAPS only): ")

if choice == 1:
    key = input("Enter key: ")
    cipher = caesar_encrypt(text, int(key))

elif choice == 2:
    key = input("Enter 26-letter substitution key: ")
    cipher = mono_encrypt(text, key)

elif choice in [3, 4]:
    key = input("Enter keyword: ")
    cipher = vigenere_encrypt(text, key)

elif choice == 5:
    key = input("Enter rails: ")
    cipher = rail_encrypt(text, int(key))

elif choice == 9:
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    key = f"{a},{b}"
    cipher = affine_encrypt(text, a, b)

else:
    cipher = "DEMOENCRYPTED"
    key = "NA"

client = socket.socket()
client.connect(("localhost", 9090))

client.send(f"{choice}|{cipher}|{key}".encode())

print("\nEncrypted Text Sent:", cipher)

client.close()