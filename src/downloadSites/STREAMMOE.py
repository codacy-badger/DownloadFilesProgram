#!/usr/bin/python
# -*- coding: utf-8 -*-


import re

from bs4 import BeautifulSoup

from .AccessSite.OpenHTML import AccessPage


class Run(object):
    """docstring for Run"""
    def __init__(self, url, url_array):
        super(Run, self).__init__()
        self.urls = []
        # get type and soup
        st = SiteType(url_array)
        soup = SoupURL(url)
        self.urls = self.get_urls(st.type, soup.s)

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
        if len(url_array) == 2:
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
        title = soup.title.string.strip()
        return re.sub(r'[^(\w\d\-\[\])]', '', title) + '.mp4'

    def get_file_url(self, soup):
        try:
            # get script
            script = soup.find('div', attrs={'id': 'player_code'}).script
            script_string = str(script)
            # re
            pattern = re.compile('"(.+).mp4"')
            media_url = pattern.search(script_string).group(0)
            media_url = media_url.replace('"', '')
            return media_url
        except:
            raise


# === test code ===
# url = 'http://stream.moe/j8nimcnn9b5v'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
