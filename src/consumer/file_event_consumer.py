import time

from src.consumer.event_consumer import EventConsumer
from src.source.file_event_source import FileEventSource


class FileEventConsumer(EventConsumer):
    def __init__(self, name):
        super().__init__(name)
        pass

    def consume_next_event(self, event_source: FileEventSource):
        first_event = event_source.pop_earliest_event()
        if first_event is not None:
            print('------- CONSUMER', self.name + ' -------')
            print(first_event)
            print('---------------------------')

    def run(self, event_source: FileEventSource):
        while event_source is not None:
            self.consume_next_event(event_source)
            time.sleep(0.100)
