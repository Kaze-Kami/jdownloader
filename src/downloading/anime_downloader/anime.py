from bs4 import BeautifulSoup
from src.util.logging.logger import log, MessageType, MessageLevel

from src.connection.tor.tor_connection_manager import TorConnectionManager


class Anime:
    def __init__(self, base_url, parser):
        self._base_url = base_url
        self._parser = parser
        while True:
            try:
                html = self._get_html()
                self._name = parser.get_name(self._html)
                self._html = html
                break
            except Exception as e:
                log("Error parsing anime '%s', retrying. ex: %s" % (self._base_url, e), MessageType.WARN, MessageLevel.DEBUG)
        self._description = ''
        self._episodes_count = 0
        self._episodes = []

    def prepare(self):
        log("Preparing anime '%s'" % self._name, MessageType.PROGRESS_START, MessageLevel.FULL_INFO)
        while True:
            try:
                self._description = self._parser.get_description(self._html)
                self._episodes = self._parser.get_episodes(self._base_url)
                self._episodes_count = len(self._episodes)
                break
            except Exception as e:
                log("Error preparing anime '%s', retrying. ex: %s" % (self._name, e), MessageType.WARN, MessageLevel.DEBUG)

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
