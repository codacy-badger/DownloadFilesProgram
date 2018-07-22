# -*- coding: utf-8 -*-
import datetime
import os

from .AccessSite.OpenHTML import SoupURL


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
        st = SiteType(url_array)
        soup = SoupURL(url)
        urls = self.get_urls(st.type, soup.s, url_array)
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


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, url_array):
        super(SiteType, self).__init__()
        self.type = self.get_type(url_array)

    def get_type(self, url_array):
        global SeqFlag
        if url_array[1] == 'archives':
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
        try:
            div_tags = soup.find(
                'div', attrs={'class': 'article-body'}
            )
            img_tags = div_tags.findAll('img')
        except:     # this type is advertisement
            raise
        x = []
        cnt = 0
        for i in img_tags:
            try:
                _url = i['srcset'].split(',')[-1].strip()
            except:
                _url = i['src'].strip()
            url = 'http:' + _url.split(' ')[0].strip()

            title = str(cnt).zfill(3) + '.' + url.split('.')[-1]
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
            soup = SoupURL(x['href']).s
            try:
                buf += Media(soup).pref
            except:
                print('Error')
                pass
        return buf

    def get_media_url(self, soup):
        div_tags = soup.findAll(
            'span', attrs={'class': 'archives-list__item-thumbnail'})
        # get title and url
        x = []
        for i in div_tags:
            a = i.parent
            if a['href'] is not None:
                x += [{
                    'title': i.img['alt'].encode('utf-8'),
                    'href': a['href'].encode('utf-8')
                }]
        return x


class Sequence(object):
    """docstring for Sequence"""
    def __init__(self, soup, url_array):
        super(Sequence, self).__init__()
        # init
        global SeqFlag
        # stop_time = self.get_limit()
        i = 1
        self.pref = []
        # view time now
        d = datetime.datetime.today()
        print('--- Donwload Sequence 最強二次元エロ画像 ---')
        print('http://' + '/'.join(url_array))
        print('Start Time is {}/{}/{} {}:{}'.format(
            d.year, d.month, d.day, d.hour, d.minute
        ))
        # start analy
        del url_array[-1]
        # this site doesn't have date-data,
        # so SEQUENCE is to scan 3 pages
        for i in range(1, 4):
            print('Scaning page:' + str(i) + '...')
            url = 'http://' + '/'.join(url_array) + '/' + str(i)
            soup = SoupURL(url).s
            self.pref += Index(soup).pref
            # i += 1
            # if self.get_files_day(soup) < stop_time:
            #     break
        # Finish
        SeqFlag = True
        print("")

    def get_limit(self):
        global LimitTime
        # check LimitTime
        limit_day = LimitTime
        if limit_day is None:
            print('Till when?')
            print('ex. YYYY/MM/DD hh:mm')
            limit_day = raw_input('-> ')
        # check Str Type
        while True:
            LimitTime = limit_day
            limit_day = limit_day.replace(' ', '')
            limit_day = limit_day.replace('/', '').replace(':', '')
            if len(limit_day) == 12:
                return int(limit_day)
            else:
                print('Oops!')
                limit_day = raw_input('-> ')

    def get_files_day(self, soup):
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
# url = 'http://nizigazo.net/archives/66427'
# url = 'http://nizigazo.net/page/SEQUENCE'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.file_status['urls']:
#     print(media['title'])
#     print(media['href'])
#     print('')
