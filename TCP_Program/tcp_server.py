import socket
import struct

class emp:
    def __init__(self, name="", id=0, age=0, gender=""):
        self.name = name
        self.id = id
        self.age = age
        self.gender = gender

def main():
    host = 'localhost'
    port = 12345

    # Create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a public host, and a well-known port
    serversocket.bind((host, port))

    # Become a server socket
    serversocket.listen(1)

    print(f"Server started on {host}:{port}")

    while True:
        # Accept connections from outside
        (clientsocket, address) = serversocket.accept()

        # Receive the key from the client
        key = struct.unpack('i', clientsocket.recv(4))[0]
        print(f"Client ({address[0]}:{address[1]}) key: {key}")

        # Create the message queue
        id = 0 # TODO: Implement msgget function

        # Receive the message type from the client
        mtype = struct.unpack('l', clientsocket.recv(8))[0]
        print(f"Client ({address[0]}:{address[1]}) mtype: {mtype}")

        # Receive the number of employee details to be sent by the client
        n = struct.unpack('i', clientsocket.recv(4))[0]
        print(f"Client ({address[0]}:{address[1]}) n: {n}")

        # Receive the employee details from the client
        for i in range(n):
            # Receive the employee details from the client
            e_data = clientsocket.recv(44) # 20+4+4+10 = 38 bytes + padding
            e = emp(*struct.unpack('20si10s', e_data))

            # TODO: Add employee data to message queue using msgsnd function

            print(f"Client ({address[0]}:{address[1]}) emp data {i+1}: {e.__dict__}")

        # Close the connection with the client
        clientsocket.close()

if __name__ == '__main__':
    main()
