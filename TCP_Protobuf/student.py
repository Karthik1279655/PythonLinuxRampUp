# student.py
import tcp_data_pb2 as StudentList


class Student:
    def __init__(self):
        self._id = None
        self._name = None
        self._age = None
        self._address = None
        self._phone_numbers = []

    def set_student_id(self, student_id):
        self._id = student_id

    def get_student_id(self):
        return self._id

    def set_student_name(self, student_name):
        self._name = student_name

    def get_student_name(self):
        return self._name

    def set_age(self, age):
        self._age = age

    def get_age(self):
        return self._age

    def set_address(self, address):
        self._address = address

    def get_address(self):
        return self._address

    def add_phone_number(self, phone_number):
        self._phone_numbers.append(phone_number)

    def get_phone_numbers(self):
        return self._phone_numbers
