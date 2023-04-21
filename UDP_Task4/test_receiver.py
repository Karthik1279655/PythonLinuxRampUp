import logging
import socket
import signal
import sys
from contextlib import contextmanager
import json
from datetime import datetime

logging.basicConfig(filename='udp_log.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


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


class ReceiverTests:
    # a class to represent a message receiver
    def __init__(self, udp_ip, udp_port):
        self.logger = logging.getLogger(__name__)
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = None

    def socket_creation(self):
        try:
            # create a UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.udp_ip, self.udp_port))
            self.logger.info("Socket created and bound successfully")
        except socket.error as err:
            self.logger.exception(f"Socket creation failed with error: {err}")
            sys.exit(1)

    def read_message(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            self.logger.info(f"Received message: {data}")
            return Message.to_json(data.decode())
        except socket.error as err:
            self.logger.exception(f"Error receiving message: {err}")
            sys.exit(1)

    def stop(self):
        if self.sock:
            self.sock.close()
            self.logger.info("Socket closed successfully")

    @contextmanager
    def receiver_socket(self):
        self.socket_creation()
        try:
            yield self.sock
        finally:
            self.stop()


def signal_handler(sig, frame):
    print(f"Received signal {sig}. Exiting...{frame}")
    sys.exit(0)


if __name__ == '__main__':
    # Set up signal handlers to gracefully handle interrupt signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    udp_ip = 'localhost'
    udp_port = 5119

    receiver = ReceiverTests(udp_ip, udp_port)

    with receiver.receiver_socket() as sock:
        while True:
            message = receiver.read_message()
            print(f"Received message: {message.to_json()}")
