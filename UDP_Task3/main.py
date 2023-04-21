import argparse
from udp_task3 import Transmitter, Receiver

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', help='Transmitter or Receiver', required=True)
    parser.add_argument('--ip', help='IP address', required=True)
    parser.add_argument('--port', help='Port number', required=True)
    parser.add_argument('--json', help='JSON file path')
    args = parser.parse_args()

    if args.type.lower() == 'transmitter':
        with Transmitter(args.ip, int(args.port), args.json) as transmitter:
            messages = transmitter.read_messages_from_file()
            if not messages:
                print(f"No messages found in {args.json}")
            for message in messages:
                transmitter.sendto_udp(message)
    elif args.type.lower() == 'receiver':
        with Receiver(args.ip, int(args.port), args.json) as receiver:
            receiver.run()
