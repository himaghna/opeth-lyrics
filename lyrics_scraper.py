"""@uthor: Himaghna Bhattacharjee
   Scrape the lyrics for all Opeth songs from darklyrics.com.

"""

import requests
from bs4 import BeautifulSoup, NavigableString, Tag


def get_text_from_album_page(album_url):
    """
    Parameters
    ----------
    album_url: str
        URL of the song page.

    Returns
    -------
    list(str)
        list of song lines
        
    """
    album_page = requests.get(album_url)
    album_soup = BeautifulSoup(album_page.content, 'html.parser')
    album_lyrics_elems = album_soup.find('div', class_='lyrics')

    song_lines = []
    for br in album_lyrics_elems.findAll('br'):
        next_s = br.nextSibling
        if not (next_s and isinstance(next_s, NavigableString)):
            continue
        next_2s = next_s.nextSibling
        if next_2s and isinstance(next_2s, Tag) and next_2s.name == 'br':
            song_line = str(next_s).strip()
            if song_line != '':
                song_lines.append(song_line)





get_text_from_album_page('http://www.darklyrics.com/lyrics/opeth/orchid.html#1')
