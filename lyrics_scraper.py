"""@uthor: Himaghna Bhattacharjee
   Scrape the lyrics for all Opeth songs from darklyrics.com.

"""
from argparse import ArgumentParser
from os import getcwd, mkdir
from os.path import isdir, join

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
        list of song lines.
        
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
            song_line = str(next_s).strip().lower()
            if song_line != '':
                song_lines.append(song_line)
    return song_lines


def get_album_page_urls(band_disco_url):
    """Extract the urls for individual urls from a band's discography page.
    
    Parameters
    ----------
    band_disco_url: str
        URL of the band discography page.
    
    Returns
    -------
    album_urls: list(str)
        list of the band's album urls.
    
    """
    PARENT_PAGE = 'http://www.darklyrics.com'
    discog_page = requests.get(band_disco_url)
    discog_soup = BeautifulSoup(discog_page.content, 'html.parser')
    album_urls = []
    for album in discog_soup.findAll('div', class_='album'):
        album_url = album.find('a', href=True)['href']
        # messy but necessary
        album_url = album_url.replace('..', PARENT_PAGE)
        album_urls.append(album_url)
    return album_urls


if __name__ == '__main__':
    DISCO_LINKS = {'opeth': 'http://www.darklyrics.com/o/opeth.html',
                   'porcupine_tree': 'http://www.darklyrics.com/p/porcupinetree.html'}
    parser = ArgumentParser()
    parser.add_argument('band',
                        help="Band for which corpus is needed."
                             "Currently implements 'opeth', 'porcupine_tree")
    parser.add_argument('-o', '--out_dir',
                        required=False, default=None,
                        help='File band_corpus.txt written to this directory')
    args = parser.parse_args()
    if args.band not in DISCO_LINKS.keys():
        raise NotImplementedError(f'{args.band} not in implemented bands: '
                                  f'{DISCO_LINKS.keys()}')
    album_urls = get_album_page_urls(DISCO_LINKS[args.band])
    text_corpus = [get_text_from_album_page(album_url)
                   for album_url in album_urls][0]  # [[]] -> []
    out_dir = args.out_dir
    if out_dir in [None, '.']:
        out_dir = getcwd()
    if not isdir(out_dir):
        print(f'Creating {out_dir}')
        mkdir(out_dir)        
    out_fpath = join(out_dir, f'lyrics_{args.band}.txt')
    print(f'Saving lyrics to file {out_fpath}')
    with open(out_fpath, "w", encoding="utf-8") as fp:
        for text_line in text_corpus:     
            fp.write('\n' + text_line)
    
    








#get_text_from_album_page('http://www.darklyrics.com/lyrics/opeth/orchid.html#1')
#print(get_album_page_urls('http://www.darklyrics.com/o/opeth.html'))
