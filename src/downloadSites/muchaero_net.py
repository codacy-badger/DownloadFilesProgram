#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import datetime

from AccessSite.OpenHTML import SoupURL


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
        if urlArray[-1].isdigit():
            urlType = 'media'   # media url
        elif urlArray[-1] == 'SEQUENCE':
            if SeqFlag:
                SeqFlag = False
                urlType = 'sequence'   # search result
            else:
                urlType = 'index'
        return urlType


class Media(object):
    """docstring for Media"""
    def __init__(self, soup):
        super(Media, self).__init__()
        self.parent = self.getFolderName(soup)
        self.pref = self.getMediaURL(soup)

    def getFolderName(self, soup):
        try:
            title = soup.title.string.split('|')[0].strip()
            title = title.replace('/', '_')
            return title
        except:
            raise

    def getMediaURL(self, soup):
        try:
            div_tags = soup.find(
                'div', attrs={'class': 'entry-content'}
            )
            img_tag = div_tags.findAll('img')
        except:     # this type is advertisement
            raise
        x = []
        cnt = 0
        for i in range(0, len(img_tag), 2):
            url = img_tag[i]['data-lazy-src']
            if '.jpg' in url:
                title = str(cnt).zfill(3) + url[-4:]
                cnt += 1
                x += [{
                    'title': self.parent + '/' + title,
                    'href': url
                }]
        return x


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
                print 'Error'
                pass
        return buf

    def getMediaURL(self, soup):
        h2_tag = soup.findAll('h2')
        del h2_tag[0]
        # get title and url
        x = []
        for i in h2_tag:
            a = i.a
            if a['href'] is not None:
                x += [{
                    'title': a.string.encode('utf-8'),
                    'href': a['href'].encode('utf-8')
                }]
        return x


class Sequence(object):
    """docstring for Sequence"""
    def __init__(self, soup, urlArray):
        super(Sequence, self).__init__()
        # init
        global SeqFlag
        # stopTime = self.getLimit()
        i = 1
        self.pref = []
        # view time now
        d = datetime.datetime.today()
        print '--- Donwload Sequence むちゃエロ二次元画像まとめ ---'
        print 'http://' + '/'.join(urlArray)
        print 'Start Time is %s/%s/%s %s:%s' % (
            d.year, d.month, d.day, d.hour, d.minute
        )
        # start analy
        del urlArray[-1]
        # this site doesn't have date-data,
        # so SEQUENCE is to scan 3 pages
        for i in range(1, 4):
            print 'Scaning page:' + str(i) + '...'
            url = 'http://' + '/'.join(urlArray) + '/' + str(i)
            soup = SoupURL(url).s
            self.pref += Index(soup).pref
            # i += 1
            # if self.getFilesDay(soup) < stopTime:
            #     break
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
        li_tag = soup.findAll('li', attrs={'class': 'cal'})
        times = []
        # get times
        for x in li_tag:
            if x.text is not None:
                x = x.text
                x = x.replace(u'年', '')
                x = x.replace(u'月', '')
                x = x.replace(u'日 ', '')
                x = x.replace(':', '')
                times += [int(x)]
        return min(times)


# === test code ===
# 2016/02/21 20:00
# url = 'http://moeimg.net/8836.html'
# url = 'http://muchaero.net/page/SEQUENCE'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# urlArray = aurl.split('/')

# x = run(url, urlArray)
# for media in x.urls:
#     print media['title']
#     print media['href']
#     print ''
