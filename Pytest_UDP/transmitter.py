import logging
import socket
from contextlib import contextmanager
import argparse
import signal
import sys
import time
import json
from datetime import datetime
import pytest


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

    def __enter__(self):
        self.socket_creation()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

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

    def _send_message(self, message):
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
        self.sock = None  # Set sock to None after closing it

    @contextmanager
    def transmitter_socket(self):
        self.socket_creation()
        try:
            yield self.sock
        finally:
            self.stop()

    def sendto_udp(self, message):
        try:
            self._send_message(message)
            self.logger.info(f"Sent message: {message.to_json()}")
        except Exception as e:
            self.logger.exception(f"Error sending message: {e}")


def parse_arguments():
    parser = argparse.ArgumentParser(description='UDP Message Transmitter')
    parser.add_argument('--ip', type=str, required=True, help='UDP server IP address')
    parser.add_argument('--port', type=int, required=True, default=9999, help='UDP server port number')
    parser.add_argument('--json', type=str, required=True, help='JSON file containing messages to send')
    return parser.parse_args()


def signal_handler(sig, frame):
    print(f"Received signal : {sig} and Exiting.......")
    sys.exit(0)


# Set up signal handlers to gracefully handle interrupt signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

"""
if __name__ == '__main__':
    args = parse_arguments()
    transmitter = Transmitter(args.ip, args.port, args.json)

    # Set up signal handlers to gracefully handle interrupt signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    with transmitter.transmitter_socket() as sock:
        messages = transmitter.read_messages_from_file()
        if messages is None:
            sys.exit(0)

        for message in messages:
            transmitter.sendto_udp(message)
            time.sleep(1)

"""


# Pytest Implementation :


def test_read_messages_length():
    json_file = 'messages.json'
    with open(json_file, 'r') as file:
        messages_data = json.load(file)
    # load a file with messages
    messages = []
    for message_data in messages_data:
        message = Message.from_dict(message_data)
        messages.append(message)
    assert len(messages) == 3


def test_read():
    with Transmitter('localhost', 5000, 'messages.json') as transmitter:
        messages = transmitter.read_messages_from_file()
        assert len(messages) == 3


def test_signal_handler():
    # create a mock signal and frame
    mock_sig = signal.SIGINT

    # use pytest.raises() to catch the SystemExit exception
    with pytest.raises(SystemExit) as exc_info:
        signal_handler(mock_sig, None)

    # verify that the exception has a value of 0
    assert exc_info.value.code == 0


def test_stop():
    with Transmitter('localhost', 5000, 'messages.json') as transmitter:
        transmitter.stop()
        time.sleep(1)
        assert transmitter.sock is None
