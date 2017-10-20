import re
from bs4 import BeautifulSoup

from src.connection.tor.tor_connection_manager import TorConnectionManager
from src.downloading.anime_downloader.anime import Episode
from src.parsing.parser_error import ParseError


# parser for hentaicore.org


def get_name(html):
    res = html.find_all('h2', {'itemprop': 'name', 'class': 'top-title'})
    if 0 == len(res):
        raise ParseError('Can\'t find name')
    return res[0].string


def get_description(html):
    res = html.find_all('span', {'itemprop': 'description'})
    if 0 == len(res):
        raise ParseError('Can\'t find description')
    res = res[0].string
    if not res:
        return ''
    return res.replace(' Watch this hentai online and follow us in Twitter and Facebook!', '')


def get_episodes(url):
    episodes = []
    con = TorConnectionManager().new_connection()
    con.acquire()
    html = BeautifulSoup(con.get(url).content, 'html.parser')
    playlist = html.find('div', {'class': 'playlist'})
    if not playlist:
        raise ParseError('Can\'t find playlist')
    for link in playlist.find_all('button'):
        player_url = link.get('value').replace('//', 'http://')
        while True:
            # get episode nr
            ep_nr = int(re.findall(r'(?<=Episode )\d+', link.string)[0])
            # print(href, ep_nr)
            player_html = con.get(player_url).content.decode('utf-8')
            video_url = re.findall('https://fex.*?mp4', player_html)
            if 0 == len(video_url):
                raise ParseError("Can't find video url")
            else:
                episodes.append(Episode(video_url[0], ep_nr))
                break
            con.change_ip()
    con.release()
    return sorted(episodes, key=lambda x: x.number)


def get_cover_url(html):
    return None
