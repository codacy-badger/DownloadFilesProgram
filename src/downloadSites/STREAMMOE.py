#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import re

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
        title = soup.title.string.strip()
        return re.sub(r'[^(\w\d\-\[\])]', '', title) + '.mp4'

    def getFileURL(self, soup):
        try:
            # get script
            script = soup.find('div', attrs={'id': 'player_code'}).script
            scriptStr = str(script)
            # re
            pattern = re.compile('"(.+).mp4"')
            media_url = pattern.search(scriptStr).group(0)
            media_url = media_url.replace('"', '')
            return media_url
        except:
            raise


# === test code ===
# url = 'http://stream.moe/j8nimcnn9b5v'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# urlArray = aurl.split('/')

# x = run(url, urlArray)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
