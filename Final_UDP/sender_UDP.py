import json
import socket
import time
from datetime import datetime
import argparse
import signal
import sys


class Message:
    def __init__(self, message_id, text):
        self.message_id = message_id
        self.text = text
        self.time = None

    def set_time(self):
        self.time = datetime.now().strftime("%H:%M:%S.%f")

    def to_json(self):
        return {'message_id': self.message_id, 'text': self.text, 'time': self.time}


class Transmitter:
    def __init__(self, json_file, ip, udp_port):
        self.json_file = json_file
        self.dest_ip = ip
        self.udp_port = udp_port

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(3)
            print("UDP socket created successfully")
        except socket.error as err:
            print("Failed to create socket: ", err)

        try:
            self.messages = self.load_messages_from_file()
        except FileNotFoundError as err:
            print(f"Error: {err}")
            sys.exit(1)

        self.receiver_addr = (self.dest_ip, self.udp_port)

    def load_messages_from_file(self):
        with open(self.json_file, 'r') as f:
            messages = json.load(f)
        return [Message(message['message_id'], message['text']) for message in messages]

    def read(self, message_id):
        for message in self.messages:
            if message.message_id == message_id:
                return message
        return None

    def write(self, message_id, text):
        message = self.read(message_id)
        if message:
            message.text = text
            message.set_time()
            message_json = json.dumps(message.to_json()).encode()
            self.sock.sendto(message_json, self.receiver_addr)

            try:
                response, _ = self.sock.recvfrom(1024)
                if response.decode() == 'ok':
                    print(f"Message {message_id} sent successfully. time: {message.time}")
            except socket.timeout:
                print("No response received from receiver...")
        else:
            print(f"Message {message_id} not found")

    def transmit(self):
        def signal_handler(sig, frame):
            print('Interrupt Occurs...Ending transmission...')
            self.sock.sendto(b'exit', self.receiver_addr)
            self.sock.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        while True:
            try:
                self.sock.sendto(b'ping', self.receiver_addr)
                response, _ = self.sock.recvfrom(1024)
                if response.decode() == 'Hi':
                    break
            except socket.error as e:
                print(f"Waiting for receiver: {e}")
                time.sleep(1)

        for message in self.messages:
            self.write(message.message_id, message.text)
            time.sleep(2)

        try:
            self.sock.sendto(b'exit', self.receiver_addr)
            response, _ = self.sock.recvfrom(1024)
            if response.decode() == 'ok':
                print("All messages sent successfully")
        except socket.timeout:
            print("No response received...closing!!")

        self.sock.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9999, help='UDP port number')
    args = parser.parse_args()

    transmitter = Transmitter('messages.json', 'localhost', args.port)
    transmitter.transmit()
