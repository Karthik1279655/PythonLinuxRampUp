
class Student:
    def __init__(self):
        self._id = None
        self._name = None
        self._age = None
        self._address = None
        self._phone_numbers = []
        self._response = None

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

    def set_name(self, name):
        self._name = name

    def get_name(self):
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

    def set_response(self, response):
        self._response = response

    def get_response(self):
        return self._response

