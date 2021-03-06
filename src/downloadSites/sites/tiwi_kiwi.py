#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import numpy as np
from bs4 import BeautifulSoup


from ._helper import AccessPage


class Run(object):
    """docstring for Run"""
    def __init__(self, url, url_array):
        super(Run, self).__init__()
        self.urls = []
        # get type and soup
        site_type = self._get_type(url_array)
        soup = _helper.get_soup(url)
        self.urls = self._get_urls(site_type, soup)

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
        title = soup.find('h1', attrs={'class': 'h1'}).string.strip()
        name = re.sub(r'[^(\w\d\-\[\])]', '', title)
        return re.sub(r'\[.+?\]', '', name) + '.mp4'

    def get_file_url(self, soup):
        try:
            div = soup.body.find('div', attrs={'id': 'modal-17'})
            tds = div.findAll('td')
            links = []
            sizes = []
            for i in xrange(0, len(tds), 2):
                a = tds[i].a
                size_mb = tds[i + 1].text.split(' ')[-2].strip()
                links.append(a)
                sizes.append(float(size_mb))
            sizes = np.asarray(sizes)
            a = links[np.argmax(sizes)]

            func = a['onclick']
            pattern = re.compile('\((.+)\)')
            values = pattern.search(func).group(0)
            values = re.sub(r"[\('\)]", '', values)
            values = values.split(',')
            url = (
                'http://tiwi.kiwi/dl?op=download_orig&id=' + values[0] +
                '&mode=' + values[1] +
                '&hash=' + values[2]
            )
            media_url = self.get_direct_download_link(url)
            return media_url
        except:
            raise

    def get_direct_download_link(self, url):
        try:
            soup = _helper.get_soup(url)
            media_url = soup.body.find(
                'a', attrs={'class': 'btn green'}
            )['href']
            return media_url
        except:
            raise


# === test code ===
# url = 'http://tiwi.kiwi/1k984qctacb2'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
