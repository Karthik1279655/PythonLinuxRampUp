import socket
import tcp_data_pb2 as StudentList

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific port
server_address = ('localhost', 5010)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    connection, client_address = sock.accept()

    try:
        print('Connection from', client_address)

        # Receive the data in small chunks and reassemble it
        data = b''
        while True:
            chunk = connection.recv(1024)
            if not chunk:
                break
            data += chunk

        # Parse the received data into a StudentList message
        student_list = StudentList.StudentList()
        student_list.ParseFromString(data)

        # Print the received student data
        for student in student_list.studentList:
            print(f"Received student data - ID: {student.student_id}, Name: {student.student_name}, Age: {student.age}, Address: {student.address}, Phone numbers: {student.phone_number}")
    finally:
        # Clean up the connection
        connection.close()
