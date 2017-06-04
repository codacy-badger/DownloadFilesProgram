#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import os
import re
from BeautifulSoup import BeautifulSoup

from OpenHTML import AccessPage
import tiwi_kiwi
import STREAMMOE


SeqFlag = True


class run(object):
    """docstring for run"""
    def __init__(self, url, urlArray):
        super(run, self).__init__()
        self.urls = []
        # get type and data
        st = SiteType(urlArray)
        data = DataHTML(url)
        urls = self.getUrls(st.type, data)
        self.filestatus = {'urls': urls, 'dir': 'anime_place'}

    def getUrls(self, urlType, data):
        if urlType == 'media':
            listUrl = Media(data).pref
        elif urlType == 'index':
            listUrl = Index(data).pref
        else:
            listUrl = []
        return listUrl


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, urlArray):
        super(SiteType, self).__init__()
        self.type = self.getType(urlArray)

    def getType(self, urlArray):
        if urlArray[1] == 'subbed' or urlArray[1] == 'dubbed':
            urlType = 'media'
        elif urlArray[1] == 'episodes':
            urlType = 'index'
        else:
            urlType = None
        return urlType


class DataHTML(object):
    """docstring for DataHTML"""
    def __init__(self, url):
        super(DataHTML, self).__init__()
        x = AccessPage(url, browser=True)
        self.soup = self.getSoup(x)
        self.driver = self.getDriver(x)

    def getSoup(self, x):
        soup = BeautifulSoup(x.html)
        return soup

    def getDriver(self, x):
        driver = x.driver
        return driver


# === Single Download ===
class Media(object):
    """docstring for Media"""
    def __init__(self, data):
        super(Media, self).__init__()
        x = {}
        x['title'] = self.getTitle(data.soup)
        # get download link
        x['href'] = self.getFileURL(data)
        self.pref = [x]

    def getTitle(self, soup):
        try:
            title = soup.title.string.split("|")[0].strip()
            title = re.sub(r'[/]', '_', title) + '.mp4'
            title = title
            return title
        except:
            raise

    def getFileURL(self, data):
        self.checkDL = False
        soup = data.soup
        driver = data.driver
        url = ''
        if not self.checkDL:
            url = self.getURL_fromSTREAMMOE(data)
        if not self.checkDL:
            url = self.getURL_fromDownloadLink(soup)
        if not self.checkDL:
            url = self.getURL_fromDirectly(soup)
        if not self.checkDL:
            url = self.getURL_fromTIWIKIWI(soup)
        return url

    def getURL_fromTIWIKIWI(self, soup):
        try:
            downloadLink = soup.find(
                'div',
                attrs={'class': 'download_feed_link'}
            ).a['href']
            if 'google' in downloadLink:
                self.checkDL = True
                return downloadLink
            url = downloadLink.replace('http://', '')
            urlArray = url.split('/')
            site = tiwi_kiwi.run(downloadLink, urlArray)
            fileURL = site.urls[0]['href'].encode("utf8")
            self.checkDL = True
            return fileURL
        except:
            self.checkDL = False

    def getURL_fromSTREAMMOE(self, data):
        driver = data.driver
        try:
            iframes = driver.find_elements_by_tag_name('iframe')
            driver.switch_to.frame(iframes[2])
            iframes = driver.find_elements_by_tag_name('iframe')
            driver.switch_to.frame(iframes[0])

            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html)
            video = soup.find('video')
            fileURL = video.source['src']

            self.checkDL = True
            return fileURL
        except:
            self.checkDL = False

    def getURL_fromDownloadLink(self, soup):
        try:
            a_s = soup.findAll('a', attrs={'class': 'download-btn-inline'})
            fileURL = sources[0]['href'].encode("utf8")
            self.checkDL = True
            return fileURL
        except:
            self.checkDL = False

    def getURL_fromDirectly(self, soup):
        try:
            video = soup.find('video')
            sources = video.findAll('source')

            fileURL = sources[0]['src'].encode("utf8")
            self.checkDL = True
            return fileURL
        except:
            self.checkDL = False


# === List Download ===
class Index(object):
    """docstring for Index"""
    def __init__(self, data):
        super(Index, self).__init__()
        self.pref = []
        urls = self.getMediaURL(data.soup)
        for x in urls:
            try:
                l = {}
                data = DataHTML(x)
                m = Media(data)
                l['title'] = m.pref[0]['title']
                l['href'] = m.pref[0]['href'].encode("utf8")
                self.pref += [l]
            except:
                print 'Error: ' + x
            else:
                print x

    def getMediaURL(self, soup):
        tag_h2 = soup.findAll('h2', attrs={'class': 'entry-title'})
        media_url = []
        for x in tag_h2:
            media_url += [x.a['href']]
        return media_url


# === test code ===
# url = 'http://animehaven.org/subbed/one-punch-man-episode-7'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# urlArray = aurl.split('/')

# x = run(url, urlArray)
# for media in x.urls:
#     print media['title']
#     print media['href']
#     print ''
