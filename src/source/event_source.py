from abc import ABC


class EventSource(ABC):
    def __init__(self):
        self.source_events = []

    def get_source_events(self):
        return self.source_events

    def pop_earliest_event(self):
        earliest_event = self.source_events.pop() if self.source_events else None
        return earliest_event

    def poll_events(self):
        pass
