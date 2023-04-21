import logging
import socket
import json
from contextlib import contextmanager
import argparse
import signal
import sys
import time
from datetime import datetime
import pytest


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
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


def signal_handler(sig, frame):
    print(f"Received signal {sig}. Exiting...{frame}")
    sys.exit(0)


# Set up signal handlers to gracefully handle interrupt signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UDP message transmitter')
    parser.add_argument('udp_ip', help='UDP IP address')
    parser.add_argument('udp_port', type=int, help='UDP port number')
    parser.add_argument('json_file', help='JSON file containing messages')
    args = parser.parse_args()

    transmitter = Transmitter(args.udp_ip, args.udp_port, args.json_file)
    messages = transmitter.read_messages_from_file()

    if messages:
        with transmitter.transmitter_socket() as sock:
            for message in messages:
                transmitter.sendto_udp(message)
                time.sleep(1)
    else:
        print(f"No messages found in {args.json_file}. Exiting...")
        sys.exit(1)

