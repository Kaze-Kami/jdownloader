import re
from bs4 import BeautifulSoup

from src.connection.tor.tor_connection_manager import TorConnectionManager
from src.downloading.anime_downloader.anime import Episode
from src.parsing.parser_error import ParseError


# parser for simply-hentai.com

def get_name(html):
    res = html.find_all('h1', {'class': 'margin-bottom-12'})
    if 0 == len(res):
        raise ParseError('Can\'t find name')
    return res[0].string


def get_description(html):
    return ""


def get_episodes(url):
    imgs = []
    con = TorConnectionManager().new_connection()
    con.acquire()
    m_url = url + "/all-pages"
    html = BeautifulSoup(con.get(m_url).content, 'html.parser')
    img_urls = re.findall('(?<="full":").*?jpg', html.text)
    if 1 == len(img_urls):
        raise ParseError("Can't find image urls!")
    img_nr = 0
    for img_url in img_urls:
        imgs.append(Episode(img_url, img_nr))
        img_nr += 1
    con.release()
    return imgs


def get_cover_url(html):
    return None
