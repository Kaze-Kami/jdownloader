from threading import Thread

import time

from src.util.logging.logger_v2 import Logger, MessageType, MessageLevel, LogLevel, log
from src.util.singleton import Singleton

_download_limit = -1


def set_download_limit(download_limit):
    global _download_limit
    _download_limit = download_limit


class DownloadManager(Thread, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._que = []
        self._active = []
        self._exit_flag = False

    def run(self):
        log('Starting download manager', MessageType.SYSTEM, MessageLevel.SYSTEM)
        while not (self._exit_flag and 0 == len(self._active)):
            self._check()
            time.sleep(1)
        log('Closing download manager', MessageType.SYSTEM, MessageLevel.SYSTEM)

    def set_exit_flag(self):
        self._exit_flag = True

    def en_que(self, download):
        download.add_finish_listener(self)
        self._que.append(download)

    def on_download_finished(self, download):
        self._active.remove(download)

    def _check(self):
        while (-1 == _download_limit or len(self._active) < _download_limit) and 0 < len(self._que):
            up = self._que.pop(0)
            self._active.append(up)
            up.start()
