import pytest
from sender_UDP import Message, Transmitter
import json
from receiver import Receiver
from contextlib import contextmanager
import socket


def test_load_messages_from_file():
    # load a file with messages
    file_path = 'messages.json'
    with open(file_path, 'r') as f:
        json.load(f)

    # Test the load_messages_from_file method
    with Transmitter(file_path, 'localhost', 5000) as transmitter:
        loaded_messages = transmitter.load_messages_from_file()
        assert len(loaded_messages) == 2
        assert loaded_messages[0].text == 'Hello'
        assert loaded_messages[1].message_id == '2'

    # Test the method with a non-exist file
    with Transmitter('nonexist.json', 'localhost', 5000) as transmitter:
        loaded_messages = transmitter.load_messages_from_file()
        assert len(loaded_messages) == 0


def test_read():
    with Transmitter('messages.json', 'localhost', 5000) as transmitter:
        message = transmitter.read('1')
        assert message.text == 'Hello'
