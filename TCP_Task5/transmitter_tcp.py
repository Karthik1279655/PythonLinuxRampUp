import socket
import tcp_data_pb2
import google.protobuf.text_format as text_format
import signal


class TCPTransmitter:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            print(f"Connected to {self.host} PORT:{self.port}")
        except socket.error as e:
            print(f"An error occurred while connecting: {e}")
            raise e

    def send_message(self):
        try:
            # Read message from .pbtxt file
            message = self.read_message()

            # Parse message
            tcp_data = self.parse_message(message)

            # Send message
            self.send_tcp_data(tcp_data)

            # Receive acknowledgement
            self.receive_acknowledgement()

        except (socket.error, KeyError) as e:
            print(f"An error occurred while sending message: {e}")
            raise e

    def read_message(self):
        with open("messages.pbtxt", "r") as f:
            message = f.read()
        return message

    def parse_message(self, message):
        tcp_data = tcp_data_pb2.StudentList()
        text_format.Merge(message, tcp_data)
        return tcp_data

    def send_tcp_data(self, tcp_data):
        data = tcp_data.SerializeToString()
        self.sock.sendall(data)
        print('Messages send successfully...')

    def receive_acknowledgement(self):
        ack = self.sock.recv(1024)
        print(f"Acknowledgement received: {ack.decode()}")

    def close(self):
        try:
            self.sock.close()
        except socket.error as e:
            print(f"An error occurred while closing socket: {e}")
            raise e

    def handle_signal(self, signal_number, stack_frame):
        print("Interrupt signal received. Closing socket.")
        self.close()
        exit(0)


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5100
    try:
        with TCPTransmitter(HOST, PORT) as transmitter:
            signal.signal(signal.SIGINT, transmitter.handle_signal) # Register signal handler for SIGINT
            transmitter.send_message()
    except Exception as e:
        print(f"An error occurred on server side: {e}")
