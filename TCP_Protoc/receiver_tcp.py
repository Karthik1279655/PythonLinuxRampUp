# Server
import socket
import tcp_data_pb2


class TCPReceiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def start(self):
        self.sock.listen()
        print(f"Server started and listening on {self.host}:{self.port}")
        conn, addr = self.sock.accept()
        print(f"Connection established from {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                tcp_data = tcp_data_pb2.StudentList()
                tcp_data.ParseFromString(data)

                # Print all details to console
                print(f"ID: {tcp_data.student_id}")
                print(f"Name: {tcp_data.student_name}")
                print(f"Age: {tcp_data.age}")
                print(f"Address: {tcp_data.address}")
                # for phone_number in tcp_data.phone_number:
                #     print(f"Phone number: {phone_number}")
                print("\nMessages Received Successfully")

                # Send acknowledgement to sender
                conn.sendall(b"Acknowledgement received")

            except (socket.error, KeyError) as e:
                print(f"An error occurred while receiving message: {e}")
                raise e

        conn.close()
        print(f"Connection closed from {addr}")


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5005
    try:
        receiver = TCPReceiver(HOST, PORT)
        receiver.start()
    except Exception as e:
        print(f"An error occurred: {e}")
