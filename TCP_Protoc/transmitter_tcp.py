# client
import socket
import tcp_data_pb2
from student import Student


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
        except socket.error as e:
            print(f"An error occurred while connecting: {e}")
            raise e

    def send_message(self, student):
        try:
            tcp_data = tcp_data_pb2.StudentList()
            tcp_data.student_id = student.get_id()
            tcp_data.student_name = student.get_name()
            tcp_data.age = student.get_age()
            tcp_data.address = student.get_address()
            for phone_number in student.get_phone_numbers():
                tcp_data.phone_number.append(phone_number)
            data = tcp_data.SerializeToString()
            self.sock.sendall(data)

            ack = self.sock.recv(1024)
            print(f"Acknowledgement received: {ack.decode()}")

            # Print only phone numbers to pbtxt file
            with open("messages.pbtxt", "a") as f:
                f.write(f"phone_number: {', '.join(student.get_phone_numbers())}\n")

            # Print all details except phone numbers to console
            print(f"ID: {student.get_id()}")
            print(f"Name: {student.get_name()}")
            print(f"Age: {student.get_age()}")
            print(f"Address: {student.get_address()}")
            print("\nMessages Sent Successfully")

        except (socket.error, KeyError) as e:
            print(f"An error occurred while sending message: {e}")
            raise e

    def close(self):
        try:
            self.sock.close()
        except socket.error as e:
            print(f"An error occurred while closing socket: {e}")
            raise e


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5005
    try:
        with TCPTransmitter(HOST, PORT) as transmitter:
            student = Student()
            student.set_id(1)
            student.set_name("Karthik")
            student.set_age(23)
            student.set_address("Andhra Pradesh, India")
            student.add_phone_number("12-(3456)7890")
            student.add_phone_number("98-(7654)3210")  # add another phone number
            transmitter.send_message(student)
    except Exception as e:
        print(f"An error occurred: {e}")
