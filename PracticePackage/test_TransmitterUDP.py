import json
import logging
import socket
import time
from datetime import datetime
import argparse
import signal
import sys
import pytest


@pytest.fixture()
class Message:
    # a class to represent a message
    def __init__(self, message_id, text, time):
        self.message_id = message_id
        self.text = text
        self.time = time

    def set_time(self):
        self.time = int(datetime.now().timestamp() * 1000)

    def to_json(self):
        return {'message_id': self.message_id, 'text': self.text, 'time': self.time}


class Transmitter:
    # a class to represent a message transmitter
    def __init__(self, udp_ip, udp_port, json_file):
        self.receiver_addr = None
        self.messages = None
        self.logger = logging.getLogger(__name__)
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.json_file = json_file
        self.sock = None

        # configure the logging module
        logging.basicConfig(filename='udp_log.log',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)

    def __enter__(self):
        try:
            # create a UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(2)
            self.logger.info("UDP Socket created successfully")
        except socket.error as err:
            self.logger.exception(f"Socket creation failed with error: {err}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.sock:
            try:
                self.sock.sendto(b'exit', self.receiver_addr)
                self.logger.debug("Sent exit message")
            except:
                pass
            self.sock.close()
            self.logger.debug("UDP Socket closed successfully")

    def test_add(self):
        assert 1 == 1

    def test_load_messages_from_file(self):
        try:
            with open(self.json_file, 'r') as file:
                messages_data = json.load(file)
                self.logger.debug(f"Opened JSON file {self.json_file}")
        except FileNotFoundError as err:
            self.logger.exception(f"Error: {self.json_file} not found. {err}")
            sys.exit(1)

        assert messages_data == json.load(file)

        self.messages = [Message(**message_data) for message_data in messages_data]
        self.receiver_addr = (self.udp_ip, self.udp_port)

    def test_read(self, message_id):
        for message in self.messages:
            if message.message_id == message_id:
                return message
        return None

    def test_write(self, message_id, text):
        message = self.test_read(message_id)
        if message:
            message.text = text
            message.set_time()
            message_json = json.dumps(message.to_json()).encode()
            self.sock.sendto(message_json, self.receiver_addr)

            try:
                response, _ = self.sock.recvfrom(1024)
                if response.decode() == 'ok':
                    self.logger.debug(f"Message {message_id} sent successfully. time: {message.time}")
            except socket.timeout as e:
                self.logger.exception(f"No response received from receiver: {e}")
        else:
            self.logger.warning(f"Message {message_id} not found")

    def test_transmit(self):
        def signal_handler(sig, frame):
            print('Interrupt Occurs...Ending transmission...')
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler())

        while True:
            try:
                self.sock.sendto(b'ping', self.receiver_addr)
                response, _ = self.sock.recvfrom(1024)
                if response.decode() == 'Hi':
                    break
            except socket.error as e:
                self.logger.debug(f"Waiting for receiver: {e}")
                time.sleep(1)

        for message in self.messages:
            self.test_write(message.message_id, message.text)
            time.sleep(2)

        try:
            self.sock.sendto(b'exit', self.receiver_addr)
            response, _ = self.sock.recvfrom(1024)
            if response.decode() == 'ok':
                self.logger.debug("All messages sent successfully")
        except socket.timeout:
            self.logger.exception("No response received...closing!!")

        self.sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send UDP messages to a specified IP address and port number.")
    parser.add_argument("ip", type=str, help="the IP address to send messages to")
    parser.add_argument("port", type=int, default=9999, help="the port number to send messages to")
    parser.add_argument("file", type=str, help="the path to a JSON file containing messages to send")
    args = parser.parse_args()

    with Transmitter(args.ip, args.port, args.file) as transmitter:
        transmitter.test_load_messages_from_file()
        transmitter.test_transmit()
