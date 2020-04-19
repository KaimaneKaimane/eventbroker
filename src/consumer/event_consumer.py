from abc import ABC


class EventConsumer(ABC):
    def __init__(self, name):
        self.name = name

    def consume_next_event(self, event_source):
        pass
