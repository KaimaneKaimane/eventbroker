from pathlib import Path
import time

from multiprocessing import Process
from multiprocessing.managers import BaseManager

from src.file_manager import FileManager

BaseManager.register('FileManager', FileManager)
manager = BaseManager()
manager.start()

file_dir = Path(__file__).parents[0]

monitored_files_test = [
    file_dir / Path('file_test_folder/somefile'),
    file_dir / Path('file_test_folder/somefile2'),
    file_dir / Path('file_test_folder/somefile3')
]


def file_manager_add(file_inst: FileManager, key):
    file_inst.add_consumer(key)


def file_manager_delete(file_inst: FileManager, key):
    file_inst.remove_consumer(key)


inst = manager.FileManager(monitored_files_test)

file_manager_process_1 = Process(target=file_manager_add, args=[inst, '#1'])
file_manager_process_2 = Process(target=file_manager_add, args=[inst, '#2'])
file_manager_process_3 = Process(target=file_manager_delete, args=[inst, '#1'])
file_manager_process_4 = Process(target=file_manager_delete, args=[inst, '#2'])

# start 1st consumer
file_manager_process_1.start()
time.sleep(5)
# start 2nd consumer (after 5 seconds)
file_manager_process_2.start()
time.sleep(10)
# delete 1st consumer (after 10/15 seconds)
file_manager_process_3.start()
time.sleep(15)
# delete 2nd consumer (after 15/30 seconds)
file_manager_process_4.start()

file_manager_process_1.join()
file_manager_process_2.join()
file_manager_process_3.join()
file_manager_process_4.join()

