import logging
import socket
import json
from contextlib import contextmanager
import signal
import sys
import time
from datetime import datetime
import pytest


class MessageTests:
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


class TransmitterTests:
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

    @pytest.fixture(scope='module')
    def udp_socket(self):
        """Fixture that creates and returns a UDP socket"""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            yield sock

    @pytest.fixture(scope='module')
    def messages(self):
        """Fixture that reads messages from a JSON file and returns a list of MessageTests objects"""
        try:
            with open(self.json_file, 'r') as file:
                messages_data = json.load(file)
                assert messages_data.text == "Hello! Karthik"
                self.logger.debug(f"Opened JSON file {self.json_file}")
        except FileNotFoundError as err:
            self.logger.exception(f"Error: {self.json_file} not found. {err}")
            return None

        messages = []
        for message_data in messages_data:
            message = MessageTests.from_dict(message_data)
            messages.append(message)
        return messages

    def test_socket_creation(self, udp_socket):
        """Test that the UDP socket was created successfully"""
        assert udp_socket is not None
        self.logger.info("Socket created successfully")

    def test_send_message(self, udp_socket, message):
        """Test that a message can be sent via UDP socket"""
        message_str = message.to_json()
        try:
            udp_socket.sendto(message_str.encode(), (self.udp_ip, self.udp_port))
            self.logger.debug(f"Sent message: {message.to_json()}")
            assert udp_socket.sendto(message_str.encode(), (self.udp_ip, self.udp_port)) == True
        except socket.error as err:
            self.logger.exception(f"Message transferring failed with error: {err}")
            exit(0)

    @pytest.mark.smoke
    def test_stop(self, udp_socket):
        """Test that the UDP socket was closed successfully"""
        udp_socket.close()
        self.logger.info("Socket closed successfully")
        assert udp_socket._closed == True

    @contextmanager
    def test_transmitter_socket(self):
        """Context manager that creates a UDP socket and yields it"""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            self.sock = sock
            self.test_socket_creation(sock)
            try:
                yield self.sock
            finally:
                self.test_stop(sock)

    def test_sendto_udp(self, message):
        try:
            self.test_send_message(message)
            self.logger.info(f"Sent message: {message.to_json()}")
        except Exception as e:
            self.logger.exception(f"Error sending message: {e}")

    def signal_handler(sig, frame):
        print(f"Received signal {sig}. Exiting...{frame}")
        sys.exit(0)

    # Set up signal handlers to gracefully handle interrupt signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Pytest functions start here
    def test_socket_creation():
        transmitter = TransmitterTests("127.0.0.1", 1234, "messages.json")
        transmitter.test_socket_creation()