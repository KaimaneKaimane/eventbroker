from multiprocessing import Process
from multiprocessing.managers import BaseManager

from src.manager import Manager
from src.source.file_event_source import FileEventSource
from src.consumer.file_event_consumer import FileEventConsumer

BaseManager.register('FileEventSource', FileEventSource)
manager = BaseManager()
manager.start()


def start_file_event_source(event_source):
    event_source.poll_events()


def start_file_event_consumer(event_source, key):
    event_consumer = FileEventConsumer(name=key)
    event_consumer.run(event_source)


class FileManager(Manager):
    def __init__(self, files_to_monitor: list):
        super().__init__()
        self.files_to_monitor = files_to_monitor
        self.consumers = {}
        self.source = None
        self.source_process = None

    def _create_event_source(self):
        self.source = manager.FileEventSource(self.files_to_monitor)
        self.source_process = Process(target=start_file_event_source, args=[self.source])
        self.source_process.start()
        print('BROKER CHANGE: Source created')

    def _delete_event_source(self):
        self.source_process.terminate()
        self.source_process = None
        self.source = None
        print('BROKER CHANGE: Source deleted')

    def _create_event_consumer(self, key):
        consumer_process = Process(target=start_file_event_consumer, args=[self.source, key])
        consumer_process.start()
        print('BROKER CHANGE: Consumer created', key)
        self.consumers[key] = consumer_process

    def _delete_event_consumer(self, key):
        self.consumers[key].terminate()
        del self.consumers[key]
        print('BROKER CHANGE: Consumer deleted', key)

    def add_consumer(self, consumer_key):
        print(self.consumers)
        if len(self.consumers) > 0:
            if consumer_key in self.consumers:
                print('Consumer key already in use')
                return

            self._create_event_consumer(consumer_key)
            self.consumers[consumer_key].join()
        else:
            self._create_event_source()
            self._create_event_consumer(consumer_key)
            self.source_process.join()
            if self.consumers.get(consumer_key) is not None:
                self.consumers[consumer_key].join()

    def remove_consumer(self, consumer_key):
        if consumer_key not in self.consumers:
            print('Consumer key not in consumers')
            return

        if len(self.consumers) > 1:
            self._delete_event_consumer(consumer_key)
        else:
            self._delete_event_consumer(consumer_key)
            self._delete_event_source()

