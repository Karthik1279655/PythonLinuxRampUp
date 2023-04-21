import socket
import signal
import tcp_data_pb2


class TCPReceiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def bind(self):
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print(f"Listening on {self.host}:{self.port}")
        except socket.error as e:
            print(f"An error occurred while binding: {e}")
            raise e

    def receive_message(self):
        try:
            conn, addr = self.sock.accept()
            print(f"Connection established with {addr}")

            data = conn.recv(1024)
            tcp_data = tcp_data_pb2.StudentList()
            tcp_data.ParseFromString(data)

            # Print received data to console
            print(f"ID: {tcp_data.student_id}")
            print(f"Name: {tcp_data.student_name}")
            print(f"Age: {tcp_data.age}")
            print(f"Address: {tcp_data.address}")
            print(f"Phone numbers: {', '.join(tcp_data.phone_number)}")

            # Send an acknowledgement back to the client
            conn.sendall("Message received".encode())

        except socket.error as e:
            print(f"An error occurred while receiving message: {e}")
            raise e

    def close(self):
        try:
            self.sock.close()
        except socket.error as e:
            print(f"An error occurred while closing socket: {e}")
            raise e


def signal_handler(sig, frame):
    print('Signal received, shutting down...')
    raise KeyboardInterrupt


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5100

    # Register signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        with TCPReceiver(HOST, PORT) as receiver:
            while True:
                receiver.receive_message()
    except KeyboardInterrupt:
        print('KeyboardInterrupt received, shutting down...')
    except Exception as e:
        print(f"An error occurred in server side: {e}")
