import socket


class UDPClient:
    def __init__(self, port):
        self.port = port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("Socket created successfully")
        except socket.error as err:
            print(f"Socket creation failed with error: {err}")


class Transmitter(UDPClient):
    def __init__(self, port):
        super().__init__(port)

    def send_message(self, message):
        self.sock.sendto(message.encode('utf-8'), ('127.0.0.1', self.port))
        self.sock.close()


class Receiver(UDPClient):
    def __init__(self, port):
        super().__init__(port)
        self.sock.bind(('127.0.0.1', self.port))

    def receive_message(self):
        data, addr = self.sock.recvfrom(1024)
        message = data.decode('utf-8')
        print(f"Received message: {message}")
        self.sock.close()


tx = Transmitter(5008)
rx = Receiver(5008)

tx.send_message("Sasken Technologies")
rx.receive_message()

