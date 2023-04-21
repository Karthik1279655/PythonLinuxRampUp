import socket

ip = '127.0.0.1'
port = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((ip, port))

print(f'Start Listening to {ip} : {port}')

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Received message: {data}")
