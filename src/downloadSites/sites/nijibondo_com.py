# -*- coding: utf-8 -*-
import os
import datetime

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
        url_type = self._get_site_type(url_array)
        soup = _helper.get_soup(url)
        urls = self.get_urls(url_type, soup.s, url_array)
        self.file_status = {'urls': urls, 'dir': 'h_pic_place'}

    def get_urls(self, url_type, soup, url_array):
        if url_type == 'media':
            list_url = Media(soup).pref
        elif url_type == 'index':
            list_url = Index(soup).pref
        elif url_type == 'sequence':
            list_url = Sequence(soup, url_array).pref
        else:
            list_url = []
        return list_url

    def _get_site_type(self, url_array):
        global SeqFlag
        if len(url_array) == 3:
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
        try:
            title = soup.title.string.split(u'｜')[0].strip()
            title = title.replace('/', '_')
            return title
        except:
            raise

    def get_media_url(self, soup):
        div_tag = soup.find('div', attrs={'id': 'the-content'})
        a_tags = div_tag.findAll('a')
        x = []
        cnt = 0
        for a in a_tags:
            url = a['href']
            title = str(cnt).zfill(3) + url[-4:]
            cnt += 1
            x += [{
                'title': os.path.join(self.parent, title),
                'href': url
            }]
        return x


class Index(object):
    """docstring for Index"""
    def __init__(self, soup):
        super(Index, self).__init__()
        url_list = self.get_media_url(soup)
        self.pref = self.get_pref(url_list)

    def get_pref(self, url_list):
        buf = []
        for x in url_list:
            soup = _helper.get_soup(x['href'])
            try:
                buf += Media(soup).pref
            except:
                print('Error')
                pass
        return buf

    def get_media_url(self, soup):
        div = soup.find('div', attrs={'id': 'list'})
        h2_tags = div.findAll('h2')

        # get title and url
        x = []
        for i in h2_tags:
            a = i.a
            if a['href'] is not None:
                x += [{
                    'title': a.string,
                    'href': a['href']
                }]
        return x


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
        print('--- Donwload Sequence にじぼんど！ ---')
        print('http://' + '/'.join(url_array))
        print('Start Time is {}/{}/{} {}:{}'.format(
            d.year, d.month, d.day, d.hour, d.minute
        ))
        # start analy
        del url_array[-1]
        while True:
            print('Scaning page:' + str(i) + '...')
            url = 'http://{}/page/{}'.format('/'.join(url_array), i)
            soup = _helper.get_soup(url)
            self.pref += Index(soup).pref
            i += 1
            if self.get_files_day(soup) < stop_time:
                break
        # Finish
        SeqFlag = True
        print("")

    def get_files_day(self, soup):
        span_tags = soup.body.find_all('span', attrs={'class': 'published'})
        times = []
        # get times
        for x in span_tags:
            if x.text is not None:
                s = x.string.split('/')
                s_zerofill = []
                for i in s:
                    s_zerofill.append(i.zfill(2))
                x = ''.join(s_zerofill)
                x = x.replace(':', '')
                times += [int(x)]
        return min(times)


# === test code ===
# 2016/02/21 20:00
# url = 'http://nijibondo.com/hentai-girls-talk'
# url = 'http://nijibondo.com/page/SEQUENCE'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.file_status['urls']:
#     print(media['title'])
#     print(media['href'])
#     print('')
