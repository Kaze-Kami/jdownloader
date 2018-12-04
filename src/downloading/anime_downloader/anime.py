from bs4 import BeautifulSoup
from src.util.logging.logger import log, MessageType, MessageLevel

from src.connection.tor.tor_connection_manager import TorConnectionManager


class Anime:
    def __init__(self, base_url, parser, ongoing=False):
        self._ongoing = ongoing
        self._base_url = base_url
        self._parser = parser
        while True:
            html = self._get_html()
            try:
                self._name = parser.get_name(html)
                self._html = html
                break
            except Exception as e:
                log("Error parsing anime '%s', retrying. ex: %s" % (self._base_url, e), MessageType.WARN, MessageLevel.DEBUG)

        self._description = ''
        self._episodes_count = 0
        self._episodes = []
        self._cover_url = ''

    def prepare(self):
        log("Preparing anime '%s'" % self._name, MessageType.PROGRESS_START, MessageLevel.FULL_INFO)
        while True:
            try:
                self._description = self._parser.get_description(self._html)
                self._episodes = self._parser.get_episodes(self._base_url)
                self._episodes_count = len(self._episodes)
                self._cover_url = self._parser.get_cover_url(self._html)
                break
            except Exception as e:
                log("Error preparing anime '%s', retrying. ex: %s" % (self._name, e), MessageType.WARN, MessageLevel.DEBUG)
                self._html = self._get_html()

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

    @property
    def cover_url(self):
        return self._cover_url

    @property
    def ongoing(self):
        return self._ongoing

    def _get_html(self):
        con = TorConnectionManager().new_connection()
        con.acquire()
        raw = con.get(self._base_url).content
        con.release()
        return BeautifulSoup(raw, 'html.parser')


class Episode:
    def __init__(self, url, number, file_type='mp4'):
        self._number = number
        self._url = url
        self._file_type = file_type

    @property
    def number(self):
        return self._number

    @property
    def file_type(self):
        return self._file_type

    @property
    def url(self):
        return self._url
