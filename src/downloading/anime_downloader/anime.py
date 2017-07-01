from bs4 import BeautifulSoup
from src.connection.tor.tor_connection_manager import TorConnectionManager
from src.util.logging.logger_v2 import log, MessageType, MessageLevel


class Anime:
    def __init__(self, base_url, parser):
        self._base_url = base_url
        self._parser = parser
        self._html = self._get_html()
        self._name = parser.get_name(self._html)
        self._description = ''
        self._episodes_count = 0
        self._episodes = []

    def prepare(self):
        log("Preparing anime '%s'" % self._name, MessageType.PROGRESS_START, MessageLevel.NORMAL_INFO)
        self._description = self._parser.get_description(self._html)
        self._episodes = self._parser.get_episodes(self._base_url)
        self._episodes_count = len(self._episodes)

    @property
    def base_url(self):
        return self._base_url

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def episodes_count(self):
        return self._episodes_count

    @property
    def episodes(self):
        return self._episodes

    def _get_html(self):
        con = TorConnectionManager().new_connection()
        con.acquire()
        raw = con.get(self._base_url).content
        con.release()
        return BeautifulSoup(raw, 'html.parser')


class Episode:
    def __init__(self, url, number):
        self._number = number
        self._url = url

    @property
    def number(self):
        return self._number

    @property
    def url(self):
        return self._url
