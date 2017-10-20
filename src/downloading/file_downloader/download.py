from threading import Thread

import sys

from src.util.logging.logger import log, MessageType, MessageLevel

from src.connection.tor.tor_connection_manager import TorConnectionManager


class Download(Thread):
    def __init__(self, url, save_path):
        super().__init__()
        self._url = url
        self._save_path = save_path
        self._con = None
        self._finish_listeners = []
        self._data_length = -1
        self._data_gotten = 0

    def add_finish_listener(self, listener):
        self._finish_listeners.append(listener)

    def _on_finish(self):
        for l in self._finish_listeners:
            l.on_download_finished(self)

    def run(self):
        self._prepare()
        log("Downloading '%s'" % self._url, MessageType.PROGRESS_START, MessageLevel.NORMAL_INFO)
        r = self._con.get(url=self._url, stream=True)
        with open(self._save_path, 'wb') as save_file:
            for arr in r.iter_content(4096):
                save_file.write(arr)
                self._data_gotten += len(arr)
                # print("Gotten %.1f%s of %s" % (self._data_gotten / self._data_length * 100, '%', self._url))
        log("Download '%s' finished" % self._url, MessageType.PROGRESS_FINISH, MessageLevel.NORMAL_INFO)
        self._con.release()
        self._on_finish()

    def _prepare(self):
        log("Preparing download '%s'" % self._url, MessageType.MESSAGE, MessageLevel.FULL_INFO)
        self._con = TorConnectionManager().new_connection()
        self._con.acquire()
        r = self._con.get(self._url, stream=True)
        self._data_length = int(r.headers.get('Content-Length'))

