# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup

from . import _helper


class Run(object):
    """docstring for Run"""
    def __init__(self, url, url_array):
        super(Run, self).__init__()
        self.urls = []
        # get type and soup
        site_type = self._get_type(url_array)
        soup = _helper.get_soup(url)
        urls = self._get_urls(site_type, soup)
        self.file_status = {'urls': urls, 'dir': 'h_video_place'}

    def _get_urls(self, url_type, soup):
        if url_type == 'media':
            list_url = Media(soup).pref
        else:
            list_url = []
        return list_url

    def _get_type(self, url_array):
        if len(url_array) == 2:
            url_type = 'media'   # media url
        else:
            url_type = None
        return url_type


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
        title = re.sub(r'[^(\w\d\-\[\])]', '', title) + '.mp4'
        return title

    def get_file_url(self, soup):
        # get script
        script = soup.select_one('#redtube-player > script:nth-of-type(2)')
        scr_string = script.string.replace('\\', '')
        # re
        strings = scr_string.split('"videoUrl":"')[1:]
        pattern = re.compile(r'(http.+)"\}')
        urls = []
        for s in strings:
            m = pattern.search(s)
            urls.append(m.group(1))
        media_url = urls[0]
        return media_url



# === test code ===
# url = 'https://www.redtube.com/8522831'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
