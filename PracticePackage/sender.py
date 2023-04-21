#server
from udp_Task1 import Transmitter

if __name__ == '__main__':
    sender = Transmitter(
        udp_ip="127.0.0.1",
        udp_port=5100,
        json_file="messages.json"
    )
    sender.transmit_messages()
    sender.stop()

