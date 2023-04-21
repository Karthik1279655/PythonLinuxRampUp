import logging
import socket
import json
from datetime import datetime
from contextlib import contextmanager
from message import Message
import argparse
import signal
import sys


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


def signal_handler(sig, frame):
    print(f"Received signal {sig}. Exiting...{frame}")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UDP message receiver')
    parser.add_argument('--ip', dest='udp_ip', required=True,
                        help='the IP address to bind to')
    parser.add_argument('--port', dest='udp_port', default=9999, required=True,
                        help='the port number to bind to')
    parser.add_argument('--json', dest='json_file', required=True,
                        help='the file containing the JSON schema for the message')
    args = parser.parse_args()

    # Set up signal handlers to gracefully handle interrupt signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    receiver = Receiver(args.udp_ip, int(args.udp_port), args.json_file)

    receiver.run()
