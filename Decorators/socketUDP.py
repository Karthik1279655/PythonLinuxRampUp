import socket


def receiver(host='', port=5000):
    def decorator(func):
        def wrapper(*args, **kwargs):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((host, port))
            print(f"Listening on {host}:{port}...")
            while True:
                data, addr = sock.recvfrom(1024)
                print(f"Received from {addr}: {data.decode('utf-8')}")
                func(data, addr)
        return wrapper
    return decorator


def sender(host='localhost', port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def decorator(func):
        def wrapper(*args, **kwargs):
            message = func(*args, **kwargs)
            sock.sendto(message.encode('utf-8'), (host, port))
            print(f"Sent to {host}:{port}: {message}")
        return wrapper
    return decorator


@receiver()
def process_data(data, addr):
    # process received data here
    pass


@sender()
def send_message():
    # get message to send here
    return "Hello, world!"


if __name__ == '__main__':
    send_message()
