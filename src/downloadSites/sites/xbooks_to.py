# -*- coding: utf-8 -*-
import datetime
import urllib
import re

from bs4 import BeautifulSoup

from . import _helper
from ._helper import AccessPage


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
        self.file_status = {
            'urls': urls,
            'dir': 'h_manga_place'}

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
        if url_array[1] == 'detail':
            global Title
            url_type = 'media'   # media url
            Title = url_array[-1]
        elif url_array[1] == 'search':
            if url_array[-1] == 'SEQUENCE':
                if SeqFlag:
                    SeqFlag = False
                    url_type = 'sequence'   # search result
                else:
                    url_type = 'index'
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
        title = soup.title.string
        if title[0:5] == u'COMIC':
            title = u'[雑誌]' + title[5:]
        title = title.split('│')[0]
        return title + '.zip'

    def get_file_url(self, soup):
        a = soup.select("#download > li:nth-of-type(2) > a")[0]
        top_url = "http://xbooks.to"
        file_url = (top_url + a['href'])
        return file_url


class Index(object):
    """docstring for Index"""
    def __init__(self, soup):
        super(Index, self).__init__()
        self.pref = self.get_media_url(soup)
        # filter
        buf = []
        for x in self.pref:
            if self.file_filter(x['title']):
                buf += [x]
        self.pref = buf

    def get_media_url(self, soup):
        # get a tags
        content_list = soup.select_one('#main2col > div.content_list')
        h3s = content_list.findAll('h3')
        x = [h3.a for h3 in h3s]
        # convert url
        fix = []
        for i in x:
            url = (
                'http://xbooks.to/detail/download_zip/' + i['href'].split('/')[-1]
            )
            fix += [{
                'title': i['title'].replace('/', '_') + '.zip',
                'href': url
            }]
        return fix

    def file_filter(self, title):
        title = title.strip()

        if re.match(r'^\[.+\](?!.+_\d).+$', title) is not None:
            return True
        elif re.match(
            u'^\((C|成年コミック|同人CG集).+\)*\[.+\](?!.+_\d).+$', title
        ) is not None:
            return True
        elif re.match(r'^COMIC.+(?!.+_\d).+$', title) is not None:
            return True
        return False


class Sequence(object):
    """docstring for Sequence"""
    def __init__(self, soup, url_array):
        super(Sequence, self).__init__()
        # init
        global SeqFlag
        global LimitTime
        stop_time = _helper.get_limit_time(LimitTime)
        self.pref = []
        # view time now
        d = datetime.datetime.today()
        print('--- Donwload Sequence dropBOOKS ---')
        print('http://' + '/'.join(url_array))
        print('Start Time is {}/{}/{} {}:{}'.format(
            d.year, d.month, d.day, d.hour, d.minute))
        # start analy
        del url_array[-1]
        i = 1
        while True:
            print('Scaning page:{}...'.format(i))
            url = 'http://{}/page:{}'.format('/'.join(url_array), i)
            url = _helper.convert_url(url)
            soup = _helper.get_soup(url)
            self.pref += Index(soup).pref
            i += 1
            if self.get_files_day(soup) < stop_time:
                break
        # Finish
        SeqFlag = True
        print("")

    def get_files_day(self, soup):
        content_list = soup.select_one('#main2col > div.content_list')
        p_tabs = content_list.findAll('p', attrs={"class": "time"})
        times = []
        # get times
        for x in p_tabs:
            time_string = x.string[1:]
            time_string = time_string.replace(' ', '')
            time_string = time_string.replace('/', '').replace(':', '')
            times.append(int(time_string))
        return min(times)


# === test code ===
# url = 'http://xbooks.to/tops/index/term:no/page:1'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
