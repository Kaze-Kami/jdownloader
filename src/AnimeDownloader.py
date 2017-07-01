import os
from datetime import datetime
from threading import Thread

from src.util.jutil import remove_line
from src.util.logging.logger import log, MessageType, MessageLevel

from src.connection.tor.tor_connection_manager import TorConnectionManager
from src.downloading.anime_downloader.anime import Anime
from src.downloading.anime_downloader.anime_download import AnimeDownload
from src.downloading.anime_downloader.anime_download_manager import AnimeDownloadManager
from src.downloading.file_downloader.download_manager import DownloadManager
# from src.parsing.anime_heaven_parser import AnimeHeavenParser
from src.parsing import anime_heaven_parser


class AnimeDownloader(Thread):
    def __init__(self, get_file_path, base_save_path):
        super().__init__()
        self._get_file_path = get_file_path
        time_string = datetime.now().strftime('gotten_%m_%d_%Y')
        self._gotten_file_path = get_file_path.parent.joinpath(time_string + ".txt")
        self._base_save_path = base_save_path
        self._urls = []
        self._active_downloads = []
        self._anime_download_manager = AnimeDownloadManager()
        self._download_manager = DownloadManager()

    def run(self):
        log('Starting anime downloader', MessageType.SYSTEM, MessageLevel.SYSTEM)
        self._prepare()
        if 0 == len(self._active_downloads):
            self._on_finish()

    def on_download_finished(self, anime_download):
        self._active_downloads.remove(anime_download)
        log('Downloaded %d of %d animes' % (len(self._urls) - len(self._active_downloads), len(self._urls)),
            MessageType.SYSTEM, MessageLevel.SYSTEM)
        if 0 == len(self._active_downloads):
            self._on_finish()

    def _prepare(self):
        # read get file
        self._urls = _read_get_file(self._get_file_path)

        # init downloads
        log('Downloading %d animes' % (len(self._urls)), MessageType.SYSTEM, MessageLevel.SYSTEM)
        self._anime_download_manager.start()
        self._download_manager.start()
        for url in self._urls:
            parser = _chose_parser(url)
            anime = Anime(url, parser)
            if not os.path.exists(self._base_save_path.joinpath(anime.name + "/jacked")):
                anime_download = AnimeDownload(anime, self._base_save_path)
                self._active_downloads.append(anime_download)
                anime_download.add_finish_listener(self)
                self._anime_download_manager.en_que(anime_download)
            else:
                log("Skipping '%s', already downloaded" % anime.name, MessageType.PROGRESS_FINISH,
                    MessageLevel.MINIMAL_INFO)
                _extend_gotten_file(anime, self._gotten_file_path)
                _truncate_get_file(anime, self._get_file_path)

    def _on_finish(self):
        log('All animes downloaded', MessageType.PROGRESS_FINISH, MessageLevel.SYSTEM)
        self._anime_download_manager.set_exit_flag()
        self._download_manager.set_exit_flag()
        TorConnectionManager().close_connections()
        log('Closing anime downloader', MessageType.SYSTEM, MessageLevel.SYSTEM)


def _read_get_file(get_file_path):
    with open(get_file_path, 'r') as get_file:
        lines = get_file.readlines()
        return [u.replace('\n', '') for u in lines if u != '\n' and u[0] != '#']


_parsers = {
    'animeheaven.eu': anime_heaven_parser
}


def _chose_parser(url):
    for k in _parsers.keys():
        if k in url:
            return _parsers[k]
    raise Exception("Unknown provider for url '%s'" % url)


def _extend_gotten_file(anime, gotten_file_path):
    url = anime.base_url
    with open(gotten_file_path, 'a') as f:
        f.write(url + '\n')


def _truncate_get_file(anime, get_file_path):
    url = anime.base_url
    with open(get_file_path, 'r') as rf:
        lines = rf.readlines()
    last_comment = 0
    for i, l in enumerate(lines):
        if 'http:' in l:
            break
        elif l[0] == '#':
            last_comment = i

    with open(get_file_path, 'w') as wf:
        for l in lines[last_comment:]:
            if l != url + '\n':
                wf.write(l)




