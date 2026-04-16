import socket

def permute(bits, table):
    return ''.join(bits[i-1] for i in table)

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b):
    return ''.join('0' if i == j else '1' for i, j in zip(a, b))

S0 = [[1,0,3,2],
      [3,2,1,0],
      [0,2,1,3],
      [3,1,3,2]]

S1 = [[0,1,2,3],
      [2,0,1,3],
      [3,0,1,0],
      [2,1,0,3]]

def sbox(bits, box):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return format(box[row][col], '02b')

def generate_keys(key):
    P10 = [3,5,2,7,4,10,1,9,8,6]
    P8  = [6,3,7,4,8,5,10,9]

    key = permute(key, P10)
    left, right = key[:5], key[5:]

    left, right = left_shift(left,1), left_shift(right,1)
    k1 = permute(left+right, P8)

    left, right = left_shift(left,2), left_shift(right,2)
    k2 = permute(left+right, P8)

    return k1, k2

def fk(bits, key):
    EP = [4,1,2,3,2,3,4,1]
    P4 = [2,4,3,1]

    left, right = bits[:4], bits[4:]

    right_exp = permute(right, EP)
    temp = xor(right_exp, key)

    s0 = sbox(temp[:4], S0)
    s1 = sbox(temp[4:], S1)

    p4 = permute(s0+s1, P4)
    left = xor(left, p4)

    return left + right

def switch(bits):
    return bits[4:] + bits[:4]

def sdes_encrypt(plain, key):
    IP = [2,6,3,1,4,8,5,7]
    IP_INV = [4,1,3,5,7,2,8,6]

    k1, k2 = generate_keys(key)

    bits = permute(plain, IP)
    bits = fk(bits, k1)
    bits = switch(bits)
    bits = fk(bits, k2)

    return permute(bits, IP_INV)

client = socket.socket()
client.connect(("localhost", 4444))

plaintext = input("Enter 8-bit plaintext: ")
key = input("Enter 10-bit key: ")

cipher = sdes_encrypt(plaintext, key)

client.send(cipher.encode())

print("Encrypted:", cipher)
print("Sent to server")

client.close()