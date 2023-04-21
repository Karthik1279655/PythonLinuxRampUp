import json
from datetime import datetime


class Message:
    # a class to represent a message
    def __init__(self, message_id, text, time):
        self.message_id = message_id
        self.text = text
        self.time = time

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_dict(cls, message_dict):
        message_dict['time'] = int(datetime.now().timestamp() * 1000)
        return cls(**message_dict)
