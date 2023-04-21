from student import Student
from transmitter_tcp import Transmitter

# Create a new Student object
student = Student()
student.set_student_id(1234)
student.set_student_name("John Smith")
student.set_age(20)
student.set_address("123 Main St")
student.add_phone_number("555-1234")
student.add_phone_number("555-5678")

# Create a new Transmitter object and transmit the student information
transmitter = Transmitter('localhost', 12345)
transmitter.transmit(student)
