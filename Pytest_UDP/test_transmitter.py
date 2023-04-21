import json
import signal
import time
from contextlib import contextmanager
from socket import AF_INET, SOCK_DGRAM, socket
import pytest
from Pytest_UDP.messages import Message
from Pytest_UDP.transmitter import Transmitter


@contextmanager
def udp_socket():
    # create a UDP socket
    sock = socket(AF_INET, SOCK_DGRAM)

    try:
        yield sock
    finally:
        sock.close()


@pytest.fixture
def messages():
    json_file = 'messages.json'
    with open(json_file, 'r') as file:
        messages_data = json.load(file)
    # load a file with messages
    messages = []
    for message_data in messages_data:
        message = Message.from_dict(message_data)
        messages.append(message)
    return messages


@pytest.fixture
def transmitter(messages):
    with udp_socket() as sock:
        # create a transmitter object
        transmitter = Transmitter('localhost', 5000, messages)

        yield transmitter

        # clean up after the test is finished
        transmitter.stop()


def test_read_messages_length(messages):
    assert len(messages) == 3


def test_read(transmitter, messages):
    assert transmitter.messages == messages


def test_signal_handler():
    # create a mock signal and frame
    mock_sig = signal.SIGINT

    # use pytest.raises() to catch the SystemExit exception
    with pytest.raises(SystemExit) as exc_info:
        # call the signal_handler function
        signal_handler(mock_sig, None)

    # verify that the exception has a value of 0
    assert exc_info.value.code == 0


def test_stop(transmitter):
    assert transmitter.sock is not None
    transmitter.stop()
    time.sleep(1)  # Add a sleep call to allow the stop() method to complete
    assert transmitter.sock is None
