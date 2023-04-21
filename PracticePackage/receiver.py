#client
from udp_Task1 import Receiver

if __name__ == '__main__':
    receiver = Receiver(
        udp_ip="127.0.0.1",
        udp_port=5100
    )
    receiver.receive_messages()
    receiver.stop()
