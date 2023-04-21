import pytest
from transmitter_tcp import TCPTransmitter
from receiver_tcp import TCPReceiver


@pytest.fixture(scope="module")
def receiver():
    # setup the receiver instances
    receiver = TCPReceiver("localhost", 5100)
    yield receiver
    receiver.close()


@pytest.fixture(scope="module")
def transmitter():
    # setup the transmitter instances
    transmitter = TCPTransmitter("localhost", 5100)
    yield transmitter
    transmitter.close()


def test_read_message(transmitter):
    message = transmitter.read_message()
    assert isinstance(message, str)


def test_parse_message(transmitter):
    message = transmitter.read_message()
    tcp_data = transmitter.parse_message(message)
    assert isinstance(tcp_data, object)
