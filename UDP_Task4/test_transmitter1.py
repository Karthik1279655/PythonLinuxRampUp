import json
from unittest.mock import MagicMock, patch
import pytest
import datetime
from transmitter import Transmitter, Message


@pytest.fixture(scope="module")
def transmitter():
    return Transmitter("127.0.0.1", 1234, "messages.json")


def test_read_messages_from_file(transmitter):
    messages = transmitter.read_messages_from_file()
    assert len(messages) == 3
    assert isinstance(messages[0], Message)
    assert messages[0].message_id == 1
    assert messages[0].text == "Hello! Karthik"
    assert isinstance(messages[0].time, int)


def test_sendto_udp(transmitter):
    with patch.object(transmitter, "_send_message") as mock_send:
        message = Message(1, "Hello! Karthik", 123456789)
        transmitter.sendto_udp(message)
        mock_send.assert_called_once_with(message)


def test_send_all_messages(transmitter):
    with patch.object(transmitter, "read_messages_from_file") as mock_read:
        messages_data = [
            {"message_id": 1, "text": "Hello! Karthik", "time": "2023-04-05T19:46:00Z"},
            {"message_id": 2, "text": "How are you?", "time": "2023-04-05T19:46:00Z"},
            {"message_id": 3, "text": "I'm doing well", "time": "2023-04-05T19:46:00Z"},
        ]
        messages = [Message.from_dict(data) for data in messages_data]
        mock_read.return_value = messages

        with patch.object(transmitter, "sendto_udp") as mock_send:
            transmitter.send_all_messages()
            assert mock_send.call_count == 3
            mock_send.assert_any_call(messages[0])
            mock_send.assert_any_call(messages[1])
            mock_send.assert_any_call(messages[2])


def test_from_dict():
    message_data = {"message_id": 1, "text": "Hello! Karthik", "time": "2023-04-05T19:46:00Z"}
    message = Message.from_dict(message_data)
    assert message.message_id == 1
    assert message.text == "Hello! Karthik"
    assert isinstance(message.time, int)


def test_to_json():
    message = Message(1, "Hello! Karthik", 123456789)
    expected_json = json.dumps({"message_id": 1, "text": "Hello! Karthik", "time": 123456789})
    assert message.to_json() == expected_json
