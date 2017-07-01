import os
import sys
import textwrap
from datetime import datetime
from threading import Thread

from src.util.logging.logger import MessageType, MessageLevel, log

from src.connection.tor.tor_connection_manager import TorConnectionManager
from src.downloading.file_downloader.download import Download
from src.downloading.file_downloader.download_manager import DownloadManager


class AnimeDownload(Thread):
    def __init__(self, anime, base_save_path):
        super().__init__()
        self._anime = anime
        self._save_path = base_save_path.joinpath(anime.name + '/')
        self._finish_listeners = []
        self._download_count = 0
        self._active_downloads = []

    @property
    def anime(self):
        return self._anime

    def run(self):
        self._prepare()
        self._download()

    def add_finish_listener(self, listener):
        self._finish_listeners.append(listener)

    def on_download_finished(self, anime_download):
        self._active_downloads.remove(anime_download)
        log("'%s': downloaded %d / %d" % (
            self._anime.name, self._download_count - len(self._active_downloads), self._download_count),
            MessageType.PROGRESS_ON_GOING, MessageLevel.MINIMAL_INFO)
        if 0 == len(self._active_downloads):
            self._on_finish()

    def _prepare(self):
        self._anime.prepare()
        log("Preparing download '%s'" % self._anime.name, MessageType.MESSAGE, MessageLevel.FULL_INFO)
        # ensure output directory
        if not os.path.exists(self._save_path):
            os.makedirs(self._save_path)
        con = TorConnectionManager().new_connection()
        con.acquire()
        # select not downloaded episodes
        for ep in self._anime.episodes:
            ep_save_path = self._save_path.joinpath('%d.mp4' % ep.number)
            gotten = False
            if os.path.exists(ep_save_path):
                ep_size = int(con.get(ep.url, stream=True).headers.get('Content-Length'))
                with open(ep_save_path, 'r'):
                    # check by size whether already downloaded
                    file_size = os.path.getsize(ep_save_path)
                    if file_size == ep_size:
                        gotten = True
            if not gotten:
                dl = Download(ep.url, ep_save_path)
                dl.add_finish_listener(self)
                self._active_downloads.append(dl)
                self._download_count += 1
            else:
                log("Skipping %s episode %d, already downloaded" % (self._anime.name, ep.number), MessageType.PROGRESS_FINISH, MessageLevel.NORMAL_INFO)
        con.release()

    def _download(self):
        if 0 < len(self._active_downloads):
            log("Starting '%s'" % self._anime.name, MessageType.PROGRESS_START, MessageLevel.MINIMAL_INFO)
            download_manager = DownloadManager()
            for dl in self._active_downloads:
                download_manager.en_que(dl)
        else:
            self._on_finish()

    def _on_finish(self):
        # write info file
        _write_info_file(self._anime, self._save_path)
        # write jacked file?
        _write_jacked_file(self._save_path)
        # todo download cover
        log('Finished %s' % self._anime.name, MessageType.PROGRESS_FINISH, MessageLevel.MINIMAL_INFO)
        for l in self._finish_listeners:
            l.on_download_finished(self)


def _write_info_file(anime, path):
    desc = textwrap.fill(text=anime.description, width=130)
    desc = desc.encode(sys.stdout.encoding, errors='replace')
    with open(path.joinpath('info.txt'), 'w') as f:
        f.write('%s (%s)\n%d Episodes\n\n%s' % (
            anime.base_url, anime.name, anime.episodes_count, desc))


def _write_jacked_file(path):
    with open(path.joinpath('jacked'), 'w') as f:
        f.write(datetime.now().strftime("%d. %m. %y, %H:%M"))
