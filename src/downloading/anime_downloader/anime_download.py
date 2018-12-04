import ctypes
import os
import textwrap
from datetime import datetime
from threading import Thread

from src.util.jutil import to_usable_path
from src.util.logging.logger import MessageType, MessageLevel, log

from src.connection.tor.tor_connection_manager import TorConnectionManager
from src.downloading.file_downloader.download import Download
from src.downloading.file_downloader.download_manager import DownloadManager


class AnimeDownload(Thread):
    def __init__(self, anime, base_save_path):
        super().__init__()
        self._anime = anime
        self._save_path = base_save_path.joinpath(to_usable_path(anime.name) + '/')
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
            # todo: changed from '%d.mp4' as update for simply-hentai, needs update for other providers aswell so the fileytpe is provided!
            # todo: Episode class provides an default constructor taking the same arguments as before assuming mp4 as default for file_type to provide backwards compatibility
            ep_save_path = self._save_path.joinpath('%d.%s' % (ep.number, ep.file_type))
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
                log("Skipping %s episode %d, already downloaded" % (self._anime.name, ep.number), MessageType.PROGRESS_FINISH, MessageLevel.FULL_INFO)
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
        if self._anime.cover_url:
            cover_save_path = self._save_path.joinpath('cover.png')
            dl = Download(self._anime.cover_url, cover_save_path)
            dl.start()
            dl.join()
        # write info file
        _write_info_file(self._anime, self._save_path)
        # write jacked file?
        _write_jacked_file(self._save_path)
        log('Finished %s' % self._anime.name, MessageType.PROGRESS_FINISH, MessageLevel.MINIMAL_INFO)
        for l in self._finish_listeners:
            l.on_download_finished(self)


def _write_info_file(anime, path):
    title = ('%s (%s)%s' % (anime.base_url, anime.name, os.linesep)).encode(errors='replace')
    episode_count = ('%d Episodes%s%s' % (anime.episodes_count, os.linesep, os.linesep)).encode(errors='replace')
    desc = textwrap.fill(text=anime.description, width=100).replace('\n', os.linesep).encode(errors='replace')
    path = path.joinpath('info.txt')
    with open(path, 'wb') as f:
        f.write(title)
        f.write(episode_count)
        f.write(desc)


def _write_jacked_file(path):
    p = path.joinpath('jacked')
    if os.path.exists(p):
        os.remove(p)
    with open(p, 'w') as f:
        f.write(datetime.now().strftime("%d. %m. %y, %H:%M"))
        os.system("attrib +h " + ('"%s"' % p))
