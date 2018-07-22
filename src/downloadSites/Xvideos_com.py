#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import os
import re
import time
from html.parser import HTMLParser

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
        urls = self.getUrls(st.type, soup.s)
        self.filestatus = {'urls': urls, 'dir': 'h_video_place'}

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
        if 'video' in urlArray[1]:
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
        title_str = soup.title.string
        title = title_str.split("- XVIDEOS")[0].split("(")[0].strip()
        title = re.sub(r'[^(\w\d\-\[\])]', '', title)
        if len(title) == 0:
            title = 'ut' + str(int(time.time()))
        title = title + '.mp4'
        return title

    def getFileURL(self, soup):
        try:
            js = soup.find('div', attrs={'id': 'video-player-bg'})
            scr = js.findAll('script')
            scrStr = ''
            scr = [str(i.string) for i in scr]
            scr = '\n'.join(scr)
            scrStr = scr.replace('\\', '')

            # get functions for video url
            pattern = r"html5player\.setVideoUrl.+(http.+)'\);" # ()で囲まれた部分だけ返す
            m = re.findall(pattern, scrStr)
            url = m[-1] # get only high quarity video url
            url = HTMLParser.HTMLParser().unescape(url)    # fix encoding bug
            return url
        except:
            raise


# === test code ===
# url = 'https://www.xvideos.com/video14042415/teen_can_t_wait_gets_off_in_public_bathroom'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# urlArray = aurl.split('/')

# x = run(url, urlArray)
# for media in x.filestatus['urls']:
#     print(media['title'])
#     print(media['href'])
#     print('')
