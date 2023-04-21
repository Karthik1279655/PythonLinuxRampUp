# ReceiverUDP.py

import json
import logging
import socket
import argparse
import signal
import sys
import time


class Receiver:
    def __init__(self, ip, udp_port):
        self.dest_ip = ip
        self.udp_port = udp_port
        self.logger = logging.getLogger(__name__)

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.logger.info("UDP socket created successfully")
        except socket.error as err:
            self.logger.exception(f"Failed to create socket: {err}")
            sys.exit(1)

        self.sock.bind((self.dest_ip, self.udp_port))
        self.logger.info(f"Bound socket to {self.dest_ip}:{self.udp_port}")

    def receive(self):
        def signal_handler(sig, frame):
            self.logger.info("Interrupt occurs...Ending Receiver..")
            self.sock.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        while True:
            try:
                data, addr = self.sock.recv(1024)
                message = data.decode()
                if message == "exit":
                    self.logger.debug("Received exit message")
                    self.sock.sendto(b"ok", addr)
                    break
                else:
                    try:
                        message_data = json.loads(message)
                        message_id = message_data["message_id"]
                        text = message_data["text"]
                        message_time = message_data["time"]
                        self.logger.debug(f"Received message {message_id} at {message_time}: {text}")
                    except json.JSONDecodeError as e:
                        self.logger.exception(f"Error parsing message {message}: {e}")
                    except KeyError as e:
                        self.logger.exception(f"Error processing message {message}: {e}")
            except socket.error as e:
                self.logger.exception(f"Socket error: {e}")
                time.sleep(1)

        self.sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receive UDP messages on a specified IP address and port number.")
    parser.add_argument("ip", type=str, help="the IP address to receive messages on")
    parser.add_argument("port", type=int, default=9999, help="the port number to receive messages on")
    args = parser.parse_args()

    # configure the logging module
    logging.basicConfig(filename="udp_log.log",
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)

    receiver = Receiver(args.ip, args.port)
    receiver.receive()
