import json
from datetime import datetime
import logging
import socket
from contextlib import contextmanager


class Message:
    # a class to represent a message
    def __init__(self, message_id, text, time):
        self.message_id = message_id
        self.text = text
        self.time = time

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_dict(cls, message_dict):
        message_dict['time'] = int(datetime.now().timestamp() * 1000)
        return cls(**message_dict)


class Transmitter:
    # a class to represent a message transmitter
    def __init__(self, udp_ip, udp_port, json_file):
        self.logger = logging.getLogger(__name__)
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.json_file = json_file
        self.sock = None

        # configure the logging module
        logging.basicConfig(filename='udp_log.log',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

    def socket_creation(self):
        try:
            # create a UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.logger.info("Socket created successfully")
        except socket.error as err:
            self.logger.exception(f"Socket creation failed with error: {err}")

    def read_messages_from_file(self):
        try:
            with open(self.json_file, 'r') as file:
                messages_data = json.load(file)
                self.logger.debug(f"Opened JSON file {self.json_file}")
        except FileNotFoundError as err:
            self.logger.exception(f"Error: {self.json_file} not found. {err}")
            return None

        messages = []
        for message_data in messages_data:
            message = Message.from_dict(message_data)
            messages.append(message)
        return messages

    def send_message(self, message):
        message_str = message.to_json()
        try:
            self.sock.sendto(message_str.encode(), (self.udp_ip, self.udp_port))
            self.logger.debug(f"Sent message: {message.to_json()}")
        except socket.error as err:
            self.logger.exception(f"Message transferring failed with error: {err}")
            exit(0)

    def stop(self):
        if self.sock:
            self.sock.close()
            self.logger.info("Socket closed successfully")

    def __enter__(self):
        self.socket_creation()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def sendto_udp(self, message):
        with self:
            self.send_message(message)


class Receiver:
    # a class to represent a message receiver
    def __init__(self, udp_ip, udp_port, json_file):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = None
        self.json_file = json_file
        self.logger = None

    def setup_logging(self):
        # configure the logging module
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler('udp_log.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def create_socket(self):
        try:
            # create a UDP socket and bind it to the specified IP address and port number
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.udp_ip, self.udp_port))
            self.logger.info("Socket bound successfully")
        except socket.error as err:
            self.logger.exception(f"Socket binding failed with error: {err}")
            exit(0)

    def receive_messages(self):
        while True:
            # Receive data from the UDP socket and get the sender's address
            data, addr = self.sock.recvfrom(1024)

            # Convert the received data to a Message object
            message_dict = json.loads(data.decode())
            message = Message(**message_dict)
            # Set the message time to the current time in milliseconds
            message.time = int(datetime.now().timestamp() * 1000)
            self.logger.info(f"Received message: {message.__dict__}")

    def stop(self):
        # close the socket object
        if self.sock:
            self.sock.close()
            self.logger.info("Socket closed successfully")

    def run(self):
        self.setup_logging()
        self.create_socket()
        self.receive_messages()

    @contextmanager
    def receiver_socket(self):
        self.create_socket()
        try:
            yield self.sock
        finally:
            self.stop()

