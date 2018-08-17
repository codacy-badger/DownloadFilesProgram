# -*- coding: utf-8 -*-

import datetime
from bs4 import BeautifulSoup

from . import _helper


SeqFlag = True
LimitTime = None


class Run(object):
    """docstring for Run"""
    def __init__(self, url, url_array, limit=None):
        super(Run, self).__init__()
        self.urls = []
        global LimitTime
        LimitTime = limit
        # get type and soup
        site_type = self._get_type(url_array)
        soup = _helper.get_soup(url)
        urls = self._get_urls(site_type, soup, url_array)
        self.file_status = {'urls': urls, 'dir': 'h_pic_place'}

    def _get_urls(self, url_type, soup, url_array):
        if url_type == 'media':
            list_url = Media(soup).pref
        elif url_type == 'index':
            list_url = Index(soup).pref
        elif url_type == 'sequence':
            list_url = Sequence(soup, url_array).pref
        else:
            list_url = []
        return list_url

    def _get_type(self, url_array):
        global SeqFlag
        if url_array[2] == 'archives':
            url_type = 'media'   # media url
        elif url_array[-1] == 'SEQUENCE':
            if SeqFlag:
                SeqFlag = False
                url_type = 'sequence'   # search result
            else:
                url_type = 'index'
        return url_type


class Media(object):
    """docstring for Media"""
    def __init__(self, soup):
        super(Media, self).__init__()
        self.parent = self.get_dir_name(soup)
        self.pref = self.get_media_url(soup)

    def get_dir_name(self, soup):
        ds = u'わくてか速報 :'
        title = soup.title.string.strip(ds).split('-')[0].strip()
        title = title.replace('/', '_')
        return title

    def get_media_url(self, soup):
        lib = []
        tag_a = soup.find(
            'div',
            attrs={"class": "article-body-more"}
        ).ol.findAll('a')
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
        url_list = self.get_media_url(soup)
        self.pref = self.get_pref(url_list)

    def get_pref(self, url_list):
        buf = []
        for x in url_list:
            soup = _helper.get_soup(x['href']).s
            buf += Media(soup).pref
        return buf

    def get_media_url(self, soup):
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
    def __init__(self, soup, url_array):
        super(Sequence, self).__init__()
        # init
        global SeqFlag
        global LimitTime
        stop_time = _helper.get_limit_time(LimitTime)
        i = 1
        self.pref = []
        # view time now
        d = datetime.datetime.today()
        print('--- Donwload Sequence わくてか速報 ---')
        print('http://' + '/'.join(url_array))
        print('Start Time is {}/{}/{} {}:{}'.format(
            d.year, d.month, d.day, d.hour, d.minute
        ))
        # start analy
        del url_array[-1]
        while True:
            print('Scaning page:' + str(i) + '...')
            url = 'http://' + '/'.join(url_array) + '/?p=' + str(i)
            soup = _helper.get_soup(url)
            self.pref += Index(soup).pref
            i += 1
            if self.get_files_day(soup) < stop_time:
                break
        # Finish
        SeqFlag = True
        print("")

    def get_files_day(self, soup):
        t = soup.body.findAll('abbr', attrs={"class": "updated"})
        times = []
        # get times
        for x in t:
            x = x['title']
            x = x.replace('-', '')
            x = x.replace('T', '')
            time_string = str(x)
            array = time_string.split(':')
            del array[-1]
            time_string = ''.join(array)
            times += [int(time_string)]
        return min(times)


# === test code ===
# 2015/10/01 00:00
# url = 'http://blog.livedoor.jp/wakusoku/SEQUENCE'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
