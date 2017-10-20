import re

from bs4 import BeautifulSoup

from src.connection.tor.tor_connection_manager import TorConnectionManager
from src.downloading.anime_downloader.anime import Episode
from src.parsing.parser_error import ParseError


# parser for animeheaven.eu


def get_name(html):
    res = html.find_all('div', {'class': 'infodes'})
    if 0 == len(res):
        raise ParseError('Can\'t find name')
    return res[0].string


def get_description(html):
    res = html.find_all('div', {'class': 'infodes2'})
    if 0 == len(res):
        raise ParseError('Can\'t find description')
    return res[0].string


def get_episodes(url):
    episodes = []
    con = TorConnectionManager().new_connection()
    con.acquire()
    html = BeautifulSoup(con.get(url).content, 'html.parser')
    for link in html.find_all('a', href=re.compile('^watch.php?')):
        href = link.get('href')
        while True:
            # get episode nr
            ep_nr = int(re.findall(r'(?<==)\d+', href)[0])
            # print(href, ep_nr)
            player_html = con.get('http://animeheaven.eu/' + href).content.decode('utf-8')
            video_urls = re.findall(r'http.*?.mp4', player_html)
            nu = None
            for u in video_urls:
                if 'video' not in u:
                    nu = u
                    break
            if nu:
                episodes.append(Episode(nu, ep_nr))
                break
            con.change_ip()
    con.release()
    return sorted(episodes, key=lambda x: x.number)


def get_cover_url(html):
    for i in [t.get('src') for t in html.find_all('img')]:
        if 'posters' in i:
            return 'http://animeheaven.eu/' + i
    raise ParseError('Can\'t find cover url')
