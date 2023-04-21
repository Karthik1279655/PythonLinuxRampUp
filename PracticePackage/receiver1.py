import argparse
import signal
from transmitterUDP import Receiver

if __name__ == "__main__":
    # create an argument parser
    parser = argparse.ArgumentParser(description="UDP Message Receiver")

    # add arguments for IP address, port number, and JSON file name
    parser.add_argument("ip", type=str, help="UDP IP address to bind the socket to")
    parser.add_argument("port", type=int, help="UDP port number to bind the socket to")
    parser.add_argument("json_file", type=str, help="JSON file to save received messages to")

    # parse the command-line arguments
    args = parser.parse_args()

    # create a receiver object
    receiver = Receiver(args.ip, args.port, args.json_file)

    try:
        # start receiving messages
        receiver.receive_messages()
    except KeyboardInterrupt:
        # if the user presses Ctrl+C, stop the receiver
        receiver.signal_handler(signal.SIGINT, None)
