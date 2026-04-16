import socket

def start_client():
    host = '127.0.0.1'
    port = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    message = input("Enter message: ")
    client.send(message.encode())

    result = client.recv(1024).decode()
    print("MD5 Hash:", result)

    client.close()

if __name__ == "__main__":
    start_client()