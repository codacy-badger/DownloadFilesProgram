# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

from .helper import AccessPage


class Run(object):
    """docstring for Run"""
    def __init__(self, url, url_array):
        super(Run, self).__init__()
        self.urls = []
        # get type and soup
        st = SiteType(url_array)
        soup = SoupURL(url)
        urls = self.get_urls(st.type, soup.s)
        self.file_status = {'urls': urls, 'dir': 'h_video_place'}

    def get_urls(self, url_type, soup):
        if url_type == 'media':
            list_url = Media(soup).pref
        else:
            list_url = []
        return list_url


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, url_array):
        super(SiteType, self).__init__()
        self.type = self.get_type(url_array)

    def get_type(self, url_array):
        if 'movies' in url_array[1]:
            url_type = 'media'   # media url
        else:
            url_type = None
        return url_type


class SoupURL(object):
    """docstring for SoupURL"""
    def __init__(self, url):
        super(SoupURL, self).__init__()
        self.s = self.get_soup(url)

    def get_soup(self, url):
        x = AccessPage(url)
        soup = BeautifulSoup(x.html)
        return soup


class Media(object):
    """docstring for Media"""
    def __init__(self, soup):
        super(Media, self).__init__()
        x = {}
        x['title'] = self.get_title(soup)
        x['href'] = self.get_file_url(soup)
        self.pref = [x]

    def get_title(self, soup):
        title = soup.find('h1').string.strip()
        title = re.sub(r'[^(\w\d\-\[\])]', '', title) + '.flv'
        return title

    def get_file_url(self, soup):
        try:
            # get script
            scr = soup.find('script', attrs={'type': 'text/javascript'})
            scr_string = scr.string.replace('\\', '')
            # re
            pattern = re.compile('":\["(.+)"\]}')
            m = pattern.search(scr_string)
            media_url = m.group(1).split('"')[-1]
            return media_url
        except:
            raise


# === test code ===
# url = 'http://xhamster.com/movies/5141360/hentai_lets_play.html'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
