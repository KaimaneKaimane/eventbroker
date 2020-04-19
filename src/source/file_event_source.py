import difflib
import time
from datetime import datetime
from pathlib import Path

import src.event.file as event
from src.source.event_source import EventSource


class FileEventSource(EventSource):
    def __init__(self, monitored_files: list):
        super().__init__()
        # Init the source with the initial file state
        self.monitored_files = monitored_files
        self.diff_checker = difflib.Differ()
        self.current_file_system = {}
        for file in monitored_files:
            if not file.is_dir():
                try:
                    with file.open() as file_handle:
                        self.current_file_system[str(file)] = file_handle.read()
                except FileNotFoundError:
                    self.current_file_system[str(file)] = None
                except Exception:
                    # ToDo catch some more file errors
                    pass

    def poll_events(self):
        while True:
            for file in self.monitored_files:
                diff_event = self._detect_file_changes(file)
                if diff_event is not None:
                    self.source_events.append(diff_event)
                time.sleep(0.100)

    def _format_diff(self, old_file_content, new_file_content):
        diff = list(self.diff_checker.compare(
            old_file_content.splitlines(),
            new_file_content.splitlines()
        ))
        return [line for line in diff if line[0] in ('+', '-')]

    def _detect_file_changes(self, file_path: Path):
        # Get the last file content
        old_file_content = self.current_file_system.get(str(file_path))
        try:
            with file_path.open() as file_handle:
                modified_time = time.ctime(file_path.stat().st_mtime)
                new_file_content = file_handle.read()

                if old_file_content is None:
                    # new file created
                    diff = self._format_diff('', new_file_content)
                    file_event_type = 'CREATED'
                else:
                    # check if diff
                    diff = self._format_diff(old_file_content, new_file_content)
                    file_event_type = 'DIFF'
                    if len(diff) == 0:
                        return None

                self.current_file_system[str(file_path)] = new_file_content

                return event.File(modified_time, file_event_type, file_path, diff)

        except FileNotFoundError:
            if old_file_content is None:
                # file is not there and there wasn't there last cycle
                return None
            else:
                # file was deleted
                diff = self._format_diff(old_file_content, '')
                file_event_type = 'DELETED'

                self.current_file_system[str(file_path)] = None
                return event.File(datetime.now(), file_event_type, file_path, diff)
        except Exception:
            # ToDo catch some more file errors
            pass
        return None
