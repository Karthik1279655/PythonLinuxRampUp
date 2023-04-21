import argparse
import socket
import struct
import multiprocessing
import pickle
import select

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="server hostname")
    parser.add_argument("port", type=int, help="server port")
    args = parser.parse_args()

    # Connect to server using TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.hostname, args.port))

        # Request key value for message queue from server
        s.sendall(b"request_key")
        key = s.recv(1024)
        key = int(key.decode())

        # Create message queue using key value
        message_queue = multiprocessing.Queue()
        message_queue._reader, message_queue._writer = \
            multiprocessing.Pipe(duplex=False)
        message_queue._reader.set_handle(key)

        # Request message type for employee data from server
        s.sendall(b"request_message_type")
        message_type = s.recv(1024)
        message_type = int(message_type.decode())

        # Request number of employee details needed from server
        num_employees = input("Enter number of employees: ")
        s.sendall(struct.pack("!I", num_employees))

        # Receive employee data from server using message queue
        for i in range(num_employees):
            ready, _, _ = select.select([s], [], [], 5.0)
            if ready:
                data = s.recv(1024)
                message_queue._writer.send(pickle.loads(data))
                employee_data = message_queue.get()
                print("Employee {}: {}".format(i+1, employee_data))
            else:
                print("Timeout waiting for employee data")
                break

if __name__ == "__main__":
    main()
