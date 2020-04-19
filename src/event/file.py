from pathlib import Path

from src.event.base import Base


class File(Base):
    def __init__(self, modified_time, file_event_type: str, file_name: Path, diff: list):
        super().__init__(modified_time)
        self.file_event_type = file_event_type
        self.file_name = file_name
        self.diff = diff

    def __str__(self):
        representation = super().__str__() + '\n'
        representation += 'file_event_type: ' + self.file_event_type + '\n'
        representation += 'file_name: ' + str(self.file_name) + '\n'
        representation += 'diff: ' + str(self.diff) + '\n'
        return representation
