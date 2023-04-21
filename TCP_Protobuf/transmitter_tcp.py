import socket
import tcp_data_pb2 as student_pb


class Transmitter:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port

    def transmit(self, student):
        # Create a new StudentList protocol buffer message
        student_list = student_pb.StudentList()

        # Set the fields of the message using the student object
        student_list.student_id = student.get_student_id()
        student_list.student_name = student.get_student_name()
        student_list.age = student.get_age()
        student_list.address = student.get_address()
        student_list.phone_number.extend(student.get_phone_numbers())

        # Serialize the message to bytes
        student_msg = student_list.SerializeToString()

        # Create a new socket and connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self._ip, self._port))

            # Send the message
            sock.sendall(student_msg)
