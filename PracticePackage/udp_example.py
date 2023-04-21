import json
import socket
from _datetime import datetime


class Message:
    def __init__(self, message_id, text, time):
        self.message_id = message_id
        self.text = text
        self.time = time


class MessageTransmitter:
    def __init__(self, udp_ip, udp_port, json_file):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.json_file = json_file
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def transmit_messages(self):
        with open(self.json_file, 'r') as file:
            messages_data = json.load(file)

        for message_data in messages_data:
            message = Message(**message_data)
            message.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Add current timestamp to message
            message_str = json.dumps(message.__dict__)
            self.sock.sendto(message_str.encode(), (self.udp_ip, self.udp_port))
            print(f"Sent message: {message.__dict__}")

    def stop(self):
        self.sock.close()


class MessageReceiver(MessageTransmitter):
    def __init__(self, udp_ip, udp_port):
        super().__init__(udp_ip, udp_port, json_file=None)
        self.sock.bind((self.udp_ip, self.udp_port))

    def receive_messages(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message_dict = json.loads(data.decode())
            message = Message(**message_dict)
            message.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Received message: {message.__dict__}")

    def stop(self):
        super().stop()
