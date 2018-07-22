#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import datetime

from BeautifulSoup import BeautifulSoup

from AccessSite.OpenHTML import AccessPage


SeqFlag = True

LimitTime = None


class run(object):
    """docstring for run"""
    def __init__(self, url, urlArray, limit=None):
        super(run, self).__init__()
        self.urls = []
        global LimitTime
        LimitTime = limit
        # get type and soup
        st = SiteType(urlArray)
        soup = SoupURL(url)
        urls = self.getUrls(st.type, soup.s, urlArray)
        self.filestatus = {'urls': urls, 'dir': 'h_pic_place'}

    def getUrls(self, urlType, soup, urlArray):
        if urlType == 'media':
            listUrl = Media(soup).pref
        elif urlType == 'index':
            listUrl = Index(soup).pref
        elif urlType == 'sequence':
            listUrl = Sequence(soup, urlArray).pref
        else:
            listUrl = []
        return listUrl


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, urlArray):
        super(SiteType, self).__init__()
        self.type = self.getType(urlArray)

    def getType(self, urlArray):
        global SeqFlag
        if urlArray[2] == 'archives':
            urlType = 'media'   # media url
        elif urlArray[-1] == 'SEQUENCE':
            if SeqFlag:
                SeqFlag = False
                urlType = 'sequence'   # search result
            else:
                urlType = 'index'
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
        self.parent = self.getFolderName(soup)
        self.pref = self.getMediaURL(soup)

    def getFolderName(self, soup):
        try:
            ds = u'わくてか速報 :'
            title = soup.title.string.strip(ds).split('-')[0].strip()
            title = title.replace('/', '_')
            return title
        except:
            raise

    def getMediaURL(self, soup):
        lib = []
        try:
            tag_a = soup.find(
                'div',
                attrs={"class": "article-body-more"}
            ).ol.findAll('a')
        except:     # this type is advertisement
            raise
        cnt = 0
        for x in tag_a:
            if '.jpg' in x['href']:
                title = x['href'].split('/')[-1]
                title = str(cnt).zfill(3) + title[-4:]
                cnt += 1
                lib += [{
                    'title': self.parent + '/' + title,
                    'href': x['href']
                }]
        return lib


class Index(object):
    """docstring for Index"""
    def __init__(self, soup):
        super(Index, self).__init__()
        url_list = self.getMediaURL(soup)
        self.pref = self.getPref(url_list)

    def getPref(self, url_list):
        buf = []
        for x in url_list:
            soup = SoupURL(x['href']).s
            try:
                buf += Media(soup).pref
            except:
                pass
        return buf

    def getMediaURL(self, soup):
        tag_h2 = soup.findAll(
            'h2',
            attrs={"class": "article-title entry-title"}
        )
        # get title and url
        x = []
        for i in tag_h2:
            x += [i.find('a')]
        # convert url
        fix = []
        for i in x:
            fix += [{
                'title': i.string,
                'href': i['href']
            }]
        return fix


class Sequence(object):
    """docstring for Sequence"""
    def __init__(self, soup, urlArray):
        super(Sequence, self).__init__()
        # init
        global SeqFlag
        stopTime = self.getLimit()
        i = 1
        self.pref = []
        # view time now
        d = datetime.datetime.today()
        print '--- Donwload Sequence わくてか速報 ---'
        print 'http://' + '/'.join(urlArray)
        print 'Start Time is %s/%s/%s %s:%s' % (
            d.year, d.month, d.day, d.hour, d.minute
        )
        # start analy
        del urlArray[-1]
        while True:
            print 'Scaning page:' + str(i) + '...'
            url = 'http://' + '/'.join(urlArray) + '/?p=' + str(i)
            soup = SoupURL(url).s
            self.pref += Index(soup).pref
            i += 1
            if self.getFilesDay(soup) < stopTime:
                break
        # Finish
        SeqFlag = True
        print ""

    def getLimit(self):
        global LimitTime
        # check LimitTime
        limitDay = LimitTime
        if limitDay is None:
            print 'Till when?'
            print 'ex. YYYY/MM/DD hh:mm'
            limitDay = raw_input('-> ')
        # check Str Type
        while True:
            LimitTime = limitDay
            limitDay = limitDay.replace(' ', '')
            limitDay = limitDay.replace('/', '').replace(':', '')
            if len(limitDay) == 12:
                return int(limitDay)
            else:
                print 'Oops!'
                limitDay = raw_input('-> ')

    def getFilesDay(self, soup):
        t = soup.body.findAll('abbr', attrs={"class": "updated"})
        times = []
        # get times
        for x in t:
            x = x['title']
            x = x.replace('-', '')
            x = x.replace('T', '')
            timeStr = str(x)
            array = timeStr.split(':')
            del array[-1]
            timeStr = ''.join(array)
            times += [int(timeStr)]
        return min(times)


# === test code ===
# 2015/10/01 00:00
# url = 'http://blog.livedoor.jp/wakusoku/SEQUENCE'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# urlArray = aurl.split('/')

# x = run(url, urlArray)
# for media in x.urls:
#     print media['title']
#     print media['href']
#     print ''
