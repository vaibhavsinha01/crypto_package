import socket 

def rotr(x, n):
    return ((x >> n) | (x << (64 - n))) & 0xffffffffffffffff

def sha512(message):
    msg = bytearray(message.encode())
    length = len(msg) * 8
    msg.append(0x80)
    while (len(msg) % 128) != 112:
        msg.append(0)
    msg += length.to_bytes(16, 'big')
    H = [
        0x6a09e667f3bcc908, 0xbb67ae8584caa73b,
        0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
        0x510e527fade682d1, 0x9b05688c2b3e6c1f,
        0x1f83d9abfb41bd6b, 0x5be0cd19137e2179
    ]
    K = [
        0x428a2f98d728ae22, 0x7137449123ef65cd
    ] * 40  

    for i in range(0, len(msg), 128):
        w = [0]*80
        chunk = msg[i:i+128]

        for j in range(16):
            w[j] = int.from_bytes(chunk[j*8:(j+1)*8], 'big')

        for j in range(16, 80):
            s0 = rotr(w[j-15],1) ^ rotr(w[j-15],8) ^ (w[j-15]>>7)
            s1 = rotr(w[j-2],19) ^ rotr(w[j-2],61) ^ (w[j-2]>>6)
            w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xffffffffffffffff

        a,b,c,d,e,f,g,h = H

        for j in range(80):
            S1 = rotr(e,14) ^ rotr(e,18) ^ rotr(e,41)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + S1 + ch + K[j] + w[j]) & 0xffffffffffffffff

            S0 = rotr(a,28) ^ rotr(a,34) ^ rotr(a,39)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffffffffffff

            h,g,f,e,d,c,b,a = g,f,e,(d + temp1) & 0xffffffffffffffff,c,b,a,(temp1 + temp2) & 0xffffffffffffffff

        H = [(x+y) & 0xffffffffffffffff for x,y in zip(H,[a,b,c,d,e,f,g,h])]

    return ''.join(format(x, '016x') for x in H)

server = socket.socket()
server.bind(("localhost", 12347))
server.listen(1)

print("sha-512 Server running...")

conn, addr = server.accept()
data = conn.recv(1024).decode()

hash_val = sha512(data)

conn.send(hash_val.encode())
conn.close()