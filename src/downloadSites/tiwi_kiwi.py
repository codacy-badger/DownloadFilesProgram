#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import numpy as np

from bs4 import BeautifulSoup

from .AccessSite.OpenHTML import AccessPage


class run(object):
    """docstring for run"""
    def __init__(self, url, urlArray):
        super(run, self).__init__()
        self.urls = []
        # get type and soup
        st = SiteType(urlArray)
        soup = SoupURL(url)
        self.urls = self.getUrls(st.type, soup.s)

    def getUrls(self, urlType, soup):
        if urlType == 'media':
            listUrl = Media(soup).pref
        else:
            listUrl = []
        return listUrl


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, urlArray):
        super(SiteType, self).__init__()
        self.type = self.getType(urlArray)

    def getType(self, urlArray):
        if len(urlArray) == 2:
            urlType = 'media'   # media url
        else:
            urlType = None
        return urlType


class SoupURL(object):
    """docstring for SoupURL"""
    def __init__(self, url):
        super(SoupURL, self).__init__()
        self.s = self.getSoup(url)

    def getSoup(self, url):
        x = AccessPage(url)
        soup = BeautifulSoup(x.html)
        return soup


class Media(object):
    """docstring for Media"""
    def __init__(self, soup):
        super(Media, self).__init__()
        x = {}
        x['title'] = self.getTitle(soup)
        x['href'] = self.getFileURL(soup)
        self.pref = [x]

    def getTitle(self, soup):
        title = soup.find('h1', attrs={'class': 'h1'}).string.strip()
        name = re.sub(r'[^(\w\d\-\[\])]', '', title)
        return re.sub(r'\[.+?\]', '', name) + '.mp4'

    def getFileURL(self, soup):
        try:
            div = soup.body.find('div', attrs={'id': 'modal-17'})
            tds = div.findAll('td')
            links = []
            sizes = []
            for i in xrange(0, len(tds), 2):
                a = tds[i].a
                size_MB = tds[i+1].text.split(' ')[-2].strip()
                links.append(a)
                sizes.append(float(size_MB))
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
            media_url = self.getDirectDownloadLink(url)
            return media_url
        except:
            raise

    def getDirectDownloadLink(self, url):
        try:
            soup = SoupURL(url).s
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
# urlArray = aurl.split('/')

# x = run(url, urlArray)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
