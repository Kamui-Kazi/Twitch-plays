import queue
from random import random

MSG_CHANCE = 0.1


class Messages:
    messages = queue.SimpleQueue()

    @classmethod
    def put(cls, _msg: str) -> None:
        if random() < MSG_CHANCE:
            cls.messages.put(_msg)

    @classmethod
    def get(cls) -> str:
        if cls.messages.empty():
            return ""
        return cls.messages.get()
