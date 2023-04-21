import json
import socket
from datetime import datetime
import logging
import time
import sys
import signal


class Message:
    def __init__(self, message_id, text, time):
        self.message_id = message_id
        self.text = text
        self.time = time


class Transmitter:
    def __init__(self, udp_ip, udp_port, json_file):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.json_file = json_file
        self.sock = None

        logging.basicConfig(filename='transmitter.log',
                            filemode='a',
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            logging.info("Socket created successfully")
        except socket.error as err:
            logging.exception(f"Socket creation failed with error: {err}")

    def transmit_messages(self):
        try:
            with open(self.json_file, 'r') as file:
                messages_data = json.load(file)
        except FileNotFoundError as err:
            logging.exception(f"Error: {self.json_file} not found. {err}")
            return

        for message_data in messages_data:
            message = Message(**message_data)
            message.time = int(datetime.now().timestamp() * 1000)
            message_str = json.dumps(message.__dict__)
            try:
                self.sock.sendto(message_str.encode(), (self.udp_ip, self.udp_port))
                logging.info(f"Sent message: {message.__dict__}")
            except socket.error as err:
                logging.exception(f"Message transferring failed with error: {err}")
                exit(0)

    def stop(self):
        if self.sock:
            self.sock.close()
            logging.info("Socket closed successfully")


class Receiver:
    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.udp_ip, self.udp_port))
            logging.info("Socket bound successfully")
        except socket.error as err:
            logging.exception(f"Socket binding failed with error: {err}")
            exit(0)

    def receive_messages(self):
        logging.basicConfig(filename='receiver.log',
                            filemode='a',
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )
        while True:
            data, addr = self.sock.recvfrom(1024)
            message_dict = json.loads(data.decode())
            message = Message(**message_dict)
            message.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Received message: {message.__dict__}")
            logging.info(f"Received message: {message.__dict__}")

    def stop(self):
        if self.sock:
            self.sock.close()
            logging.info("Socket closed successfully")
