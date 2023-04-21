import json
import socket
import argparse
import signal
import sys
import time


class Receiver:
    def __init__(self, ip, udp_port):
        self.dest_ip = ip
        self.udp_port = udp_port

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("UDP socket created successfully")
        except socket.error as err:
            print("Failed to create socket: %s" % err)

        self.sock.bind((self.dest_ip, self.udp_port))

    def receive(self):
        def signal_handler(sig, frame):
            print("Interrupt Occurs...Ending Receiver..")
            self.sock.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        while True:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()
            if message == 'ping':
                self.sock.sendto(b'Hi', addr)
            elif message == 'exit':
                self.sock.sendto(b'ok', addr)
                break
            else:
                message = json.loads(data.decode())
                print(f"Received message: {message['message_id']}: {message['text']}  time: {message['time']}")
                response = 'ok'
                self.sock.sendto(response.encode(), addr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9999, help='UDP port number')
    args = parser.parse_args()

    receiver = Receiver('localhost', args.port)
    receiver.receive()

