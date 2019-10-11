import os, sys, time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging


# СОЗДАЕМ ЛОГГЕР
logger = logging.getLogger(__name__)


# PATH_TO_USER_UPLOAD_DIR
SRC = 'd:\Projects\py\myblog-development\curiosity\models.py'
# PATH_TO_SERVE_MEDIA_WIN10 
DST = 'd:\\media\\images\\'
# PATH_TO_LOGS
PATH_TO_LOGS = os.getcwd()+'\\media_files.log'

class ImageHandler(FileSystemEventHandler):
    def on_modified(self, event):
        return ps.kill("python")


# ПОЛУЧЕНИЕ ЛОГОВ
def get_logs():
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

    file_handler = logging.FileHandler(filename=PATH_TO_LOGS)
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)

    root_logger = logging.getLogger()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    root_logger.setLevel(logging.INFO)
    return root_logger


if __name__ == "__main__":
    
    root_logger = get_logs()
    
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=SRC, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()