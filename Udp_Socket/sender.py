import socket

ip = '127.0.0.1'
port = 5006
message = input().encode()

print(f'Sending {message} to {ip}:{port}')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(message, (ip, port))

