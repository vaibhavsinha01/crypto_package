import socket
import math

def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xffffffff

def md5(msg):
    msg = bytearray(msg, 'utf-8')
    original_len_bits = (8 * len(msg)) & 0xffffffffffffffff

    msg.append(0x80)
    while (len(msg) * 8) % 512 != 448:
        msg.append(0)

    for i in range(8):
        msg.append((original_len_bits >> (8 * i)) & 0xff)

    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    K = [int(abs(math.sin(i + 1)) * (2**32)) & 0xffffffff for i in range(64)]
    s = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4

    for i in range(0, len(msg), 64):
        chunk = msg[i:i+64]

        M = []
        for j in range(16):
            val = (chunk[j*4] |
                   (chunk[j*4+1] << 8) |
                   (chunk[j*4+2] << 16) |
                   (chunk[j*4+3] << 24))
            M.append(val)

        a, b, c, d = A, B, C, D

        for j in range(64):
            if j < 16:
                f = (b & c) | (~b & d)
                g = j
            elif j < 32:
                f = (d & b) | (~d & c)
                g = (5*j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3*j + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7*j) % 16

            f = (f + a + K[j] + M[g]) & 0xffffffff
            a, d, c, b = d, c, b, (b + left_rotate(f, s[j])) & 0xffffffff

        A = (A + a) & 0xffffffff
        B = (B + b) & 0xffffffff
        C = (C + c) & 0xffffffff
        D = (D + d) & 0xffffffff

    return ''.join(x.to_bytes(4, 'little').hex() for x in [A, B, C, D])


def start_server():
    host = '127.0.0.1'
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    print("MD5 Server running on port 5000...")

    conn, addr = server.accept()
    print("Connected by:", addr)

    data = conn.recv(1024).decode()
    print("Received:", data)

    result = md5(data)
    conn.send(result.encode())

    conn.close()
    server.close()

if __name__ == "__main__":
    start_server()