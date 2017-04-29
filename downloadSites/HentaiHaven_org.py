#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import os
import re
import httplib
import urlparse
from BeautifulSoup import BeautifulSoup

from AccessSite.OpenHTML import AccessPage
import tiwi_kiwi


SeqFlag = True


class run(object):
    """docstring for run"""
    def __init__(self, url, urlArray):
        super(run, self).__init__()
        self.urls = []
        # get type and soup
        st = SiteType(urlArray)
        soup = SoupURL(url)
        urls = self.getUrls(st.type, soup.soup)
        self.filestatus = {'urls': urls, 'dir': 'h_anime_place'}

    def getUrls(self, urlType, soup):
        if urlType == 'media':
            listUrl = Media(soup).pref
        elif urlType == 'index':
            listUrl = Index(soup).pref
        else:
            listUrl = []
        return listUrl


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, urlArray):
        super(SiteType, self).__init__()
        self.type = self.getType(urlArray)

    def getType(self, urlArray):
        if 'episode' in urlArray[1]:
            urlType = 'media'
        else:
            urlType = 'index'
        return urlType


class SoupURL(object):
    """docstring for SoupURL"""
    def __init__(self, url):
        super(SoupURL, self).__init__()
        self.soup = self.getSoup(url)

    def getSoup(self, url):
        x = AccessPage(url)
        soup = BeautifulSoup(x.html)
        return soup


# === Single Download ===
class Media(object):
    """docstring for Media"""
    def __init__(self, soup):
        super(Media, self).__init__()
        x = {}
        x['title'] = self.getTitle(soup)
        # get download link
        x['href'] = self.getFileURL(soup)
        self.pref = [x]

    def getTitle(self, soup):
        try:
            title = soup.title.string.split("|")[0].strip()
            title = re.sub(r'[^(\w\d\-\[\])]', '', title)
            title = re.sub(r'[/]', '_', title) + '.mp4'
            return title
        except:
            raise

    def getFileURL(self, soup):
        shortURL = soup.article.find(
            "a", attrs={"class": "btn btn-1 btn-1e"}
        )["href"]
        url = self.expandShortenURL(shortURL)
        url = AccessPage(url).html.url
        if 'tiwi.kiwi' in url:
            url = self.getURL_fromTiwikiwi(url)
        return url

    def expandShortenURL(self, surl):
        parsed = urlparse.urlparse(surl)
        h = httplib.HTTPConnection(parsed.netloc)
        h.request('HEAD', parsed.path)
        response = h.getresponse()
        if response.status/100 == 3 and response.getheader('Location'):
            return response.getheader('Location')
        else:
            return surl

    def getURL_fromTiwikiwi(self, url):
        originurl = url
        url = url.replace('http://', '')
        urlArray = url.split('/')
        site = tiwi_kiwi.run(originurl, urlArray)
        fileURL = site.urls[0]['href'].encode("utf8")
        self.checkDL = True
        return fileURL


# === List Download ===
class Index(object):
    """docstring for Index"""
    def __init__(self, soup):
        super(Index, self).__init__()
        self.pref = []
        urls = self.getMediaURL(soup)
        for x in urls:
            try:
                l = {}
                soup = SoupURL(x).soup
                m = Media(soup)
                l['title'] = m.pref[0]['title']
                l['href'] = m.pref[0]['href'].encode("utf8")
                self.pref += [l]
            except:
                print 'Error: ' + x
            else:
                print x

    def getMediaURL(self, soup):
        a_tag = soup.findAll("a", attrs={"class": "thumbnail-image"})
        media_url = []
        for x in a_tag:
            media_url += [x['href']]
        return media_url


# === test code ===
# url = 'http://hentaihaven.org/rance-01-the-quest-for-hikari-episode-1/'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# urlArray = aurl.split('/')

# x = run(url, urlArray)
# for media in x.urls:
#     print media['title']
#     print media['href']
#     print ''
