#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-
import re
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
        self.filestatus = {'urls': urls, 'dir': 'h_manga_place'}

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
        if urlArray[1] == 'detail':
            global Title
            urlType = 'media'   # media url
            Title = urlArray[-1]
        elif urlArray[2] == 'index':
            urlType = 'index'   # search result
            if urlArray[-1] == 'SEQUENCE':
                if SeqFlag:
                    SeqFlag = False
                    urlType = 'sequence'   # search result
                else:
                    urlType = 'index'
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
        try:
            title = soup.title.string
            if title[0:5] == u'COMIC':
                title = u'[雑誌]' + title[5:]
            return title + '.zip'
        except:
            raise

    def getFileURL(self, soup):
        try:
            topUrl = "http://dropbooks.tv"
            fileURL = (
                topUrl
                +
                [
                    x.get("href")
                    for x in soup.body.div.findAll("a")
                    if x.get("href").count('download_zip')
                ][0]
            )
            return fileURL
        except:
            raise


class Index(object):
    """docstring for Index"""
    def __init__(self, soup):
        super(Index, self).__init__()
        self.pref = self.getMediaURL(soup)
        # filter
        buf = []
        for x in self.pref:
            if self.fileFilter(x['title']):
                buf += [x]
        self.pref = buf

    def getMediaURL(self, soup):
        tab_h3 = (
            soup.body.
            find('div', id="container").find('div', id="wrap").
            find('div', id="outline").find('div', id="main2col").
            findAll('h3')
        )
        # get title and url
        x = []
        for i in tab_h3:
            x += [i.find('a')]
        # convert url
        fix = []
        for i in x:
            url = (
                'http://dropbooks.tv/detail/download_zip/' +
                i['href'].split('/')[-1]
            )
            fix += [{
                'title': i['title'].replace('/', '_') + '.zip',
                'href': url
            }]
        return fix

    def fileFilter(self, title):
        title = title.strip()

        if re.match(r'^\[.+\](?!.+_\d).+$', title) is not None:
            return True
        elif re.match(u'^\((C|成年コミック|同人CG集).+\)*\[.+\](?!.+_\d).+$', title) is not None:
            return True
        elif re.match(r'^COMIC.+(?!.+_\d).+$', title) is not None:
            return True
        return False


class Sequence(object):
    """docstring for Sequence"""
    def __init__(self, soup, urlArray):
        super(Sequence, self).__init__()
        # init
        global SeqFlag
        stopTime = self.getLimit()
        self.pref = []
        # view time now
        d = datetime.datetime.today()
        print '--- Donwload Sequence dropBOOKS ---'
        print 'http://' + '/'.join(urlArray)
        print 'Start Time is %s/%s/%s %s:%s' % (
            d.year, d.month, d.day, d.hour, d.minute
        )
        # start analy
        del urlArray[-1]
        i = 1
        while True:
            print 'Scaning page:' + str(i) + '...'
            url = 'http://' + '/'.join(urlArray) + '/page:' + str(i)
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
        p_tab = soup.body.findAll('p', attrs={"class": "time"})
        times = []
        # get times
        for x in p_tab:
            timeStr = x.string[1:]
            timeStr = timeStr.replace(' ', '')
            timeStr = timeStr.replace('/', '').replace(':', '')
            times.append(int(timeStr))
        return min(times)


# === test code ===
# url = 'http://dropbooks.tv/tops/index/term:no/page:1'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# urlArray = aurl.split('/')

# x = run(url, urlArray)
# for media in x.urls:
#     print media['title']
#     print media['href']
#     print ''
