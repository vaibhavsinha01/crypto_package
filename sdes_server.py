import socket

P10 = [3,5,2,7,4,10,1,9,8,6]
P8  = [6,3,7,4,8,5,10,9]
IP  = [2,6,3,1,4,8,5,7]
IP_INV = [4,1,3,5,7,2,8,6]
EP  = [4,1,2,3,2,3,4,1]
P4  = [2,4,3,1]

S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

def permute(bits, table):
    return ''.join(bits[i-1] for i in table)

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def sbox(bits, box):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return format(box[row][col], '02b')

def generate_keys(key):
    key = permute(key, P10)
    left, right = key[:5], key[5:]
    left, right = left_shift(left, 1), left_shift(right, 1)
    k1 = permute(left + right, P8)
    left, right = left_shift(left, 2), left_shift(right, 2)
    k2 = permute(left + right, P8)
    return k1, k2

def fk(bits, key):
    left, right = bits[:4], bits[4:]
    temp = xor(permute(right, EP), key)
    p4 = permute(sbox(temp[:4], S0) + sbox(temp[4:], S1), P4)
    return xor(left, p4) + right

def decrypt(cipher, key):
    k1, k2 = generate_keys(key)
    bits = permute(cipher, IP)
    bits = fk(bits, k2)
    bits = fk(bits[4:] + bits[:4], k1)
    return permute(bits, IP_INV)

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 4444))
server.listen(1)

print("Server waiting...")
conn, addr = server.accept()

cipher = conn.recv(1024).decode()
print("Received cipher:", cipher)

key = input("Enter 10-bit key: ")
print("Decrypted:", decrypt(cipher, key))

conn.close()
server.close()